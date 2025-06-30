from agents import Agent, Runner, Span, Trace, OpenAIChatCompletionsModel, RunConfig, ModelProvider
from openai import AsyncOpenAI
from typing import cast, Any
import os
from dotenv import load_dotenv
from agents.tracing import TracingProcessor,set_trace_processors, trace
from pprint import pprint

load_dotenv()

# set_tracing_disabled(disabled=True)  # Comment out to enable tracing

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
    tracing_disabled=False,
)


class LocalTraceProcessor(TracingProcessor):
    def __init__(self):
        self.traces = []
        self.spans = []

    def on_trace_start(self, trace: Trace) -> None:
        self.traces.append(trace)
        print("=" * 50)
        print("🔍 TRACE STARTED")
        print("=" * 50)
        print(f"Trace ID: {trace.trace_id}")
        print(f"Trace Start Time: {trace.start()}")
        print("=" * 50)

    def on_trace_end(self, trace: Trace) -> None:
        print("=" * 50)
        print("🏁 TRACE ENDED")
        print("=" * 50)
        print(f"Trace ID: {trace.trace_id}")
        print("Trace Export Data:")
        pprint(trace.export())
        print("=" * 50)

    def on_span_start(self, span: Span[Any]) -> None:
        self.spans.append(span)
        print("-" * 40)
        print("📊 SPAN STARTED")
        print("-" * 40)
        print(f"Span ID: {span.span_id}")
        print(f"Span Start Time: {span.start()}")
        print("-" * 40)

    def on_span_end(self, span: Span[Any]) -> None:
        print("-" * 40)
        print("✅ SPAN ENDED")
        print("-" * 40)
        print(f"Span ID: {span.span_id}")
        print("Span Export Data:")
        pprint(span.export())
        print("-" * 40)

    def force_flush(self):
        print("🔄 FORCING FLUSH OF TRACE DATA")
        print(f"Total traces collected: {len(self.traces)}")
        print(f"Total spans collected: {len(self.spans)}")

    def shutdown(self) -> None:
        print("=" * 60)
        print("🛑 SHUTTING DOWN TRACE PROCESSOR")
        print("=" * 60)
        
        print(f"\n📋 SUMMARY:")
        print(f"Total Traces Collected: {len(self.traces)}")
        print(f"Total Spans Collected: {len(self.spans)}")
        
        print(f"\n📊 COLLECTED TRACES:")
        for i, trace in enumerate(self.traces, 1):
            print(f"\n--- Trace {i} ---")
            pprint(trace.export())
            
        print(f"\n📊 COLLECTED SPANS:")
        for i, span in enumerate(self.spans, 1):
            print(f"\n--- Span {i} ---")
            pprint(span.export())
            
        print("=" * 60)

local_processor = LocalTraceProcessor()
set_trace_processors([local_processor])

print("🚀 Starting tracing demonstration...")
print("Initial traces:", len(local_processor.traces))
print("Initial spans:", len(local_processor.spans))
print("=" * 60)

async def main():
    panacloud_agent: Agent = Agent(
        name="panacloud_agent",
        instructions="You are helpful assistant",
        model=model,
    )
    with trace("Example_flow"):
        first_result = await Runner.run(panacloud_agent, "Start the task")
        second_result = await Runner.run(panacloud_agent, f"Rate this result: {first_result.final_output}")
        print(f"Result: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

import asyncio
asyncio.run(main())
