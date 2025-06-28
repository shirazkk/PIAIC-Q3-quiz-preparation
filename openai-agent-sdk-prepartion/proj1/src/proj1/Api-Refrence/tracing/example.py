from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
    RunConfig,
    ModelProvider,
    set_trace_processors,
    function_tool,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    input_guardrail,
    output_guardrail,
    OutputGuardrailTripwireTriggered,
)
from agents.tracing import (
    TracingProcessor,
    Span,
    Trace,
)
from agents.handoffs import handoff
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import List, cast

# Load environment variables
load_dotenv()

# Set tracing disabled as we will use our custom tracing processor
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# External Gemini API client (simulate the external connection to Gemini model)
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Create the model instance using the external client
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=external_client
)

# Set run configuration with proper ModelProvider casting
config = RunConfig(
    model=model,
    model_provider=cast(ModelProvider, external_client),
    tracing_disabled=False  # Enable tracing
)

# Custom TracingProcessor that prints tracing information to console
class CustomTracingProcessor(TracingProcessor):
    def __init__(self):
        super().__init__()
        self.current_spans = []

    def on_trace_start(self, trace: Trace) -> None:
        print(f"🔍 [TRACE START] Trace ID: {trace.trace_id}")
        print(f"   📊 Starting new trace execution")

    def on_trace_end(self, trace: Trace) -> None:
        print(f"✅ [TRACE END] Trace ID: {trace.trace_id}")
        print(f"   📊 Trace execution completed")
        print(f"   📈 Total spans processed: {len(self.current_spans)}")
        self.current_spans.clear()

    def on_span_start(self, span: Span) -> None:
        print(f"📈 [SPAN START] Span ID: {span.span_id}")
        print(f"   📋 Span Data: {span.span_data}")
        self.current_spans.append(span)

    def on_span_end(self, span: Span) -> None:
        print(f"🏁 [SPAN END] Span ID: {span.span_id}")
        print(f"   📋 Span Data: {span.span_data}")
        # Remove span from current spans list
        if span in self.current_spans:
            self.current_spans.remove(span)

    def on_trace_provider(self, trace_id: str, spans: List[Span]) -> None:
        print(f"📊 [TRACE PROVIDER] Trace ID: {trace_id}")
        print(f"   📈 Spans in trace:")
        for span in spans:
            print(f"      - Span ID: {span.span_id}, Data: {span.span_data}")

    def force_flush(self) -> None:
        print("🔄 [FORCE FLUSH] Flushing all pending traces")

    def shutdown(self) -> None:
        print("🛑 [SHUTDOWN] Shutting down tracing processor")

# Initialize custom tracing processor
custom_processor = CustomTracingProcessor()

# Set the custom tracing processor
set_trace_processors([custom_processor])

# ================== TOOLS DEFINITION ==================

@function_tool
def calculate_math(expression: str) -> str:
    """Calculate mathematical expressions safely."""
    try:
        # Safe evaluation for basic math operations
        allowed_chars = set('0123456789+-*/(). ')
        if all(c in allowed_chars for c in expression):
            result = eval(expression)
            return f"Result: {expression} = {result}"
        else:
            return "Error: Only basic mathematical operations are allowed"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

@function_tool
def get_weather_info(city: str) -> str:
    """Get weather information for a city (simulated)."""
    weather_data = {
        "Islamabad": "Sunny, 25°C, Perfect weather for outdoor activities",
        "Karachi": "Humid, 32°C, Sea breeze expected in evening",
        "Lahore": "Partly cloudy, 28°C, Good for sightseeing",
        "Peshawar": "Clear skies, 30°C, Hot but pleasant",
        "Quetta": "Cool, 18°C, Mountain air, very refreshing"
    }
    return weather_data.get(city, f"Weather data not available for {city}")

@function_tool
def get_pakistan_history(figure: str) -> str:
    """Get historical information about Pakistani figures."""
    history_data = {
        "Quaid-e-Azam": "Muhammad Ali Jinnah (1876-1948) was the founder of Pakistan. He led the Pakistan Movement and became the first Governor-General of Pakistan.",
        "Allama Iqbal": "Sir Muhammad Iqbal (1877-1938) was a poet, philosopher, and politician who inspired the Pakistan Movement with his poetry and vision.",
        "Liaquat Ali Khan": "Liaquat Ali Khan (1895-1951) was Pakistan's first Prime Minister and a close associate of Quaid-e-Azam.",
        "Fatima Jinnah": "Fatima Jinnah (1893-1967) was the sister of Quaid-e-Azam and known as 'Mother of the Nation' for her role in Pakistan's independence."
    }
    return history_data.get(figure, f"Historical information not available for {figure}")

# ================== GUARDRAIL OUTPUT MODELS ==================

class MathCheckOutput(BaseModel):
    is_math: bool
    reason: str

class ContentSafetyOutput(BaseModel):
    is_safe: bool
    reason: str

class HistoryCheckOutput(BaseModel):
    is_history: bool
    reason: str

# ================== GUARDRAIL AGENTS ==================

# Guardrail agent to check if input contains math
math_check_agent = Agent(
    name="MathCheckAgent",
    instructions="Check if the user input contains mathematical expressions or calculations. Return true if it's math-related, false otherwise.",
    output_type=MathCheckOutput,
    model=model
)

# Guardrail agent to check content safety
safety_check_agent = Agent(
    name="SafetyCheckAgent", 
    instructions="Check if the user input is safe and appropriate. Return true if it's safe, false if it contains inappropriate content.",
    output_type=ContentSafetyOutput,
    model=model
)

# Guardrail agent to check if input is history-related
history_check_agent = Agent(
    name="HistoryCheckAgent",
    instructions="Check if the user input is asking about Pakistani history or historical figures. Return true if it's history-related, false otherwise.",
    output_type=HistoryCheckOutput,
    model=model
)

# ================== GUARDRAIL FUNCTIONS ==================

@input_guardrail
def math_input_guardrail(context: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:
    """Guardrail to check if input contains math and redirect to math specialist."""
    # For now, we'll use a simple check instead of running the agent
    math_keywords = ["calculate", "math", "equation", "solve", "+", "-", "*", "/", "="]
    is_math = any(keyword in input.lower() for keyword in math_keywords)
    return GuardrailFunctionOutput(
        output_info=f"Math check: {is_math}",
        tripwire_triggered=is_math
    )

@input_guardrail
def safety_input_guardrail(context: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:
    """Guardrail to check if input is safe and appropriate."""
    # Simple safety check
    inappropriate_words = ["inappropriate", "unsafe", "harmful"]
    is_safe = not any(word in input.lower() for word in inappropriate_words)
    return GuardrailFunctionOutput(
        output_info=f"Safety check: {is_safe}",
        tripwire_triggered=not is_safe
    )

@input_guardrail
def history_input_guardrail(context: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:
    """Guardrail to check if input is history-related and redirect to history specialist."""
    # Simple history check
    history_keywords = ["history", "quaid", "iqbal", "jinnah", "pakistan", "independence", "founder"]
    is_history = any(keyword in input.lower() for keyword in history_keywords)
    return GuardrailFunctionOutput(
        output_info=f"History check: {is_history}",
        tripwire_triggered=is_history
    )

# ================== AGENTS DEFINITION ==================

# 1. Math Specialist Agent
math_agent = Agent(
    name="MathSpecialist",
    instructions="""
    You are a mathematical specialist agent. Your expertise is in:
    - Mathematical calculations and problem solving
    - Explaining mathematical concepts
    - Providing step-by-step solutions
    
    Use the calculate_math tool for computations.
    Always explain your reasoning and show your work.
    """,
    model=model,
    tools=[calculate_math],
    input_guardrails=[safety_input_guardrail]
)

# 2. History Specialist Agent
history_agent = Agent(
    name="HistorySpecialist",
    instructions="""
    You are a Pakistani history specialist agent. Your expertise is in:
    - Pakistani history and historical figures
    - Independence movement and founding fathers
    - Cultural and historical significance
    
    Use the get_pakistan_history tool for historical information.
    Provide detailed, accurate historical context.
    """,
    model=model,
    tools=[get_pakistan_history],
    input_guardrails=[safety_input_guardrail]
)

# 3. Main Coordinator Agent (Original agent enhanced)
panacloud_agent = Agent(
    name="panacloud_agent",
    instructions="""
    You are a helpful coordinator assistant that can:
    - Answer general questions about Pakistan
    - Coordinate with specialist agents for specific tasks
    - Provide weather information using tools
    
    When you receive:
    - Mathematical questions → Hand off to MathSpecialist
    - Historical questions about Pakistani figures → Hand off to HistorySpecialist
    - Weather questions → Use the weather tool yourself
    - General questions → Answer directly
    
    Always be helpful and informative.
    """,
    model=model,
    tools=[get_weather_info],
    handoffs=[
        handoff(agent=math_agent),
        handoff(agent=history_agent)
    ],
    input_guardrails=[safety_input_guardrail]
)

# Function to demonstrate the multi-agent system with tracing
def run_multi_agent_demo():
    """Run demonstrations of the multi-agent system with different scenarios."""
    print("🤖 Multi-Agent System with Tools, Handoffs, and Guardrails Demo")
    print("=" * 80)
    
    scenarios = [
        {
            "name": "Math Question",
            "input": "Calculate (15 + 7) * 3 and explain the steps",
            "description": "This will trigger handoff to MathSpecialist agent"
        },
        {
            "name": "History Question", 
            "input": "Tell me about Quaid-e-Azam and his role in Pakistan's creation",
            "description": "This will trigger handoff to HistorySpecialist agent"
        },
        {
            "name": "Weather Question",
            "input": "What's the weather like in Islamabad today?",
            "description": "This will be handled by the main agent using tools"
        },
        {
            "name": "General Question",
            "input": "What is the capital of Pakistan and why is it important?",
            "description": "This will be handled directly by the main agent"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n🔍 Scenario {i}: {scenario['name']}")
        print(f"📝 Description: {scenario['description']}")
        print(f"💬 Input: {scenario['input']}")
        print("-" * 60)
        
        try:
            result = Runner.run_sync(
                panacloud_agent,
                scenario['input'],
                run_config=config
            )
            
            print(f"✅ Response: {result.final_output}")
            print("=" * 60)
            
        except InputGuardrailTripwireTriggered as e:
            print(f"🛡️ Input Guardrail Triggered: {e}")
            print("=" * 60)
        except OutputGuardrailTripwireTriggered as e:
            print(f"🛡️ Output Guardrail Triggered: {e}")
            print("=" * 60)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("=" * 60)

# Function to demonstrate the agent with tracing
def run_agent_with_tracing():
    """Run the agent and demonstrate custom tracing output."""
    print("🤖 Starting agent execution with custom tracing...")
    print("=" * 60)
    
    try:
        # Run the agent with tracing enabled
        result = Runner.run_sync(
            panacloud_agent, 
            "Who is the founder of Pakistan? Please provide a brief answer.", 
            run_config=config
        )
        
        print("=" * 60)
        print(f"💬 Agent Response: {result.final_output[:150]}")
        print("✅ Agent execution completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during agent execution: {e}")

# Test function to verify tracing processor works
def test_tracing_processor():
    """Test the custom tracing processor without running the agent."""
    print("🧪 Testing Custom Tracing Processor...")
    print("=" * 60)
    
    # Create a test span class that implements all required methods
    class TestSpan(Span):
        def __init__(self):
            self._span_id = "test_span_456"
            self._span_data = {"operation": "test"}
            self._trace_id = "test_trace_123"
            self._parent_id = None
            self._started_at = None
            self._ended_at = None
            self._error = None
            
        @property
        def span_id(self) -> str:
            return self._span_id
            
        @property
        def span_data(self) -> dict:
            return self._span_data
            
        @property
        def trace_id(self) -> str:
            return self._trace_id
            
        @property
        def parent_id(self) -> str | None:
            return self._parent_id
            
        @property
        def started_at(self) -> float | None:
            return self._started_at
            
        @property
        def ended_at(self) -> float | None:
            return self._ended_at
            
        @property
        def error(self) -> str | None:
            return self._error
            
        def start(self) -> None:
            import time
            self._started_at = time.time()
            
        def finish(self) -> None:
            import time
            self._ended_at = time.time()
            
        def set_error(self, error: str) -> None:
            self._error = error
            
        def export(self) -> dict:
            return {
                "span_id": self._span_id,
                "span_data": self._span_data,
                "trace_id": self._trace_id,
                "parent_id": self._parent_id,
                "started_at": self._started_at,
                "ended_at": self._ended_at,
                "error": self._error
            }
            
        def __enter__(self):
            self.start()
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                self.set_error(str(exc_val))
            self.finish()
    
    # Create a test trace class
    class TestTrace(Trace):
        def __init__(self):
            self._trace_id = "test_trace_123"
            
        @property
        def trace_id(self) -> str:
            return self._trace_id
            
        def __enter__(self):
            return self
            
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    
    # Test trace start
    print("Testing trace start...")
    test_trace = TestTrace()
    custom_processor.on_trace_start(test_trace)
    
    # Test span start
    print("\nTesting span start...")
    test_span = TestSpan()
    custom_processor.on_span_start(test_span)
    
    # Test span end
    print("\nTesting span end...")
    custom_processor.on_span_end(test_span)
    
    # Test trace end
    print("\nTesting trace end...")
    custom_processor.on_trace_end(test_trace)
    
    print("=" * 60)
    print("✅ Tracing processor test completed!")

# Run the demonstration
if __name__ == "__main__":
    
    # Run the multi-agent system demo
    run_multi_agent_demo()
    test_tracing_processor()
    
    # Uncomment the line below to run the original single agent demo
    # run_agent_with_tracing()
