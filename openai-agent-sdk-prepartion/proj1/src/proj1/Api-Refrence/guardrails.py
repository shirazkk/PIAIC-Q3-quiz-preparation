
from agents import(
    Agent,
    Runner,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
    RunConfig,
    ModelProvider,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
    OutputGuardrailTripwireTriggered,
)
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from pydantic import BaseModel

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

class MessageOutput(BaseModel): 
    response: str


class MathOutput(BaseModel):
    is_math:bool
    reason:str



# guardial_agent:Agent = Agent(
#     name="Guardial Check",
#     instructions= "Check if the user is asking you about only Agentic Ai questions",
#     output_type= AgenticAi,
#     model=model
# )

guardial_agent:Agent = Agent(
    name="Guardial Check",
    instructions= "Check if the output includes any math",
    output_type= MathOutput,
    model=model
)


# @input_guardrail
# async def ai_guardial(context:RunContextWrapper[None], agent:Agent,input:str)-> GuardrailFunctionOutput:
#     response = await Runner.run(guardial_agent,input,context=context.context ,run_config=config)
#     return GuardrailFunctionOutput(
#         output_info=response.final_output,
#         tripwire_triggered=not response.final_output.agentic_ai
#     )


@output_guardrail
async def math_guardrail(context:RunContextWrapper[None], agent:Agent,input:str)-> GuardrailFunctionOutput:
    response = await Runner.run(guardial_agent,input=input,context=context.context,run_config=config)
    return GuardrailFunctionOutput(
        output_info=response.final_output,
        tripwire_triggered = response.final_output.is_math
    )

async def main():
    try:
        # panacloud_agent: Agent = Agent(
        #     name="panacloud_agent",
        #     instructions="You are a Agentic Ai specialist. You help user with Agentic Ai quaries",
        #     model=model,
        #     input_guardrails=[ai_guardial]
        # )
        panacloud_agent: Agent = Agent(
            name="Customer support agent",
            instructions="You are a customer support agent. You help customers with their questions.",
            output_guardrails=[math_guardrail],
            model=model,
        )

        response = await  Runner.run(panacloud_agent, "Hello, can you help me solve for x: 2x + 3 = 11?", run_config=config)
        print(response.final_output)

    except OutputGuardrailTripwireTriggered:
        print("output guardial triggred")


import asyncio
asyncio.run(main())