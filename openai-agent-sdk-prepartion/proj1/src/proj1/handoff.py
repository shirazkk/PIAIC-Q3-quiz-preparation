from agents import Agent, handoff, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider, ItemHelpers, RunContextWrapper
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

class EscalationData(BaseModel):
    reason: str


async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation agent called with reason: {input_data.reason}")

def input_filter(input_data):
    # Filter or modify input data as needed
    return input_data.strip()

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
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

# def on_handoff(context: RunContextWrapper[None]):
#     print("Handoff called")



# Math Agent (Handles math-related queries)
math_agent: Agent = Agent(
    name="Math Teacher",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} <You are a math teacher Answer the user's math-related> questions.""",
    model=model
)

# Physics Agent (Handles physics-related queries)
physics_agent: Agent = Agent(
    name="Physics Teacher",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} <You are a physics teacher. Answer the user's physics-related questions>.""",
    model=model
)

# Create handoff objects for each agent
math_handoff = handoff(
    agent=math_agent,
    on_handoff=on_handoff,
    input_type=EscalationData,
    tool_name_override= "me_math_agent_ko_transfer_kr_raha_ho",
)

physics_handoff = handoff(
    agent=physics_agent,
    on_handoff=on_handoff,
    input_type=EscalationData,
    tool_name_override= "me_physics_agent_ko_transfer_kr_raha_ho",

)

# Triage Agent (Handles the classification and handoff of math and physics questions)
async def TriageAgent():
    triage_agent: Agent = Agent(
        name="Triage Agent",
        instructions=(
            "You are a triage agent that routes questions to the appropriate specialist. "
            "For math questions, use the math_agent. For physics questions, use the physics_agent. "
            "If the question is not related to either physics or math, handle it yourself. "
            "Be precise in your classification to ensure questions go to the right specialist."
        ),
        handoffs=[math_handoff, physics_handoff],
        model=model,
    )

    # Simulate input query for the Triage Agent (Could be either Math or Physics related)
    user_query = """What is the Heisenberg Uncertainty Principle and how does it 
 affect the measurement of a particle's position and momentum?"""

    # Use the Triage Agent to process the query
    response =  Runner.run_streamed(triage_agent, user_query, run_config=config)

    # Stream events and print relevant progress
    async for event in response.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent Name: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "handoff_call_item":
                print(f"handoff occured : {event.item.agent.handoffs[0].tool_name}")
            elif event.item.type == "message_output_item":
                print(f"Final response: {ItemHelpers.text_message_output(event.item)}")  # Final response
            else:
                pass





# Main function to run the Triage Agent
def main():
    asyncio.run(TriageAgent())

if __name__ == "__main__":
    main()
