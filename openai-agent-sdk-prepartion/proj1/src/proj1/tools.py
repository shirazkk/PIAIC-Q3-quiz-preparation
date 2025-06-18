# import json

# from typing_extensions import TypedDict, Any

# from agents import Agent, FunctionTool, RunContextWrapper, function_tool


# class Location(TypedDict):
#     lat: float
#     long: float

# @function_tool  
# async def fetch_weather(location: Location) -> str:
    
#     """Fetch the weather for a given location.

#     Args:
#         location: The location to fetch the weather for.
#     """
#     # In real life, we'd fetch the weather from a weather API
#     return "sunny"


# @function_tool(name_override="fetch_data")  
# def read_file(ctx: RunContextWrapper[Any], path: str, directory: str | None = None) -> str:
#     """Read the contents of a file.

#     Args:
#         path: The path to the file to read.
#         directory: The directory to read the file from.
#     """
#     # In real life, we'd read the file from the file system
#     return "<file contents>"


# agent = Agent(
#     name="Assistant",
#     tools=[fetch_weather, read_file],  
# )

# for tool in agent.tools:
#     if isinstance(tool, FunctionTool):
#         print(tool.name)
#         print(tool.description)
#         print(json.dumps(tool.params_json_schema, indent=2))
#         print()






"""CUSTOM FUNCTION TOOL"""

# from typing import Any

# from pydantic import BaseModel

# from agents import RunContextWrapper, FunctionTool, RunResult, ToolCallOutputItem



# def do_some_work(data: str) -> str:
#     return "done"


# class FunctionArgs(BaseModel):
#     username: str
#     age: int


# async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
#     parsed = FunctionArgs.model_validate_json(args)
#     return do_some_work(data=f"{parsed.username} is {parsed.age} years old")


# tool = FunctionTool(
#     name="process_user",
#     description="Processes extracted user data",
#     params_json_schema=FunctionArgs.model_json_schema(),
#     on_invoke_tool=run_function,
# )

# print(tool.params_json_schema)

# ---------------------------------------------------------------------------------------------------------

from agents import  RunResult, ToolCallOutputItem
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv


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



async def extract_json_payload(run_result: RunResult) -> str:
    # Scan the agent’s outputs in reverse order until we find a JSON-like message from a tool call.
    for item in reversed(run_result.new_items):
        if isinstance(item, ToolCallOutputItem) and item.output.strip().startswith("{"):
            return item.output.strip()
    # Fallback to an empty JSON object if nothing was found
    return "{}"

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that returns JSON data.",
    model=model,
)


json_tool = agent.as_tool(
    tool_name="get_data_json",
    tool_description="Run the data agent and return only its JSON payload",
    custom_output_extractor=extract_json_payload,
)

async def run_panacloud_agent():
    panacloud_agent: Agent = Agent(
        name="panacloud_agent",
        instructions="You are helpful assistant",
        model=model,
        tools=[json_tool],
    )

    response = await Runner.run(panacloud_agent, "who is founder of pakistan", run_config=config)
    print(response.final_output)    


def main():
    import asyncio
    asyncio.run(run_panacloud_agent())