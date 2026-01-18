# Quickstart: RAG Agent

**Feature Branch**: `003-rag-agent`

Get the RAG agent running in under 5 minutes.

---

## Prerequisites

- Python 3.9 or newer
- Existing RAG pipeline setup (Features 001 and 002 complete)
- API keys for OpenAI, Cohere, and Qdrant

## 1. Install Dependencies

```bash
# Navigate to project root
cd hackathon-1

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install the OpenAI Agents SDK
pip install openai-agents
```

## 2. Configure Environment

Ensure your `.env` file contains all required API keys:

```env
# .env file
OPENAI_API_KEY=sk-your-openai-key
COHERE_API_KEY=your-cohere-key
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-qdrant-key
```

## 3. Run Your First Query

```bash
# Ask a question about the textbook
python agent.py "What is ROS 2?"
```

Expected output:

```
Question: What is ROS 2?

Answer:
ROS 2 (Robot Operating System 2) is a set of software libraries and tools
for building robot applications. It provides hardware abstraction, device
drivers, communication between processes over multiple machines, tools for
visualization and simulation, and much more...

Sources:
[1] Module 1: ROS 2 Fundamentals > Introduction to ROS 2
    https://physical-ai-textbook.../docs/module-1-ros2/intro

Response time: 2.1s
```

## 4. Validate the Agent

Run the built-in test suite to verify everything works:

```bash
python agent.py --test
```

Expected output:

```
RAG Agent Validation Suite
==========================
Running 8 test queries...

[PASS] "What is ROS 2?" -> module-1-ros2 (0.89, 1.2s)
[PASS] "How do I simulate in Gazebo?" -> module-2-simulation (0.85, 1.1s)
...

[PASS] VALIDATION PASSED
```

---

## Common Commands

| Command | Description |
|---------|-------------|
| `python agent.py "question"` | Ask a question |
| `python agent.py --test` | Run validation suite |
| `python agent.py -k 10 "question"` | Retrieve more context (10 chunks) |
| `python agent.py --json "question"` | Get JSON output |
| `python agent.py -v "question"` | Verbose mode with retrieval details |

---

## Programmatic Usage

```python
import asyncio
from agent import ask

async def main():
    response = await ask("What is ROS 2?")
    print(response.answer)

asyncio.run(main())
```

---

## Troubleshooting

### "OPENAI_API_KEY not set"

```bash
export OPENAI_API_KEY=sk-your-key
# or add to .env file
```

### "Knowledge base unavailable"

Ensure Qdrant credentials are correct and the collection exists:

```bash
python backend/retrieve.py --stats
```

### "No relevant context found"

The question may be outside the textbook's scope. Try questions about:
- ROS 2 fundamentals
- Robot simulation with Gazebo
- NVIDIA Isaac Sim
- Vision-Language-Action models
- Capstone projects

---

## Next Steps

1. **Explore the textbook**: Ask questions about different modules
2. **Review sources**: Check the citation URLs for deeper learning
3. **Customize retrieval**: Adjust `--top-k` and `--threshold` for your needs
4. **Integrate programmatically**: Use the `ask()` function in your code
