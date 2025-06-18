# from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider
# from openai import AsyncOpenAI
# from typing import cast
# import os
# from dotenv import load_dotenv
# from openai.types.responses import ResponseTextDeltaEvent
# import asyncio

# load_dotenv()

# set_tracing_disabled(disabled=True)

# gemini_api_key = os.getenv("GEMINI_API_KEY")

# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# external_client = AsyncOpenAI(
#     api_key= gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client,
# )

# config = RunConfig(
#     model=model,
#     model_provider=cast(ModelProvider, external_client),
#     tracing_disabled=True,

# )

# async def run_panacloud_agent():
#     panacloud_agent: Agent = Agent(
#         name="panacloud_agent",
#         instructions="You are helpful assistant",
#         model=model,
#     )

#     response = Runner.run_streamed(panacloud_agent, "who is founder of pakistan", run_config=config)

#     async for event in response.stream_events():
#         if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
#             print(event.data.delta, end="" , flush=True)
        
# def main():
#     asyncio.run(run_panacloud_agent())







from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider,function_tool,ItemHelpers
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv

import asyncio

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@function_tool
def weather_tool():
    """
    A tool to get the current weather.
    """
    return "The current weather is sunny with a temperature of 25°C."


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

async def run_panacloud_agent():
    panacloud_agent: Agent = Agent(
        name="panacloud_agent",
        instructions="You are helpful assistant",
        model=model,
        tools=[weather_tool],
    )

    response = Runner.run_streamed(panacloud_agent, "what is current weather", run_config=config)

    async for event in response.stream_events():
        if event.type == "raw_response_event":
           continue
        elif event.type =="agent_updated_stream_event":
           print(f"Agent Updated: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print(f"Tool wa called: {event.item.agent.tools[0].name}")
            elif event.item.type == "tool_call_output_item":
                print(f"TOOl Call output item: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n ,{ItemHelpers.text_message_output(event.item)}")
            else: 
                pass
        
def main():
    asyncio.run(run_panacloud_agent())