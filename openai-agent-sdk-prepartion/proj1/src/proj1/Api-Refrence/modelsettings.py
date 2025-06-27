from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider , ModelSettings
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



model_setting = ModelSettings(
    temperature= 1.0, #control randomness higher value make output more random low value make ouput predictable
    top_p= 0.9, #Top-p (Nucleus Sampling) controls word selection by focusing on a subset of words that cumulatively make up a certain probability. Higher values make the output more predictable, while lower values increase randomness and creativity.
    max_tokens=10, #how many token model use for ouput 
    tool_choice="auto", #required mean tool calling required auto mean llm decide tool call none mean no tool call
    # frequency_penalty=0.9, #Reduces the likelihood of repeating the same words. Higher values penalize repeated tokens more strongly. (frequency_penalty is not available in gemini-2.0-flash model)
    presence_penalty= 0.9,  #Increases the likelihood of introducing new topics or words. A higher value encourages the model to mention new words or topics that weren’t previously mentioned.
    parallel_tool_calls=True, #Decides whether tool calls should be executed in parallel (at the same time) or sequentially (one after another).
    truncation = "auto", #  Controls whether and how the model’s output should be truncated.
    # metadata= {"name":"shiraz"}, # include extra information for model (metadata is not available in gemini-2.0-flash model)
    # store=True, #If set to True, it saves the generated model response for later use or retrieval.(store is not available in gemini-2.0-flash)
    include_usage=True, #If set to True, the model will include usage details like the number of tokens used.This helps you track resource consumption during the agent’s execution.

)



config = RunConfig(
    model=model,
    model_provider=cast(ModelProvider, external_client),
    tracing_disabled=True,
    model_settings=model_setting

)


panacloud_agent: Agent = Agent(
    name="panacloud_agent",
    instructions="You are helpful assistant",
    model=model,
)

response = Runner.run_sync(panacloud_agent, "who is founder of pakistan", run_config=config)
print(response)
print(response.final_output)
print(response.raw_responses)
