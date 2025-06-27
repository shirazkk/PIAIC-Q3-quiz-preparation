# from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider
# from openai import AsyncOpenAI
# from typing import cast
# import os
# from dotenv import load_dotenv
# from agents.exceptions import MaxTurnsExceeded, AgentsException,ModelBehaviorError, UserError

# load_dotenv()
# set_tracing_disabled(disabled=True)

# # Load Gemini API Key
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set in .env")

# # Create Gemini model
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client,
# )

# # Define configuration with max_turns = 1 (so we can force the exception easily)
# config = RunConfig(
#     model=model,
#     model_provider=cast(ModelProvider, external_client),
#     tracing_disabled=True,
# )

# # max-turns-exceeded exception
# # class MaxTurnsExceeded(AgentsException):
# #     def max_turns(self):
# #         return f"[❌ MaxTurnsExceeded]"


# # model-behavior-error
# class UserError(AgentsException):
#     def model_error(self):
#         return f"ModelBehavior Error occur "




# # Define the agent
# panacloud_agent: Agent = Agent(
#     name="panacloud_agent",
#     instructions="You are a helpful assistant you call this tool to get output always `calculator_tool`",
#     model=model,
# )

# # Now run the agent with a very low max_turns limit
# try:
#     response = Runner.run_sync(
#         panacloud_agent,
#         input="hello i need a output of calculator_tool",
#         run_config=config,
#         tools = [calculator_tool]
#         # max_turns= 0 # 👈 Limit to 1 turn only to simulate exceeding turns
#     )
#     print(response.final_output)

# except UserError as mbr:
#     print(mbr)
