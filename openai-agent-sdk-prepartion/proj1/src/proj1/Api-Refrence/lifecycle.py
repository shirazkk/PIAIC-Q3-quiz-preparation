from agents import Agent, RunConfig, RunContextWrapper, Runner,OpenAIChatCompletionsModel,ModelProvider,function_tool,AgentHooks ,FunctionTool ,RunHooks
from openai import AsyncOpenAI
from typing import cast, Any
from dotenv import load_dotenv
import os


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=cast(ModelProvider, external_client),
    tracing_disabled= True
)

# RunHooks: A class that handles lifecycle events for the entire agent run, allowing callbacks at different stages like agent start, end, handoffs, and tool usage.

class MyRunHook(RunHooks):

    async def on_agent_start(self,context:RunContextWrapper[Any],agent:Agent):
        print(f"{agent.name} started")

    async def on_handoff(self, context: RunContextWrapper[Any], from_agent: Agent[Any], to_agent: Agent[Any]) -> None:
        print(f"{from_agent.name} handoff to {to_agent.name}")  

    async def on_tool_start(self, context: RunContextWrapper[Any], agent: Agent[Any], tool: FunctionTool) -> None:
        print(f"{agent.name} call a tool {tool.name}") 

    async def on_tool_end(self, context: RunContextWrapper[Any], agent: Agent[Any], tool: FunctionTool ,result: str) -> None:
        print(f"{agent.name} call this tool {tool.name} with this output {result}")
     

    async def on_agent_end(self, context: RunContextWrapper[Any], agent: Agent[Any], output: Any) -> None:
        print(f"{agent.name} with this output {output} Ended")

    

# AgentHooks: A class that handles lifecycle events specific to a single agent, allowing callbacks for when the agent starts, ends, handles a handoff, or uses a tool.

class MyAgentHooks(AgentHooks):
    async def on_start(self, context, agent):
        print(f"[AgentHooks] {agent.name} started")

    async def on_end(self, context, agent, output):
        print(f"[AgentHooks] {agent.name} ended with: {output}")

    async def on_handoff(self, context, agent, source):
        print(f"[AgentHooks] {source.name} handed off to {agent.name}")

    async def on_tool_start(self, context, agent, tool):
        print(f"[AgentHooks] {agent.name} starting tool: {tool.name}")

    async def on_tool_end(self, context, agent, tool, result):
        print(f"[AgentHooks] {tool.name} ended with: {result}")

@function_tool
def captilize_letters(text:str):
    """Capitilize the response of llm"""
    return text.capitalize


@function_tool(
        name_override="Add_two_numbers",
        description_override="This tool add two numbers", )
def calculator(a,b):
    return a+b



spanish_agent: Agent = Agent(
    name="Spanish Agent",
    instructions="You are a Spanish agent. You can answer in Spanish language only.",
    model=model,
    tools=[captilize_letters]
)

# Create Turkish Agent
turkish_agent: Agent = Agent(
    name="Turkish Agent",
    instructions="You are a Turkish agent. You can answer in Turkish language only.",
    model=model,
    tools=[captilize_letters]
)

async def main():
    panacloud_agent: Agent = Agent(
        name="panacloud_agent",
        instructions="If the question is in Spanish, delegate it to the Spanish Agent. If the question is in Turkish, delegate it to the Turkish Agent. If the question is in any other language, you handle that task and respond to the user.",
        handoffs=[spanish_agent,turkish_agent],
        model=model,
        tools=[calculator],
        hooks= MyAgentHooks()
    )


    response = await Runner.run(panacloud_agent, "Pakistan'ın kurucusu kimdir? Cevabımı büyük harflerle istiyorum",run_config=config,hooks=MyRunHook())

    print(response.final_output)

import asyncio
asyncio.run(main())
