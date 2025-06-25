# from typing import List
# from agents import RunContextWrapper, FunctionToolResult, ToolsToFinalOutputResult
# from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, ModelProvider, function_tool, ModelSettings, AgentHooks, RunContextWrapper
# from openai import AsyncOpenAI
# from typing import Coroutine, cast, Any
# import os
# from dotenv import load_dotenv
# from pydantic import BaseModel

# # Load environment variables
# load_dotenv()

# # Fetch the Gemini API key
# gemini_api_key = os.getenv("GEMINI_API_KEY")

# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# # Initialize the external OpenAI client with the Gemini API
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# # Initialize the model
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client,
# )

# # Define the run configuration
# config = RunConfig(
#     model=model,
#     model_provider=cast(ModelProvider, external_client),
#     tracing_disabled=True,
# )

# # Define the response model for structured output
# class SupportResponse(BaseModel):
#     response: str

# # Define function tools
# @function_tool
# def add_task() -> str:
#     return "Your task has been added."

# @function_tool
# def check_due_date() -> str:
#     return "Due date is 7/12/2025."

# @function_tool
# def mark_complete() -> str:
#     return "Task has been completed!"



# async def custom_tools_to_final_output(
#     context: RunContextWrapper,
#     tool_results: List[FunctionToolResult]
# ) -> ToolsToFinalOutputResult:
#     # Process the tool results
#     combined_data = ""
#     for result in tool_results:
#         combined_data += result.output  # Assuming each result has an 'output' attribute

#     # Determine if the combined data is sufficient for a final output
#     if len(combined_data) > 100:  # Arbitrary condition for demonstration
#         return ToolsToFinalOutputResult(is_final_output=True, final_output=combined_data)
#     else:
#         return ToolsToFinalOutputResult(is_final_output=False)





# # Initialize the agent with tools, instructions, and hooks
# TaskAgent: Agent = Agent(
#     name="Task Agent",
#     instructions="Answer user task-related queries and call tools to get the final output.",
#     tools=[add_task, check_due_date, mark_complete],
#     tool_use_behavior=custom_tools_to_final_output,
#     model=model,
# )

# # Run the agent synchronously with a sample input
# response = Runner.run_sync(TaskAgent, "add task", run_config=config)

# # Print the final output from the agent
# print(response.final_output)







from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider,Handoff,RunContextWrapper, enable_verbose_stdout_logging, ModelSettings
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX




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
class User:
    name:str


def customer_support_instruction(context:RunContextWrapper[User],agent:Agent):
    return f" you are customer support agent which first greeting to user with his name {context.context.name} your task is to process user query if he ask about facebook password reset"

user = User(name="shiraz")

customer_support_agent:Agent[User] = Agent(
    name= "Customer Support Agent",
    instructions=customer_support_instruction,
    model = model,
)

panacloud_agent: Agent[User] = Agent(
    name="panacloud_agent",
    instructions="first greeting user with his name provided in context then if user question about customer support you deligate task to `customer_support_agent` if not about customer support you process it",
    model=model,
     model_settings= ModelSettings(
        # temperature=0.5,
        # top_p=0.4,
        frequency_penalty=1.0,

     ),
     tool_use_behavior=""
)

response = Runner.run_sync(
    panacloud_agent,
    "Can you tell me about your favorite hobby?",
    run_config=config,
    context=user
)
print(response.final_output)

