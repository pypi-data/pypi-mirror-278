import os
import uuid
from random import random

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader

from parea import Parea, get_current_trace_id, trace
from parea.evals.general import answer_matches_target_llm_grader_factory
from parea.schemas import Completion, FeedbackRequest, LLMInputs, Message, ModelParams, Role

load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"), project_name="pg-essay")


def call_llm(content: str, model: str) -> str:
    return p.completion(
        data=Completion(
            llm_configuration=LLMInputs(
                model=model,
                model_params=ModelParams(temp=0.0),
                messages=[Message(role=Role.user, content=content)],
            )
        )
    ).content


paul_graham_essay = SimpleDirectoryReader("pg-essay").load_data()


def factory(model: str) -> callable:
    @trace
    def summarize_paul_graham_essay(context: str, question: str) -> str:
        content = f"""
        Review the following document:\n{context}
        \nAnswer the following question:{question}
        \n\nResponse:
        """

        score_base = 0.3
        if model.startswith("gpt-4"):
            score_base = 0.7
        elif model.startswith("claude"):
            score_base = 0.5
        p.record_feedback(
            FeedbackRequest(
                score=score_base + random() * 0.3,
                trace_id=get_current_trace_id(),
            )
        )

        return call_llm(content, model)

    return summarize_paul_graham_essay


def run():
    # for model in ["gpt-4-0125-preview"]:
    for model in ["gpt-4-32k-0613", "claude-3-haiku-20240307", "gemini-pro", "gpt-4-0125-preview"]:
        for question in [
            "What company did Paul leave after returning to painting",
            "What seminal event helped Paul Graham realize the potential power of publishing content online, and how did this realization impact his work?",
        ]:
            func = factory(model)
            response = func(context=paul_graham_essay[0].text, question=question)
            print(f"{model} response: {response}")
            print()


if __name__ == "__main__":
    run()
