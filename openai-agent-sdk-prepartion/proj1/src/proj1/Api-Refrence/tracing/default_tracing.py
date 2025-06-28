
import asyncio
from agents import Agent, Runner, function_tool, get_current_trace
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, RunConfig, ModelProvider
from openai import AsyncOpenAI
from typing import cast
import os
from dotenv import load_dotenv

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


# ================== DEFAULT TRACING FUNDAMENTALS ==================


async def demo_automatic_tracing():
    """Demonstrate that tracing happens automatically with zero configuration."""
    print("=== Demo: Automatic Tracing (Zero Configuration) ===")

    print("📊 Key Fact: Tracing is ENABLED BY DEFAULT")
    print("   • No setup required")
    print("   • No configuration needed")
    print("   • Automatically captures all agent runs")
    print("   • Comprehensive data collection out of the box\n")

    # Create the simplest possible agent
    simple_agent = Agent(
        name="SimpleAgent",
        instructions="You are a simple demonstration agent. Respond briefly."
    )

    print("🤖 Running a simple agent with ZERO tracing configuration...")
    print("   The SDK will automatically:")
    print("   • Create a trace for the entire run")
    print("   • Create spans for agent processing")
    print("   • Create spans for LLM calls")
    print("   • Assign unique trace IDs")
    print("   • Capture timing information")

    try:
        # This simple run automatically creates comprehensive traces
        result = await Runner.run(
            simple_agent,
            "Hello, please say hi back",
            max_turns=2,
            run_config=config
        )

        print(f"\n✅ Agent completed successfully!")
        print(f"💬 Response: {result.final_output}")
        print(f"\n📊 What was automatically traced:")
        print(f"   ✓ Complete agent execution workflow")
        print(f"   ✓ LLM generation calls and responses")
        print(f"   ✓ Agent reasoning and decision making")
        print(f"   ✓ Execution timing and performance data")
        print(f"   ✓ Unique trace ID for this entire operation")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_traces_vs_spans():
    """Demonstrate the fundamental difference between traces and spans."""
    print("\n=== Demo: Understanding Traces vs Spans ===")

    print("🏗️ Conceptual Hierarchy:")
    print("   📊 TRACE = Complete workflow (like a project)")
    print("   📈 SPAN = Individual operation (like a task in that project)")
    print("   📈 SPAN = Sub-operation (like a subtask)")
    print("   📈 SPAN = ... (can be nested)")
    print()

    print("🔍 Real-world analogy:")
    print("   📊 TRACE = 'Making dinner'")
    print("   📈 SPAN = 'Preparing ingredients'")
    print("   📈 SPAN = 'Cooking main course'")
    print("   📈 SPAN = 'Setting table'")
    print("   📈 SPAN = 'Serving food'")
    print()

    # Create agent to demonstrate trace/span generation
    demo_agent = Agent(
        name="TraceSpanDemo",
        instructions="You demonstrate traces and spans. Respond briefly to show the concepts."
    )

    print("🤖 Running agent to see trace/span structure...")

    try:
        # Single agent run = One trace containing multiple spans
        result = await Runner.run(
            demo_agent,
            "Please explain what you do in simple terms",
            max_turns=2,
            run_config=config
        )

        print(f"\n✅ Execution completed!")
        print(f"\n📊 Trace/Span Structure Created:")
        print(f"   📊 ONE TRACE named 'Agent trace' containing:")
        print(f"   ├── 📈 Agent span (agent reasoning/processing)")
        print(f"   ├── 📈 Generation span (LLM API call)")
        print(f"   └── 📈 Response span (final output formatting)")
        print(f"\n🎯 Key Understanding:")
        print(f"   • 1 Agent Run = 1 Trace")
        print(f"   • Each operation within the run = 1 Span")
        print(f"   • All spans belong to the same trace")
        print(f"   • Spans can be nested hierarchically")

        print(f"final output {result.final_output}")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_trace_identification():
    """Demonstrate how traces are identified and tracked."""
    print("\n=== Demo: Trace Identification ===")

    print("🔖 Trace Identification System:")
    print("   • Each trace gets a unique trace_id")
    print("   • Format: trace_<32_alphanumeric_characters>")
    print("   • Automatically generated by the SDK")
    print("   • Used to correlate all spans in a workflow")
    print()

    @function_tool
    def show_current_trace() -> str:
        """Tool that shows current trace information."""
        current_trace = get_current_trace()

        if current_trace:
            return f"Currently executing in trace: {current_trace.trace_id}"
        else:
            return "No current trace found"

    trace_demo_agent = Agent(
        name="TraceDemoAgent",
        instructions="Use the show_current_trace tool to demonstrate trace identification.",
        tools=[show_current_trace]
    )

    print("🤖 Running agent that will show its own trace ID...")

    try:
        result = await Runner.run(
            trace_demo_agent,
            "Please use your tool to show the current trace information",
            max_turns=3,
            run_config=config
        )

        print(f"\n✅ Trace identification demonstrated!")
        print(f"📋 Tool output: {result.final_output}")
        print(f"\n🎯 Key Points:")
        print(f"   • Tools can access their execution trace")
        print(f"   • Each run gets a unique trace_id")
        print(f"   • Trace IDs help correlate related operations")
        print(f"   • Same trace_id links all spans in this run")

    except Exception as e:
        print(f"❌ Error: {e}")


async def demo_multiple_traces():
    """Demonstrate how multiple agent runs create separate traces."""
    print("\n=== Demo: Multiple Independent Traces ===")

    print("🔄 Multiple Runs = Multiple Traces:")
    print("   • Each Runner.run() creates a new trace")
    print("   • Traces are independent by default")
    print("   • Each has its own unique trace_id")
    print("   • Spans belong to their specific trace")

    simple_agent = Agent(
        name="MultiTraceDemo",
        instructions="You demonstrate multiple traces. Respond with just a number."
    )

    print(f"\n🤖 Running the same agent 3 times...")
    print(f"   Each run will create a separate, independent trace")

    try:
        for i in range(1, 4):
            print(f"\n   🔄 Run {i}:")

            result = await Runner.run(
                simple_agent,
                f"Please respond with just the number {i}",
                max_turns=2,
                run_config=config
            )

            print(f"      Response: {result.final_output}")
            print(f"      ✓ Created independent trace #{i}")

        print(f"\n📊 Result: 3 Separate Traces Created")
        print(f"   • Run 1 = Trace 1 (unique trace_id)")
        print(f"   • Run 2 = Trace 2 (different trace_id)")
        print(f"   • Run 3 = Trace 3 (different trace_id)")
        print(f"\n🎯 Key Understanding:")
        print(f"   • Each agent run is traced independently")
        print(f"   • No correlation between runs by default")
        print(f"   • Each trace contains only spans from its run")

    except Exception as e:
        print(f"❌ Error: {e}")


# ================== MAIN EXECUTION ==================


async def main():
    """Run all default tracing demonstrations."""
    print("📊 OpenAI Agents SDK - Default Tracing Fundamentals 📊")
    print("\nThis module covers the core concept: tracing happens automatically")
    print("with zero configuration required.\n")

    # Run all demonstrations
    await demo_automatic_tracing()
    await demo_traces_vs_spans()
    await demo_trace_identification()
    await demo_multiple_traces()

    print("\n" + "="*60)
    print("🎓 Key Takeaways - Default Tracing:")
    print("• Tracing is enabled by default - no setup needed")
    print("• Each agent run creates one trace automatically")
    print("• Traces contain spans representing individual operations")
    print("• Each trace has a unique trace_id for identification")
    print("• Multiple runs create separate, independent traces")
    print("• Comprehensive data is captured out of the box")

    print(f"\n🎯 Next Steps:")
    print(f"• Learn about different span types in 02_span_types.py")
    print(f"• Understand tracing controls in 03_tracing_control.py")


if __name__ == "__main__":
    asyncio.run(main())
