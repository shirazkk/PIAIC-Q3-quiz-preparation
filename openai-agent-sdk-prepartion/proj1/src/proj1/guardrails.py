from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider, RunContextWrapper, GuardrailFunctionOutput, TResponseInputItem,input_guardrail,InputGuardrailTripwireTriggered
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

class Country(BaseModel):
    israel:bool
    reason:str

guardial_agent: Agent= Agent(
     name= "Guardial Agent",
     instructions= "Check user is asking about Israel?",
     output_type=Country,
     model= model

)

@input_guardrail
async def country_guardial(ctx:RunContextWrapper[Country], agent:Agent, input:str | list[TResponseInputItem])->GuardrailFunctionOutput:
     result = await Runner.run(guardial_agent, input,context=ctx.context, run_config=config)
     return GuardrailFunctionOutput(
          output_info = result.final_output,
          tripwire_triggered= result.final_output.israel
     )

panacloud_agent: Agent = Agent(
    name="panacloud_agent",
    instructions= "You are a helpful assistant",
    input_guardrails=[country_guardial],
    model=model,
)
try:
    result = Runner.run_sync(panacloud_agent, "israel is country?", run_config=config)
    print(result.final_output)

except InputGuardrailTripwireTriggered:
    print(f"Error: We Dont recognize israel as a county")


