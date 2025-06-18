from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    websocket_base_url="wss://generativelanguage.googleapis.com/v1beta/openai/",
    timeout=10,
    max_retries=3,
    project= "Panacloud Agent",
    organization="my-organization-id",
    default_headers={"Authorization": f"Bearer {gemini_api_key}"},
    default_query={"query_param": "example_value"},
    http_client=httpx.AsyncClient(),
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


panacloud_agent: Agent = Agent(
    name="panacloud_agent",
    instructions="You are helpful assistant",
    model=model,
)

response = Runner.run_sync(panacloud_agent, "who is founder of pakistan", run_config=config)
print(response.final_output)
