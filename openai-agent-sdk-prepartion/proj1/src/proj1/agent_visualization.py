from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider, RunContextWrapper
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents.extensions.visualization import draw_graph


load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


class UserContext(BaseModel):
    name:str
    is_alive:bool

def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."




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


user = UserContext(name="shirazali", is_alive=False)

panacloud_agent: Agent = Agent[UserContext](
    name="panacloud_agent",
    instructions=dynamic_instructions,
    model=model,
)

result = Runner.run_sync(panacloud_agent, "hello", run_config=config, context=user)
for item in result.new_items:
        print(f"Item Type: {item.__class__.__name__}")
print(result.final_output)
print(result.raw_responses)

draw_graph(panacloud_agent, filename="agent_graph")



