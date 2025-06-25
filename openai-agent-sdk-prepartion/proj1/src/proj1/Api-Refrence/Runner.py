from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider, ItemHelpers
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=cast(ModelProvider, external_client),
    tracing_disabled=True,

)

async def main():
    panacloud_agent: Agent = Agent(
            name="panacloud_agent",
            instructions="You are helpful assistant",
            model=model,
        )

    response =  Runner.run_streamed(
            starting_agent=panacloud_agent, 
            input="who is founder of pakistan", 
            run_config=config,
            # max_turns=0
            )
    async for event in response.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
            print(event.data.delta, end=" ", flush=True)



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

