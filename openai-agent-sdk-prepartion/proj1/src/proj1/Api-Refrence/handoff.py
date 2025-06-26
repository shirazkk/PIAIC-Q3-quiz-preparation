from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider, Handoff, RunContextWrapper
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from agents.handoffs import HandoffInputData

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
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

# This will log when a handoff is done
def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
    agent_name = agent.name
    print("--------------------------------")
    print(f"Handing off to {agent_name}...")
    print("--------------------------------")
    # You can log additional context information here if needed
    # print(f"Context {ctx.usage}")
    # print(f"Context {ctx.context}")

# Custom filter to modify input data before handing off
class MyHandoffInputFilter(HandoffInputData):
    def __call__(self, input_data: str) -> str:
        # Example: capitalize the first letter
        filtered_input = input_data.capitalize()
        print(f"Filtered Input: {filtered_input}")  # Log the filtered input
        return filtered_input

# Create Spanish Agent
spanish_agent: Agent = Agent(
    name="Spanish Agent",
    instructions="You are a Spanish agent. You can answer in Spanish language only.",
    model=model
)

# Create Turkish Agent
turkish_agent: Agent = Agent(
    name="Turkish Agent",
    instructions="You are a Turkish agent. You can answer in Turkish language only.",
    model=model
)

# Main agent with handoff logic
panacloud_agent: Agent = Agent(
    name="panacloud_agent",
    instructions="If the question is in Spanish, delegate it to the Spanish Agent. If the question is in Turkish, delegate it to the Turkish Agent. If the question is in any other language, you handle that task and respond to the user.",
    handoffs=[
        Handoff(
            agent_name=spanish_agent,
            input_filter= MyHandoffInputFilter(),
            # on_handoff = lambda context: on_handoff(spanish_agent,ctx=context)
        ),
        Handoff(
            agent_name=spanish_agent,
            input_filter= MyHandoffInputFilter(),
            # on_handoff = lambda context: on_handoff(spanish_agent,ctx=context)
        )
    ],
    model=model,
)

# Running the main agent with a Spanish input
response = Runner.run_sync(panacloud_agent, "¿Quién es el fundador de Pakistán?", run_config=config)
print(response.final_output)

# You can also print the last agent to see which one was used to respond
# print(f"Last Agent: {response.last_agent.name}")
