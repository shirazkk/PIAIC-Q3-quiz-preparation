from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, ModelProvider, function_tool, ModelSettings, AgentHooks, RunContextWrapper
from openai import AsyncOpenAI
from typing import Coroutine, cast, Any
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Fetch the Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Initialize the external OpenAI client with the Gemini API
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Initialize the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Define the run configuration
config = RunConfig(
    model=model,
    model_provider=cast(ModelProvider, external_client),
    tracing_disabled=True,
    model_settings=ModelSettings(tool_choice="add_task")  # Force tool use for "add_task"
)

# Define the response model for structured output
class SupportResponse(BaseModel):
    response: str

# Define function tools
@function_tool
def add_task() -> str:
    return "Your task has been added."

@function_tool
def check_due_date() -> str:
    return "Due date is 7/12/2025."

@function_tool
def mark_complete() -> str:
    return "Task has been completed!"

# Define custom hooks for logging agent actions
class TaskManagementHook(AgentHooks):
    def on_start(self, context: RunContextWrapper[Any], agent: Agent[Any]):
        print(f"[HOOK] Agent {agent.name} started with input: {context.context}")

    def on_tool_call(self, agent: Agent[Any], tool_name: str, tool_input: Any):
        print(f"[HOOK] Agent {agent.name} called tool {tool_name} with input: {tool_input}")

# Initialize the agent with tools, instructions, and hooks
TaskAgent: Agent = Agent(
    name="Task Agent",
    instructions="Answer user task-related queries and call tools to get the final output.",
    tools=[add_task, check_due_date, mark_complete],
    model=model,
    hooks=TaskManagementHook()  # Attach the custom hooks
)

# Run the agent synchronously with a sample input
response = Runner.run_sync(TaskAgent, "add task", run_config=config)

# Print the final output from the agent
print(response.final_output)
