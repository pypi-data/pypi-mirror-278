import os
import random

from dotenv import load_dotenv
from openai import OpenAI

from parea import Parea, trace
from parea.evals.general import levenshtein

load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"), project_name="testing")

client = OpenAI()
p.wrap_openai_client(client)


def random_eval(log) -> float:
    return random.random()


# annotate the function with the trace decorator and pass the evaluation function(s)
@trace(eval_funcs=[random_eval])
def greeting(name: str) -> str:
    # return (
    #     client.chat.completions.create(
    #         messages=[{"role": "user", "content": f"Hello {name}"}],
    #         model="gpt-3.5-turbo-0125",
    #         temperature=0.7,
    #         max_tokens=10,
    #         top_p=1.0,
    #     )
    #     .choices[0]
    #     .message.content
    # )
    return name


data = [
    {
        "name": "Foo",
        "target": "Hi Foo",
    },
    {
        "name": "Bar",
        "target": "Hello Bar",
    },
]  # test data to run the experiment on (list of dicts)


# # Define the experiment
# # You can use the CLI command "parea experiment parea/cookbook/run_experiment.py" to execute this experiment
# # or call `.run()`
# # p.experiment(
# #     data=data,  # Data to run the experiment on (list of dicts)
# #     func=greeting,  # Function to run (callable)
# #     n_trials=1,  # Number of times to run the experiment on the same data
# # )


# You can optionally run the experiment manually by calling `.run()`
if __name__ == "__main__":
    p.experiment(
        name="greeting",
        data=data,
        func=greeting,
        n_trials=100,
    ).run()
