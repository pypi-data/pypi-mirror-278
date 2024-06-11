import os

from dotenv import load_dotenv

from parea import Parea, trace, trace_insert
from parea.schemas import Completion, LLMInputs, Log, Message, ModelParams, Role

load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"))


# def eval_func(log: Log) -> float:
#     from random import random
#     from time import sleep
#
#     sleep(random() * 10)
#     return random()


# annotate the function with the trace decorator and pass the evaluation function(s)
@trace(eval_funcs_names=["Coverage (LLM)"])
def func(post, title, text, coverage) -> str:
    return text


if __name__ == "__main__":
    p.experiment(
        name="Coverage",
        data="Summarization Validation",  # this is the name of your Dataset in Parea (Dataset page)
        func=func,
    ).run()

    # Or use a dataset using its ID instead of the name
    # p.experiment(
    #     data=121,  # this is the id of your Dataset in Parea (Dataset page)
    #     func=func,
    # ).run(name="hello-world-example")
