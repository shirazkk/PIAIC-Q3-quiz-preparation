from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider, trace
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryRequest(BaseModel):
    prompt: str

class StoryResponse(BaseModel):
    outline: str
    story: str

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
            # Generate outline
            story_outline = await Runner.run(story_outline_agent, request.prompt, run_config=config)
            outline_text = story_outline.final_output

            # Check outline
            outline_checker = await Runner.run(
                outline_checker_agent,
                outline_text,
                run_config=config
            )
            assert isinstance(outline_checker.final_output, OutlineCheckerOutput)
            if not outline_checker.final_output.good_quality:
                raise HTTPException(status_code=400, detail="Outline is not good quality. Please try a different prompt.")
            if not outline_checker.final_output.is_scifi:
                raise HTTPException(status_code=400, detail="Outline is not science fiction. Please try a different prompt.")

            # Generate story
            story_generate = await Runner.run(
                story_agent,
                outline_text,
                run_config=config
            )
            story_text = story_generate.final_output

            return StoryResponse(outline=outline_text, story=story_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 