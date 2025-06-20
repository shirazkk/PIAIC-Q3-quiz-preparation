from agents.tracing import custom_span, trace, set_trace_processors, TracingProcessor, Span, Trace
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv
from typing import List

class PrintTraceProcessor(TracingProcessor):
    def on_trace_provider(self, trace_id: str, spans: List[Span]):
        print(f"[TRACE PROVIDER] trace_id: {trace_id}")
        for s in spans:
            print(f"  [Span] {s.span_id}: {s.span_data}")

    def on_span_start(self, span: Span):
        print(f"[SPAN START] {span.span_id}: {span.span_data}")

    def on_span_end(self, span: Span):
        print(f"[SPAN END] {span.span_id}: {span.span_data}")

    def on_trace_start(self, trace: Trace):
        print(f"[TRACE START] {trace.trace_id}")

    def on_trace_end(self, trace: Trace):
        print(f"[TRACE END] {trace.trace_id}")

    def force_flush(self):
        pass

    def shutdown(self):
        pass

set_trace_processors([PrintTraceProcessor()])



def simulate_tool():
    with custom_span("Tool Span"):
        print("Simulating tool execution...")

def simulate_guardrail():
    with custom_span("Guardrail Span"):
        print("Simulating guardrail check...")

def simulate_generation():
    with custom_span("Generation Span"):
        print("Simulating LLM generation...")

def main():
    with trace("Agent Run Trace"):
        print("Agent run started.")
        simulate_guardrail()
        simulate_tool()
        simulate_generation()
        print("Agent run finished.")

if __name__ == "__main__":
    main()


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


panacloud_agent: Agent = Agent(
    name="panacloud_agent",
    instructions="You are helpful assistant",
    model=model,
)

response = Runner.run_sync(panacloud_agent, "who is founder of pakistan", run_config=config)
print(response.final_output)


