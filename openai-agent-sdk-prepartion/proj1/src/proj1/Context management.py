# from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider, RunContextWrapper,function_tool
# from openai import AsyncOpenAI
# from typing import cast
# import os
# from dotenv import load_dotenv
# from dataclasses import dataclass

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


# @dataclass
# class Car:
#     name:str
#     color:str
#     price:int


# @function_tool
# def get_car_info(context:RunContextWrapper[Car]):
#     return f"car name is {context.context.name} color is {context.context.color} price is {context.context.price}"

# car = Car(name="BMW",color="Red",price=20000)

# panacloud_agent: Agent = Agent[Car](
#     name="panacloud_agent",
#     instructions="when user ask about car name car price car color so use `get_car_info` tool anf then answer them",
#     tools=[get_car_info],
#     model=model,
# )

# response = Runner.run_sync(panacloud_agent, "what is the name of car?", run_config=config, context=car)
# print(response.final_output)




"""LLM-CONTEXT"""

from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider,RunContextWrapper
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from dataclasses import dataclass

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

@dataclass
class Flight:
    name:str
    day:str

def dynamic_instructions(context: RunContextWrapper[Flight], agent: Agent[Flight]):
    return f"You are talking to {context.context.name}. Today is {context.context.day}. Be friendly.salam the user with his name {context.context.name}"

# 2. Create the agent with dynamic instructions (this goes to LLM)
agent = Agent[Flight](
    name="TravelBot",
    instructions=dynamic_instructions,
    model= model
)



llm_context= Flight(name="shiraz",day="Eid Holiday")

response = Runner.run_sync(agent,  input="Can you help me book a flight to Lahore?", run_config=config, context=llm_context)
print(response.final_output)
