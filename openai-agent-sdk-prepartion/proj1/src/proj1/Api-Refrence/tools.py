from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider,RunContextWrapper,function_tool,
from openai import AsyncOpenAI
from typing import cast, Any
import os
from dotenv import load_dotenv
from agents import FunctionTool
import json


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



@function_tool(
        name_override="Add_two_numbers",
        description_override="This tool add two numbers", 
        strict_mode=True ,
        is_enabled= True,
        docstring_style="google",
        use_docstring_info=True,
              )
def calculator(a,b):
    return a+b


panacloud_agent: Agent = Agent(
    name="panacloud_agent",
    instructions="You can always answer user question calling tool if tool output dont match with user query just tell him i am unable to answer this ",
    model=model,
    tools=[calculator]
)

response = Runner.run_sync(panacloud_agent, "calculate sum of two numbers 2 and 2", run_config=config)
print(response.final_output)

print(response.raw_responses)