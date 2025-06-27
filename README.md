# PIAIC Exam Preparation Repository

A comprehensive collection of Python code examples and practice materials covering advanced Python topics for PIAIC (Presidential Initiative for Artificial Intelligence and Computing) exam preparation.

## 📚 Topics Covered

This repository contains practical examples and implementations for the following key areas:

### 1. 🧬 Python Generics
Advanced type hints and generic programming concepts with practical implementations.

**Key Features:**
- **Upper Bounds**: Type constraints with `TypeVar` and `bound` parameters
- **Result Wrapper**: Generic error handling with `OperationResult[T, E]`
- **API Response Wrapper**: Generic response structures
- **Caching System**: Type-safe caching implementations
- **Method Overloading**: Generic method implementations
- **Paging System**: Generic pagination utilities
- **Type Restrictions**: Advanced type constraint examples

**Files:**
- `generics/upper_bounds.py` - Type bounds and constraints
- `generics/result_wrapper.py` - Generic result handling
- `generics/api_response_wrapper.py` - API response structures
- `generics/caching_system.py` - Type-safe caching
- `generics/method-overload.py` - Method overloading examples
- `generics/pagingsystem.py` - Pagination utilities
- `generics/restric_type.py` - Type restrictions
- `generics/swap_two_values.py` - Generic value swapping

### 2. 📝 Markdown Documentation
Comprehensive markdown syntax examples and best practices.

**Content:**
- Basic and extended markdown syntax
- Text formatting (bold, italic, strikethrough)
- Lists and nested lists
- Links and images
- Code blocks and inline code
- Tables and footnotes
- HTML integration
- Horizontal rules and headers

**File:**
- `markdown/readm.md` - Complete markdown reference

### 3. 🤖 OpenAI Agent SDK
Advanced AI agent implementations using OpenAI's Agent SDK.

**Features:**
- **Task Management Agent**: Multi-tool agent with forced tool usage
- **Customer Support Agent**: Real-world customer service implementation
- **Context Management**: Advanced context handling and memory
- **Guardrails**: Safety and validation mechanisms
- **Handoff System**: Agent-to-agent transitions
- **Streaming**: Real-time response streaming
- **Tracing**: Debugging and monitoring capabilities
- **Tools Integration**: Custom tool implementations

**Key Components:**
- `agent.py` - Base agent implementation
- `task_manager.py` - Task management system
- `customer_support_agent.py` - Customer service agent
- `Context management.py` - Context handling
- `guardrails.py` - Safety mechanisms
- `handoff.py` - Agent handoff logic
- `streaming.py` - Streaming responses
- `tracing.py` - Debugging and monitoring
- `tools.py` - Custom tool implementations
- `lifecycle.py` - agent lifecycle

### 4. 🛡️ Pydantic Data Validation
Comprehensive data validation and settings management using Pydantic.

**Examples Covered:**
- **Basic Models**: Simple data models with validation
- **Field Validation**: Custom validation rules and constraints
- **Nested Models**: Complex nested data structures
- **JSON Serialization**: Data serialization and parsing
- **Settings Management**: Environment-based configuration
- **Real-world Examples**: Blog post validation with custom validators

**Features:**
- Type validation and conversion
- Custom validators and field constraints
- Environment variable integration
- JSON serialization/deserialization
- Error handling with `ValidationError`
- Nested model relationships

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip or uv package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd piaic_exam_prepartion
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

### Running Examples

#### Generics Examples
```bash
cd generics
python upper_bounds.py
python result_wrapper.py
python api_response_wrapper.py
```

#### Pydantic Examples
```bash
cd pydantic
python main.py
```

#### OpenAI Agent SDK Examples
```bash
cd openai-agent-sdk-prepartion/proj1
python -m src.proj1.main
```

## 📁 Project Structure

```
piaic_exam_prepartion/
├── generics/                    # Python Generics examples
│   ├── upper_bounds.py         # Type bounds and constraints
│   ├── result_wrapper.py       # Generic result handling
│   ├── api_response_wrapper.py # API response structures
│   ├── caching_system.py       # Type-safe caching
│   ├── method-overload.py      # Method overloading
│   ├── pagingsystem.py         # Pagination utilities
│   ├── restric_type.py         # Type restrictions
│   └── swap_two_values.py      # Generic value swapping
├── markdown/                   # Markdown documentation
│   └── readm.md               # Complete markdown reference
├── openai-agent-sdk-prepartion/ # OpenAI Agent SDK examples
│   └── proj1/
│       └── src/proj1/
│           ├── agent.py              # Base agent
│           ├── task_manager.py       # Task management
│           ├── customer_support_agent.py # Customer service
│           ├── Context management.py # Context handling
│           ├── guardrails.py         # Safety mechanisms
│           ├── handoff.py            # Agent handoffs
│           ├── streaming.py          # Streaming responses
│           ├── tracing.py            # Debugging
│           └── tools.py              # Custom tools
└── pydantic/                  # Pydantic examples
    └── main.py               # Data validation examples
```

## 🎯 Learning Objectives

This repository is designed to help you master:

1. **Advanced Python Type Hints**: Understanding generics, type bounds, and constraints
2. **Data Validation**: Building robust data models with Pydantic
3. **AI Agent Development**: Creating intelligent agents with OpenAI SDK
4. **Documentation**: Writing clear, structured documentation with Markdown
5. **Best Practices**: Following Python and AI development best practices

## 🔧 Key Technologies

- **Python 3.8+**: Modern Python features and type hints
- **Pydantic**: Data validation and settings management
- **OpenAI Agent SDK**: AI agent development framework
- **Type Hints**: Advanced type system usage
- **Markdown**: Documentation and content creation

## 📖 Usage Examples

### Generics Example
```python
from typing import TypeVar

AnimalType = TypeVar('AnimalType', bound=Animal)

def get_animal(animal: AnimalType) -> AnimalType:
    return animal
```

### Pydantic Example
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int = Field(..., gt=0)
```

### Agent SDK Example
```python
from openai import Agent

agent = Agent(
    name="TaskAgent",
    tools=[add_task, check_due_date, mark_complete]
)
```

## 🤝 Contributing

This is a personal exam preparation repository. Feel free to fork and adapt for your own learning needs.

## 📄 License

This project is for educational purposes as part of PIAIC exam preparation.

## 🔗 Related Resources

- [PIAIC Official Website](https://piaic.org/)
- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [OpenAI Agent SDK Documentation](https://platform.openai.com/docs/assistants)
- [Markdown Guide](https://www.markdownguide.org/)

---

**Happy Learning! 🎓**

*This repository is maintained as part of PIAIC (Presidential Initiative for Artificial Intelligence and Computing) exam preparation.* 
