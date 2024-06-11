import asyncio
import os

from dotenv import load_dotenv

from parea import Parea

load_dotenv()

p = Parea(api_key=os.getenv("PAREA_API_KEY"))


async def main():
    print(p.get_trace_log("2b7542e3-eead-4f76-89f6-c59c272e6a87"))
    print(await p.aget_trace_log("2b7542e3-eead-4f76-89f6-c59c272e6a87"))


asyncio.run(main())
