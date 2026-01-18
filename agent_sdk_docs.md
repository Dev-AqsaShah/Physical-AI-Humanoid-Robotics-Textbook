# OpenAI Agents SDK - Python

The OpenAI Agents SDK is a lightweight yet powerful framework for building multi-agent workflows in Python. It provides a provider-agnostic approach to orchestrating LLM-based agents, supporting the OpenAI Responses and Chat Completions APIs, as well as 100+ other LLM providers through integrations like LiteLLM. The SDK is designed to handle complex agent interactions with minimal boilerplate code, enabling developers to focus on building intelligent, tool-enabled agents rather than managing low-level API calls and conversation history.

The framework provides automatic conversation history management through session memory, built-in tracing for debugging and monitoring, configurable safety checks through guardrails, and seamless handoffs between specialized agents. It supports structured outputs using Pydantic models, streaming responses for real-time interactions, integration with Model Context Protocol (MCP) servers, voice capabilities through the Voice Pipeline API, and advanced reasoning features with models like GPT-5. With comprehensive examples covering everything from basic agent creation to complex multi-agent workflows, the SDK enables rapid development of production-ready agent systems.

## Core APIs and Functions

### Agent Creation and Basic Execution

```python
import asyncio
from agents import Agent, Runner

# Create a simple agent with instructions
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant that responds in haikus."
)

# Synchronous execution
result = Runner.run_sync(agent, "Tell me about recursion in programming.")
print(result.final_output)
# Output: Function calls itself, / Looping in smaller pieces, / Infinite loop's dance.

# Asynchronous execution
async def main():
    result = await Runner.run(agent, "Explain machine learning.")
    print(result.final_output)
    # Access conversation items
    for item in result.new_items:
        print(item)

asyncio.run(main())
```

### GPT-5 with Reasoning and Verbosity

```python
import asyncio
from openai.types.shared import Reasoning
from agents import Agent, ModelSettings, Runner

async def main():
    # Create agent with GPT-5 and reasoning settings
    agent = Agent(
        name="Knowledgeable GPT-5 Assistant",
        instructions="You're a knowledgeable assistant. Always provide interesting answers.",
        model="gpt-5",
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium"),  # "minimal", "low", "medium", "high"
            verbosity="low"  # "low", "medium", "high"
        )
    )

    result = await Runner.run(agent, "Explain quantum computing.")
    print(result.final_output)

    # Access reasoning content if available
    for item in result.new_items:
        if hasattr(item, 'type') and item.type == 'reasoning':
            print(f"Reasoning: {item.summary}")

asyncio.run(main())
```

### Continuing Conversations with Previous Response ID

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Be very concise."
    )

    # First turn
    result = await Runner.run(agent, "What is the largest country in South America?")
    print(result.final_output)
    # Brazil

    # Continue conversation using previous response ID
    # This avoids re-sending previous messages (OpenAI Responses API only)
    result = await Runner.run(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id
    )
    print(result.final_output)
    # Brasilia

asyncio.run(main())
```

### Function Tools

```python
import asyncio
from typing import Annotated
from pydantic import BaseModel, Field
from agents import Agent, Runner, function_tool

# Define structured output type
class Weather(BaseModel):
    city: str = Field(description="The city name")
    temperature_range: str = Field(description="Temperature in Celsius")
    conditions: str = Field(description="Weather conditions")

# Create a function tool with decorator
@function_tool
def get_weather(city: Annotated[str, "The city to get weather for"]) -> Weather:
    """Get current weather information for a specified city."""
    # In production, this would call a real weather API
    return Weather(
        city=city,
        temperature_range="14-20C",
        conditions="Sunny with wind."
    )

# Create agent with tools
agent = Agent(
    name="Weather Assistant",
    instructions="You are a helpful weather assistant.",
    tools=[get_weather]
)

async def main():
    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny with wind, temperatures between 14-20C.

asyncio.run(main())
```

### Multi-Agent Handoffs

```python
import asyncio
from agents import Agent, Runner

# Create specialized agents
spanish_agent = Agent(
    name="Spanish Agent",
    instructions="You only speak Spanish."
)

english_agent = Agent(
    name="English Agent",
    instructions="You only speak English."
)

french_agent = Agent(
    name="French Agent",
    instructions="You only speak French."
)

# Create triage agent that routes to specialists
triage_agent = Agent(
    name="Triage Agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent, french_agent]
)

async def main():
    # Agent automatically hands off to Spanish agent
    result = await Runner.run(triage_agent, "Hola, ¿cómo estás?")
    print(result.final_output)
    # ¡Hola! Estoy bien, gracias por preguntar. ¿Y tú, cómo estás?

    # Check which agent handled the request
    print(f"Handled by: {result.current_agent.name}")
    # Handled by: Spanish Agent

asyncio.run(main())
```

### Session Memory for Conversation History

```python
import asyncio
from agents import Agent, Runner, SQLiteSession

# Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely."
)

async def main():
    # Create persistent session
    session = SQLiteSession("conversation_123", "conversations.db")

    # First turn - ask about location
    result = await Runner.run(
        agent,
        "What city is the Golden Gate Bridge in?",
        session=session
    )
    print(result.final_output)
    # San Francisco

    # Second turn - agent remembers context automatically
    result = await Runner.run(
        agent,
        "What state is it in?",
        session=session
    )
    print(result.final_output)
    # California

    # Third turn - continues remembering context
    result = await Runner.run(
        agent,
        "What's the population?",
        session=session
    )
    print(result.final_output)
    # Approximately 39 million

    # Retrieve conversation history
    history = await session.get_items()
    print(f"Total items in session: {len(history)}")

    # Get limited history
    recent = await session.get_items(limit=2)
    for msg in recent:
        print(f"{msg['role']}: {msg['content']}")

asyncio.run(main())
```

### Redis Session for Distributed Systems

```python
import asyncio
from agents import Agent, Runner
from agents.extensions.memory import RedisSession

async def main():
    # Connect to Redis for scalable session storage
    session = RedisSession.from_url(
        "user_456",
        url="redis://localhost:6379/0"
    )

    agent = Agent(name="Assistant")

    # Different session IDs maintain separate histories
    result = await Runner.run(
        agent,
        "Remember: my favorite color is blue",
        session=session
    )

    # Later conversation remembers context
    result = await Runner.run(
        agent,
        "What's my favorite color?",
        session=session
    )
    print(result.final_output)
    # Your favorite color is blue.

asyncio.run(main())
```

### Streaming Responses

```python
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, RawResponsesStreamEvent

async def main():
    agent = Agent(
        name="Storyteller",
        instructions="You are a creative storyteller."
    )

    # Stream text output in real-time
    result = Runner.run_streamed(agent, "Tell me 3 short jokes.")

    async for event in result.stream_events():
        # Check for text delta events
        if event.type == "raw_response_event":
            if isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)

    print("\n\n--- Final Output ---")
    print(result.final_output)

asyncio.run(main())
```

### Input Guardrails

```python
import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem
)

# Define guardrail output type
class MathHomeworkOutput(BaseModel):
    reasoning: str
    is_math_homework: bool

# Create guardrail agent
guardrail_agent = Agent(
    name="Guardrail Check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput
)

# Define guardrail function
@input_guardrail
async def math_guardrail(
    context: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Check if input contains math homework request."""
    result = await Runner.run(guardrail_agent, input, context=context.context)
    output = result.final_output_as(MathHomeworkOutput)

    return GuardrailFunctionOutput(
        output_info=output,
        tripwire_triggered=output.is_math_homework
    )

async def main():
    # Create agent with input guardrail
    agent = Agent(
        name="Customer Support Agent",
        instructions="You help customers with their questions.",
        input_guardrails=[math_guardrail]
    )

    input_data = []

    # First request - legitimate question
    input_data.append({
        "role": "user",
        "content": "What's the capital of California?"
    })

    try:
        result = await Runner.run(agent, input_data)
        print(result.final_output)
        # The capital of California is Sacramento.
        input_data = result.to_input_list()
    except InputGuardrailTripwireTriggered:
        print("Request blocked by guardrail")

    # Second request - math homework (triggers guardrail)
    input_data.append({
        "role": "user",
        "content": "Can you help me solve for x: 2x + 5 = 11"
    })

    try:
        result = await Runner.run(agent, input_data)
        print(result.final_output)
    except InputGuardrailTripwireTriggered:
        message = "Sorry, I can't help you with your math homework."
        print(message)
        input_data.append({"role": "assistant", "content": message})

asyncio.run(main())
```

### Structured Output Types

```python
import asyncio
from dataclasses import dataclass
from agents import Agent, Runner, AgentOutputSchema

@dataclass
class JokeCollection:
    """Collection of jokes with metadata."""
    jokes: list[str]
    theme: str
    total_count: int

async def main():
    # Agent with structured output
    agent = Agent(
        name="Comedian",
        instructions="Generate jokes based on user request.",
        output_type=JokeCollection
    )

    result = await Runner.run(agent, "Tell me 3 programming jokes.")

    # Access structured output
    jokes = result.final_output_as(JokeCollection)
    print(f"Theme: {jokes.theme}")
    print(f"Total jokes: {jokes.total_count}")
    for i, joke in enumerate(jokes.jokes, 1):
        print(f"{i}. {joke}")

    # Using non-strict JSON schema for complex types
    @dataclass
    class ComplexOutput:
        data: dict[int, str]  # Not strict-mode compatible

    flexible_agent = Agent(
        name="Flexible Agent",
        instructions="Generate output.",
        output_type=AgentOutputSchema(ComplexOutput, strict_json_schema=False)
    )

    result = await Runner.run(flexible_agent, "Create a mapping of numbers to words.")
    print(result.final_output)

asyncio.run(main())
```

### Model Context Protocol (MCP) Integration

```python
import asyncio
import os
from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerStdio

async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    # Connect to MCP server via stdio
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir]
        }
    ) as server:
        # Create agent with MCP server access
        agent = Agent(
            name="File Assistant",
            instructions="Use the tools to read filesystem and answer questions.",
            mcp_servers=[server]
        )

        trace_id = gen_trace_id()
        with trace(workflow_name="MCP Example", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")

            # List files
            result = await Runner.run(agent, "Read the files and list them.")
            print(result.final_output)

            # Ask questions about content
            result = await Runner.run(agent, "What is my #1 favorite book?")
            print(result.final_output)

            # Reasoning over multiple files
            result = await Runner.run(
                agent,
                "Look at my favorite songs. Suggest one new song I might like."
            )
            print(result.final_output)

asyncio.run(main())
```

### Hosted MCP Tools

```python
import asyncio
from agents import Agent, HostedMCPTool, Runner

async def main():
    # Use hosted MCP server via OpenAI Responses API
    agent = Agent(
        name="Git Assistant",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "gitmcp",
                    "server_url": "https://gitmcp.io/openai/codex",
                    "require_approval": "never"  # Only for trusted servers
                }
            )
        ]
    )

    # Agent can use hosted MCP tools automatically
    result = await Runner.run(
        agent,
        "Which language is this repo written in?"
    )
    print(result.final_output)
    # The repository is primarily written in TypeScript and Rust...

asyncio.run(main())
```

### Built-in Tools

```python
import asyncio
from agents import Agent, Runner, WebSearchTool, trace

async def main():
    # Web search tool
    agent = Agent(
        name="Research Assistant",
        instructions="You are a helpful research assistant.",
        tools=[
            WebSearchTool(
                user_location={"type": "approximate", "city": "New York"}
            )
        ]
    )

    with trace("Web search example"):
        result = await Runner.run(
            agent,
            "Search the web for 'local sports news' and give me 1 interesting update."
        )
        print(result.final_output)
        # The New York Yankees are pursuing a new pitcher...

asyncio.run(main())
```

### Code Interpreter Tool

```python
import asyncio
from agents import Agent, CodeInterpreterTool, Runner, trace

async def main():
    agent = Agent(
        name="Code Interpreter",
        model="gpt-5.2",
        instructions="You love doing math.",
        tools=[
            CodeInterpreterTool(
                tool_config={"type": "code_interpreter", "container": {"type": "auto"}}
            )
        ]
    )

    with trace("Code interpreter example"):
        result = await Runner.run(
            agent,
            "What is the square root of 273 * 312821 plus 1782?"
        )
        print(result.final_output)
        # Code interpreter executes Python to solve: 9232.017...

asyncio.run(main())
```

### File Search Tool

```python
import asyncio
from openai import OpenAI
from agents import Agent, FileSearchTool, Runner, trace

async def main():
    # Create vector store and index a file
    client = OpenAI()
    text = "Arrakis, the desert planet in Frank Herbert's 'Dune,' was inspired by the scarcity of water as a metaphor for oil and other finite resources."
    file_upload = client.files.create(
        file=("example.txt", text.encode("utf-8")),
        purpose="assistants"
    )

    vector_store = client.vector_stores.create(name="example-vector-store")
    client.vector_stores.files.create_and_poll(
        vector_store_id=vector_store.id,
        file_id=file_upload.id
    )

    # Create agent with file search tool
    agent = Agent(
        name="File Searcher",
        instructions="You answer only based on the information in the vector store.",
        tools=[
            FileSearchTool(
                max_num_results=3,
                vector_store_ids=[vector_store.id],
                include_search_results=True
            )
        ]
    )

    with trace("File search example"):
        result = await Runner.run(
            agent,
            "Tell me 1 sentence about Arrakis I might not know."
        )
        print(result.final_output)
        # Arrakis was inspired by water scarcity as a metaphor for oil...

asyncio.run(main())
```

### Image Generation Tool

```python
import asyncio
from agents import Agent, ImageGenerationTool, Runner, trace

async def main():
    agent = Agent(
        name="Image Generator",
        instructions="You are a helpful agent.",
        tools=[
            ImageGenerationTool(
                tool_config={"type": "image_generation", "quality": "low"}
            )
        ]
    )

    with trace("Image generation example"):
        result = await Runner.run(
            agent,
            "Create an image of a frog eating a pizza, comic book style."
        )
        print(result.final_output)
        # I've created a comic book style image of a frog eating a pizza.

        # Access generated image from tool call results
        for item in result.new_items:
            if item.type == "tool_call_item":
                raw_call = item.raw_item
                if raw_call.get("type") == "image_generation_call":
                    img_result = raw_call.get("result")  # Base64 encoded image
                    # Save or display the image

asyncio.run(main())
```

### Shell and Patch Tools

```python
import asyncio
from pathlib import Path
from agents import (
    Agent,
    Runner,
    ShellTool,
    ShellCommandRequest,
    ShellResult,
    ApplyPatchTool,
    LocalShellTool
)

# Custom shell executor with approval logic
class CustomShellExecutor:
    def __init__(self, cwd: Path):
        self.cwd = cwd

    async def __call__(self, request: ShellCommandRequest) -> ShellResult:
        # Custom execution logic with approval, logging, etc.
        # Execute commands and return ShellResult
        pass

async def main():
    # ShellTool with custom executor
    shell_agent = Agent(
        name="Shell Agent",
        instructions="You can run shell commands.",
        tools=[ShellTool(executor=CustomShellExecutor(Path.cwd()))]
    )

    # LocalShellTool for simple local command execution
    local_shell_agent = Agent(
        name="Local Shell Agent",
        instructions="Run local shell commands.",
        tools=[LocalShellTool()]
    )

    # ApplyPatchTool for file editing with diffs
    patch_agent = Agent(
        name="File Editor",
        instructions="You can edit files using patches.",
        tools=[ApplyPatchTool()]
    )

    result = await Runner.run(
        patch_agent,
        "Create a new Python file hello.py with a hello world function"
    )
    print(result.final_output)

asyncio.run(main())
```

### Computer Use Tool

```python
import asyncio
from agents import Agent, Runner, ComputerTool

async def main():
    # Computer use tool for automating desktop tasks
    agent = Agent(
        name="Computer Assistant",
        instructions="You can control the computer to automate tasks.",
        tools=[
            ComputerTool(
                display_width=1024,
                display_height=768,
                display_num=1
            )
        ]
    )

    result = await Runner.run(
        agent,
        "Open a text editor and type 'Hello World'"
    )
    print(result.final_output)
    # The computer tool allows agents to control mouse, keyboard, and screen

asyncio.run(main())
```

### LiteLLM Provider for Any LLM

```python
import asyncio
from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

set_tracing_disabled(disabled=True)

@function_tool
def get_weather(city: str):
    """Get weather for a city."""
    return f"The weather in {city} is sunny."

async def main():
    # Use Anthropic Claude via LiteLLM
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(
            model="anthropic/claude-3-5-sonnet-20240620",
            api_key="your-api-key"
        ),
        tools=[get_weather]
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

    # Use Google Gemini via LiteLLM
    gemini_agent = Agent(
        name="Gemini Assistant",
        model=LitellmModel(
            model="gemini/gemini-2.0-flash",
            api_key="your-gemini-key"
        )
    )

    result = await Runner.run(gemini_agent, "Explain quantum computing.")
    print(result.final_output)

asyncio.run(main())
```

### Usage Tracking

```python
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, Usage, function_tool

class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str

@function_tool
def get_weather(city: str) -> Weather:
    """Get weather information."""
    return Weather(
        city=city,
        temperature_range="14-20C",
        conditions="Sunny"
    )

async def main():
    agent = Agent(
        name="Usage Demo",
        instructions="You are a concise assistant.",
        tools=[get_weather]
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

    # Access usage statistics
    usage: Usage = result.context_wrapper.usage
    print(f"\n=== Usage Statistics ===")
    print(f"Requests: {usage.requests}")
    print(f"Input tokens: {usage.input_tokens}")
    print(f"Output tokens: {usage.output_tokens}")
    print(f"Total tokens: {usage.total_tokens}")
    # Output:
    # === Usage Statistics ===
    # Requests: 2
    # Input tokens: 1247
    # Output tokens: 89
    # Total tokens: 1336

asyncio.run(main())
```

### Tracing and Debugging

```python
import asyncio
import uuid
from agents import Agent, Runner, trace

async def main():
    # Create conversation ID for grouping traces
    conversation_id = str(uuid.uuid4().hex[:16])

    agent = Agent(
        name="Assistant",
        instructions="You are helpful."
    )

    # Wrap execution in trace for monitoring
    with trace("Customer Support Flow", group_id=conversation_id):
        result = await Runner.run(agent, "Help me with my order.")
        print(result.final_output)

    # View trace in OpenAI dashboard
    # https://platform.openai.com/traces

    # Disable tracing if needed
    from agents import set_tracing_disabled
    set_tracing_disabled(disabled=True)

    result = await Runner.run(agent, "Another request.")
    print(result.final_output)

asyncio.run(main())
```

### Voice Pipeline for Streamed Audio

```python
import asyncio
from agents import function_tool
from agents.voice import VoicePipeline, StreamedAudioInput

@function_tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."

# Define a workflow class
class MyWorkflow:
    def __init__(self, secret_word: str, on_start=None):
        self.secret_word = secret_word
        self.on_start = on_start

    async def run(self, audio_input):
        # Process audio and transcription
        # This is a simplified example
        pass

async def main():
    # Create audio input stream
    audio_input = StreamedAudioInput()

    # Create voice pipeline with workflow
    pipeline = VoicePipeline(
        workflow=MyWorkflow(secret_word="hello", on_start=lambda t: print(f"Transcription: {t}"))
    )

    # Run pipeline and stream audio events
    result = await pipeline.run(audio_input)

    async for event in result.stream():
        if event.type == "voice_stream_event_audio":
            # Handle audio output (play to speaker, etc.)
            audio_data = event.data
            print(f"Received audio: {len(audio_data)} bytes")
        elif event.type == "voice_stream_event_lifecycle":
            print(f"Lifecycle event: {event.event}")

asyncio.run(main())
```

### Realtime Voice Agent

```python
import asyncio
from agents import function_tool
from agents.realtime import (
    RealtimeAgent,
    RealtimeRunner,
    RealtimeSession
)

@function_tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."

# Create voice-enabled agent
agent = RealtimeAgent(
    name="Voice Assistant",
    instructions="You are a friendly voice assistant.",
    tools=[get_weather]
)

async def main():
    # Create realtime session for voice interaction
    async with RealtimeSession() as session:
        runner = RealtimeRunner(session)

        # Handle voice events
        async for event in runner.run(agent):
            if event.type == "response.audio.delta":
                # Stream audio to output device
                pass
            elif event.type == "response.text.done":
                print(f"Agent: {event.text}")

asyncio.run(main())
```

### Configuration and Settings

```python
import asyncio
from openai import AsyncOpenAI
from agents import (
    Agent,
    Runner,
    RunConfig,
    ModelSettings,
    set_default_openai_key,
    set_default_openai_client,
    set_default_openai_api
)

# Set API key programmatically
set_default_openai_key("sk-...", use_for_tracing=True)

# Or set custom client
client = AsyncOpenAI(api_key="sk-...", base_url="https://custom.endpoint")
set_default_openai_client(client, use_for_tracing=True)

# Choose API type (responses or chat_completions)
set_default_openai_api("responses")  # or "chat_completions"

async def main():
    # Agent with custom model settings
    agent = Agent(
        name="Custom Agent",
        instructions="You are helpful.",
        model_settings=ModelSettings(
            model="gpt-4o",
            temperature=0.7,
            max_tokens=1000
        )
    )

    # Run with configuration
    result = await Runner.run(
        agent,
        "Tell me a story.",
        config=RunConfig(max_turns=5)
    )
    print(result.final_output)

asyncio.run(main())
```

## Summary

The OpenAI Agents SDK simplifies building sophisticated multi-agent systems by providing high-level abstractions over LLM interactions. Core use cases include customer support chatbots with specialized routing agents, research assistants that combine web search and document analysis tools, code generation systems with built-in safety guardrails, voice-enabled interfaces for hands-free interactions, and long-running workflows with durable conversation history. The framework's session management eliminates manual history tracking, while built-in tracing provides visibility into agent behavior for debugging and optimization. Advanced models like GPT-5 offer enhanced reasoning capabilities with configurable effort levels and verbosity settings.

Integration patterns are designed for flexibility and scalability. The SDK works seamlessly with any OpenAI-compatible API through custom model providers, integrates with external tools via Model Context Protocol servers, supports Redis for distributed session storage across multiple servers, and enables human-in-the-loop workflows through Temporal integration for long-running tasks. The Voice Pipeline API provides streamed audio processing for real-time voice interactions, while the previous_response_id parameter enables efficient conversation continuation without re-sending history. Built-in tools include WebSearchTool for internet queries, FileSearchTool for vector store document retrieval, CodeInterpreterTool for Python code execution and mathematical computations, ImageGenerationTool for creating images from text descriptions, ComputerTool for desktop automation, and shell command execution tools (ShellTool, LocalShellTool, and ApplyPatchTool for file editing with diff patches). With comprehensive streaming support, structured outputs, and extensive guardrail configurations, the SDK provides production-ready components for building intelligent agent systems that can handle complex, multi-step tasks while maintaining safety and reliability.
