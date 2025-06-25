from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider,set_default_openai_key, set_default_openai_client,set_default_openai_api,set_tracing_export_api_key,set_trace_processors,enable_verbose_stdout_logging
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv



# If we can't set the OpenAI key in the environment, we can use this function to set the key directly.
# By default, tracing is enabled (True). If we disable tracing (set it to False), we must either set the OpenAI key in the environment
# or use set_tracing_export_api_key() to enable tracing.
# set_default_openai_key(key="openai_key",use_for_tracing=False) 


# external_client = AsyncOpenAI(
#     api_key= "gemini_api_key",
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )


# set_default_openai_client(client=external_client,use_for_tracing=False)

# set_default_openai_api("chat_completions")


# set_tracing_export_api_key(api_key="OPENAI_KEY")

# set_tracing_disabled(disabled=True)


# set_trace_processors(processors=)








enable_verbose_stdout_logging()



load_dotenv()


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


panacloud_agent: Agent = Agent(
    name="panacloud_agent",
    instructions="You are helpful assistant",
    model=model,
)

response = Runner.run_sync(panacloud_agent, "who is founder of pakistan", run_config=config)
print(response.final_output)


