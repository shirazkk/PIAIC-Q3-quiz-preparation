from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, ModelProvider,function_tool, RunContextWrapper
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from typing import cast
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from pydantic import BaseModel
import asyncio

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

@dataclass
class UserContext:
    name:str
    is_premium:bool


class SupportResponse(BaseModel):
    response:str
    


@function_tool
def get_product_info(product: str) -> str:
    return f"{product} has a 1-year warranty."

@function_tool
def check_order_status(order_id: str) -> str:
    return f"Order {order_id} is shipped."

@function_tool
def process_refund(order_id: str) -> str:
    return f"Refund for order {order_id} processed."


ProductAgent: Agent = Agent(
    name="ProductAgent",
    instructions="Answer product-related questions using get_product_info. For queries like 'Provide general product information' or unspecified products, use 'laptop' as the default product. Return the response as a JSON string: {\"response\": \"<tool_output>\"}.",
    tools=[get_product_info],
    model=model
)

OrderAgent: Agent = Agent(
    name="OrderAgent",
    instructions="Handle order status queries using check_order_status. If no order_id is provided, use '#123' as the default. Return the response as a JSON string: {\"response\": \"<tool_output>\"}.",
    tools=[check_order_status],
    model=model
)

RefundAgent: Agent = Agent(
    name="RefundAgent",
    instructions="Process refund requests using process_refund. If no order_id is provided, use '#123' as the default. Return the response as a JSON string: {\"response\": \"<tool_output>\"}.",
    tools=[process_refund],
    model=model
)

def triage_instruction(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    return f"""You are assisting {context.context.name}. Your role is to delegate tasks to specialized agents:
- For product-related questions or explicit requests to hand off to ProductAgent (e.g., 'I handoff to product agent'), hand off to ProductAgent with the input 'Provide general product information' if no specific product is mentioned.
- For order status queries, hand off to OrderAgent.
- For refund requests, hand off to RefundAgent.
Ensure the handoff includes a clear input for the target agent."""

user_context = UserContext(name="Shiraz Ali", is_premium=True)

async def main():
    triageagent:Agent = Agent[UserContext](
        name= "Triage agent",
        instructions= triage_instruction,
        handoffs=[ProductAgent,OrderAgent,RefundAgent],
        model=model
    )


    response =  Runner.run_streamed(triageagent, "process refund requests?", run_config=config ,context=user_context)
    async for event in response.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())