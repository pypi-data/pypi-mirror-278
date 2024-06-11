<center>
    <p style="text-align:center">
        <img alt="parea logo" src="https://media.dev.to/cdn-cgi/image/width=320,height=320,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Forganization%2Fprofile_image%2F8067%2Fc508b9f7-50ae-43b6-91fc-d8535102b518.png" width="200"/>
        <br>
        <a href="https://docs.parea.ai/">Docs</a>
        |
        <a href="https://github.com/parea-ai/parea-sdk-py">GitHub</a>
        |
        <a href="https://discord.gg/KbHtZqwvsQ">Community</a>
    </p>
</center>
<h1 align="center">Tracing & Evaluating a DSPy Application</h1>

DSPy is a framework for automatically prompting and fine-tuning language models. It provides:

- Composable and declarative APIs that allow developers to describe the architecture of their LLM application in the form of a "module" (inspired by PyTorch's `nn.Module`),
- Optimizers formerly known as "teleprompters" that optimize a user-defined module for a particular task. The optimization could involve selecting few-shot examples, generating prompts, or fine-tuning language models.

Parea makes your DSPy applications *observable* by visualizing the underlying structure of each call to your compiled DSPy module and surfacing problematic spans of execution based on latency, token count, or other evaluation metrics. Additionally, Parea allows you to *track the performance* of your DSPy modules over time, across different architectures, optimizers, etc.

In this tutorial, you will:
- Build and optimize DSPy modules that use retrieval-augmented generation and multi-hop reasoning to answer questions over AirBnB 2023 10k filings dataset,
- Instrument your application using [Parea AI](https://parea.ai),
- Inspect the traces of your application to understand the inner works of a DSPy forward pass.
- Evaluate your modules
- Understand how many samples are necessary to achieve good performance on the test set.

ℹ️ This notebook requires an OpenAI API key.
ℹ️ This notebook requires a Parea API key, which can be created [here](https://docs.parea.ai/api-reference/authentication#parea-api-key).


## 1. Install Dependencies and Import Libraries

Install Parea, DSPy, ChromaDB, and other dependencies.


```python
!pip install "regex~=2023.10.3" dspy-ai  # DSPy requires an old version of regex that conflicts with the installed version on Colab
!pip install parea-ai chromadb
```

⚠️ DSPy conflicts with the default version of the `regex` module that comes pre-installed on Google Colab. If you are running this notebook in Google Colab, you will likely need to restart the kernel after running the installation step above and before proceeding to the rest of the notebook, otherwise, your instrumentation will fail.

Import libraries.


```python
import json
import os
import random
from getpass import getpass

import chromadb
import dspy
import nest_asyncio
import openai
from dsp.utils import deduplicate
from dspy import evaluate as dspy_eval
from dspy.retrieve.chromadb_rm import ChromadbRM
from dspy.teleprompt import BootstrapFewShot

from parea import Parea
from parea.utils.trace_integrations.dspy import attach_evals_to_module, convert_dspy_examples_to_parea_dicts
```

## 2. Configure Your OpenAI & Parea API Key

Set your OpenAI & Parea API key if they are not already set as environment variables.


```python
for api_key_name in ["OPENAI_API_KEY", "PAREA_API_KEY"]:
    if not (api_key_value := os.getenv(api_key_name)):
        api_key_value = getpass(f"🔑 Enter your {api_key_name.split('_')[0].title()} API key: ")
    if api_key_name == "OPENAI_API_KEY":
        openai.api_key = api_key_value
    os.environ[api_key_name] = api_key_value
```

## 3. Configure LM

We will use `gpt-3.5-turbo` as our LLM of choice for this tutorial.


```python
turbo = dspy.OpenAI(model="gpt-3.5-turbo")
dspy.settings.configure(lm=turbo)
```

## 4. Load & Index Data

Next we will download [Virat](https://twitter.com/virattt)'s processed AirBnB 2023 10k filings dataset. This dataset contains 100 triplets of question, relevant context, and answer from AirBnB's 2023 10k filings. We will store the contexts in ChromaDB to fetch those to when trying to answer a question.


```python
path_qca = "airbnb-2023-10k-qca.json"

if not os.path.exists(path_qca):
    !wget https://virattt.github.io/datasets/abnb-2023-10k.json -O airbnb-2023-10k-qca.json

with open(path_qca, "r") as f:
    question_context_answers = json.load(f)

chroma_client = chromadb.PersistentClient()
collection = chroma_client.get_or_create_collection(name="contexts")
if collection.count() == 0:
    collection.add(documents=[qca["context"] for qca in question_context_answers], ids=[str(i) for i in range(len(question_context_answers))])
```

Now let's transform the dataset into `dspy.Example` objects and mark the `question` field as the input field. Then, we can split the data into a training and test set.


```python
qca_dataset = []
for qca in question_context_answers:
    # Tell DSPy that the 'question' field is the input. Any other fields are labels and/or metadata.
    qca_dataset.append(dspy.Example(question=qca["question"], answer=qca["answer"], golden_context=qca["context"]).with_inputs("question"))

random.seed(2024)
random.shuffle(qca_dataset)
train_set = qca_dataset[: int(0.7 * len(qca_dataset))]
test_set = qca_dataset[int(0.7 * len(qca_dataset)) :]

len(train_set), len(test_set)
```

Each sample in our dataset has a question, a golden context and a human-annotated answer.


```python
train_set[0]
```

## 5. Define A Simple RAG Module

In order to define the RAG module, we need to define a signature that takes in two inputs, `context` and `question`, and outputs an `answer`. The signature provides:

- A description of the sub-task the language model is supposed to solve.
- A description of the input fields to the language model.
- A description of the output fields the language model must produce.


```python
class GenerateAnswer(dspy.Signature):
    """Answer questions with short factoid answers."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")
```

Define your module by subclassing `dspy.Module` and overriding the `forward` method. Here, we use ChromaDB to retrieve the top-k passages from the context and then use the Chain-of-Thought generate the final answer.


```python
class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = ChromadbRM("contexts", "./chroma", k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = [r["long_text"] for r in self.retrieve(question)]
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)
```

## 6. Evaluate the RAG Module

We will use Parea to evaluate the RAG module on the test set. This consists of two parts:
- **instrumentation**: We will trace the execution of the module components to understand how the module processes the input: done by the `trace_dspy` method.
- **experimentation**: We will run an experiment to see the model's performance on the test set.

To be able to execute experiments in a notebook, we need to apply a patch to the `nest_asyncio` module.


```python
p = Parea(api_key=os.getenv("PAREA_API_KEY"))
p.trace_dspy()

nest_asyncio.apply()
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # needed because of transformers
```

We will use two evaluation functions for our experiment:
- `dspy.evaluate.answer_exact_match`: checks if the predicted answer is an exact match with the target answer.
- `gold_passages_retrieved`: checks if the retrieved context matches the golden context.

Note, we need to convert the list of `dspy.Example`s into a list of dictionaries and also attach the evaluation metric to the module such that we can execute the experiment with Parea. We can do the former via `convert_dspy_examples_to_parea_dicts` and the latter via `attach_evals_to_module`.


```python
def gold_passages_retrieved(example, pred, trace=None):
    return any(example["golden_context"] == c for c in pred.context)


p.experiment(
    "AirBnB 10 k filings",  # name of the experiment
    convert_dspy_examples_to_parea_dicts(test_set),  # dataset of the experiment
    attach_evals_to_module(RAG(), [dspy_eval.answer_exact_match, gold_passages_retrieved]),  # function which should be evaluated
).run(
    "simple-rag"
)  # name of the run
```

We can see that only in 37% of the cases the correct context is retrieved. Additionally, by looking at the relationship between the retrieval accuracy (`gold_passages_retrieved`) and the overall accuracy of our RAG pipeline (`answer_exact_match`), we can see our retrieval step is the bottleneck (e.g. both metrics agree in 90% of cases).

![Simple RAG](https://drive.google.com/uc?id=1zZ-9b9PVfeeIX6fgSfqu_8NapIscpLsw)

When inspecting a single sample, we can see that the retrieved context (middle red box) doesn't match the question (top red box) and the correct context (bottom red box) at all:

![Bad Retrieval](https://drive.google.com/uc?id=1zBXRzKmTde4Qtd3cegSV1xAb9iUExDIu)

## 7. We need better retrieval: Simplified Baleen

One way to improve this to iteratively refine the query given already retrieved contexts before generating a final answer. This is encapsulated in standard NLP by multi-hop search systems, c.f. e.g. Baleen (Khattab et al., 2021). Let's try it out!

For that we will introduce a new `Signature`: given some context and a question, generate a new query to find more relevant information.


```python
class GenerateSearchQuery(dspy.Signature):
    """Write a simple search query that will help answer a complex question."""

    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    query = dspy.OutputField()
```

Now we can define a simplified version of Baleen. Concretely, we will do in the `forward` pass:

1. Loop `self.max_hops` times to fetch diverse contexts. In each iteration:
    1. Generate a search query using Chain-of-Thought (the predictor at `self.generate_query[hop]`).
    2. Then, retrieve the top-k passages using that query.
    3. Finally, add the (deduplicated) passages to our accumulated context.
2. After the loop, `self.generate_answer` generates an answer via CoT.
3. Finally, return a prediction with the retrieved context and predicted answer.

Note, we need to pull `ChromadbRM` outside of the module declaration to ensure that the module is pickleable, which is a requirement to optimize it later on.


```python
def retrieve_passages(query, k):
    retriever = ChromadbRM("contexts", "./chroma", k=k)
    return [r["long_text"] for r in retriever(query)]


class SimplifiedBaleen(dspy.Module):
    def __init__(self, passages_per_hop=3, max_hops=2):
        super().__init__()

        self.generate_query = [dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)]
        self.passages_per_hop = passages_per_hop
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
        self.max_hops = max_hops

    def forward(self, question):
        context = []

        for hop in range(self.max_hops):
            query = self.generate_query[hop](context=context, question=question).query
            passages = retrieve_passages(query, self.passages_per_hop)
            context = deduplicate(context + passages)

        pred = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=pred.answer)
```

## 8. Optimizing the Baleen Model

Now, we can apply the **magic** of DSPy and optimize our model on our training set. For that we need to select an optimizer and define an evaluation metric.

As optimizer, we will choose the `BootstrapFewShot` optimizer which uses few-shot examples to boost the performance of the prompts. To evaluate the pipeline we will apply the following logic:
1. check if the predicted answer is an exact match with the target answer
2. check if the retrieved context matches the golden context
3. check if the queries for the individual hops aren't too long
4. check if the queries are sufficiently different from each other


```python
def validate_context_and_answer_and_hops(example, pred, trace=None):
    if not dspy.evaluate.answer_exact_match(example, pred):
        return False
    if not gold_passages_retrieved(example, pred):
        return False

    hops = [example.question] + [outputs.query for *_, outputs in trace if "query" in outputs]

    if max([len(h) for h in hops]) > 100:
        return False
    if any(dspy.evaluate.answer_exact_match_str(hops[idx], hops[:idx], frac=0.8) for idx in range(2, len(hops))):
        return False

    return True


teleprompter = BootstrapFewShot(metric=validate_context_and_answer_and_hops)
compiled_baleen = teleprompter.compile(SimplifiedBaleen(), teacher=SimplifiedBaleen(passages_per_hop=2), trainset=train_set)
```

Now let's compare the unoptimized with the optimized system to see if there are any improvements:


```python
p.experiment(
    "AirBnB 10 k filings",
    convert_dspy_examples_to_parea_dicts(test_set),
    attach_evals_to_module(SimplifiedBaleen(), [dspy_eval.answer_exact_match, gold_passages_retrieved]),
).run("unoptimized-baleen")

p.experiment(
    "AirBnB 10 k filings", convert_dspy_examples_to_parea_dicts(test_set), attach_evals_to_module(compiled_baleen, [dspy_eval.answer_exact_match, gold_passages_retrieved])
).run("optimized-baleen")
```

When selecting both experiments in the overview, we can that our retrieval accuracy has increased from 40% to 53.3% and the overall accuracy has increased from 37% to 43%.

![Experiments Comparison](https://drive.google.com/uc?id=1NI8_ELz-0Gyxw2VqQwz_HyuBOua_HVT2)

## 9. Ablation on Training Samples

Finally, let's see how many samples are actually necessary to achieve a performance improvement. For that we will repeat the optimization with 5, 10, 25, 50, and all training samples.


```python
for n_train in [5, 10, 25, 50, len(train_set)]:
    teleprompter = BootstrapFewShot(metric=validate_context_and_answer_and_hops)
    compiled_baleen = teleprompter.compile(SimplifiedBaleen(), teacher=SimplifiedBaleen(passages_per_hop=2), trainset=train_set[:n_train])

    p.experiment(
        "AirBnB 10 k filings", convert_dspy_examples_to_parea_dicts(test_set), attach_evals_to_module(compiled_baleen, [dspy_eval.answer_exact_match, gold_passages_retrieved])
    ).run(f"n_train-{n_train}")
```

We can see that our optimization has started to overfit on the training set when we use more than 50 training samples. Using 50 training samples leads to 77% correct retrieved context and 63% overall accuracy on the test set.

![Experiments Overview](https://drive.google.com/uc?id=1JTsNyLWqv7onuYnRAwHhEggr7oJvP4U-)

Now, it's your tun to achieve 100% accuracy on the test set! 🚀


```python

```
