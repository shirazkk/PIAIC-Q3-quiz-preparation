from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider,trace
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

story_outline_agent = Agent(
    name="story_outline_agent",
    instructions="Generate a very short story outline based on the user's input.",
)


class OutlineCheckerOutput(BaseModel):
    good_quality: bool
    is_scifi: bool


outline_checker_agent = Agent(
    name="outline_checker_agent",
    instructions="Read the given story outline, and judge the quality. Also, determine if it is a scifi story.",
    output_type=OutlineCheckerOutput,
)

story_agent = Agent(
    name="story_agent",
    instructions="Write a short story based on the given outline.",
    output_type=str,
)


async def main():
    input_prompt = input("What kind of story do you want? ")

    print("\n================ STORY GENERATION FLOW ================\n")
    with trace("Deterministic story flow"):
        print("[1] Generating story outline...\n")
        story_outline = await Runner.run(story_outline_agent, input_prompt , run_config=config)
        print("--- Story Outline Generated ---")
        print(story_outline.final_output)
        print("\n======================================================\n")

        print("[2] Checking outline quality and genre...\n")
        outline_checker = await Runner.run(
            outline_checker_agent,
            story_outline.final_output,
            run_config=config
        )

        assert isinstance(outline_checker.final_output, OutlineCheckerOutput)
        if not outline_checker.final_output.good_quality:
            print("[!] Outline is NOT good quality. Re generating story ouline.\n")
            exit(0)
        if not outline_checker.final_output.is_scifi:
            print("[!] Outline is NOT science fiction. Stopping execution.\n")
            exit(0)
        
        print("[✓] Outline is good quality and a science fiction story. Proceeding to story generation.\n")
        print("======================================================\n")

        print("[3] Generating the full story...\n")
        story_generate = await Runner.run(
            story_agent,
            story_outline.final_output ,
            run_config=config
        )

        print("--- Story Generated ---\n")
        print(story_generate.final_output)
        print("\n==================== END OF FLOW =====================\n")
        print("Story generation complete!\n")

import asyncio
asyncio.run(main())