#!/usr/bin/env python3
"""
RAG Agent - Question Answering with Retrieved Context

An AI agent that answers questions about the Physical AI & Humanoid Robotics
textbook using retrieved context from the Qdrant vector database.

Uses the OpenAI Agents SDK with grounded responses and source citations.
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass, asdict, field
from typing import Optional

from dotenv import load_dotenv
from rich.console import Console

# Load environment variables early (before creating clients)
load_dotenv()

# Import from existing retrieval module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
from retrieve import semantic_search, ResultSet, SearchResult

# OpenAI Agents SDK imports
from agents import Agent, Runner, function_tool
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Initialize console and logging
console = Console()

# OpenRouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

def _create_openrouter_model() -> OpenAIChatCompletionsModel:
    """Create OpenRouter model client."""
    if not OPENROUTER_API_KEY:
        console.print("[red]Error: OPENROUTER_API_KEY environment variable not set[/red]")
        console.print("Please set it in your .env file or environment")
        sys.exit(2)

    client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    return OpenAIChatCompletionsModel(
        openai_client=client,
        model="mistralai/devstral-small-2505"
    )

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# =============================================================================
# Constants
# =============================================================================

DEFAULT_TOP_K = 5
DEFAULT_RELEVANCE_THRESHOLD = 0.5
MAX_TOP_K = 20
MAX_QUERY_LENGTH = 2000

SYSTEM_INSTRUCTIONS = """You are a helpful assistant that answers questions about the Physical AI & Humanoid Robotics textbook.

You MUST follow these rules:
1. ONLY use information from the retrieved context to answer questions
2. Cite your sources using [Chapter: Section] format after relevant statements
3. If the context does not contain relevant information, say "I don't have information about that in the textbook"
4. Never fabricate or make up information not present in the context
5. If asked about topics outside the textbook's scope, explain you can only answer about Physical AI and Humanoid Robotics topics covered in the textbook
6. Be concise but thorough in your answers
7. If multiple sources support a point, cite all relevant sources"""

# Topics covered in the textbook for helpful suggestions
TEXTBOOK_TOPICS = [
    "ROS 2 fundamentals",
    "Robot simulation with Gazebo",
    "NVIDIA Isaac Sim",
    "Vision-Language-Action models",
    "Capstone projects",
]


# =============================================================================
# Data Classes (T004)
# =============================================================================

@dataclass
class SourceCitation:
    """Represents a citation to source material in the response."""
    chapter: str
    section: str
    url: str
    relevance_score: float


@dataclass
class AgentResponse:
    """Represents the complete response from the agent."""
    answer: str
    sources: list[SourceCitation] = field(default_factory=list)
    has_relevant_context: bool = True
    retrieval_time_ms: float = 0.0
    generation_time_ms: float = 0.0
    total_time_ms: float = 0.0


# =============================================================================
# Context Formatting (T005)
# =============================================================================

def format_context_for_agent(result_set: ResultSet, threshold: float = DEFAULT_RELEVANCE_THRESHOLD) -> tuple[str, list[SourceCitation], bool]:
    """
    Convert ResultSet to LLM-ready text with citations.

    Args:
        result_set: Results from semantic_search()
        threshold: Minimum relevance score to include

    Returns:
        Tuple of (formatted_context, citations, has_relevant_context)
    """
    citations = []
    context_parts = []
    has_relevant = False

    for i, result in enumerate(result_set.results, 1):
        if result.score >= threshold:
            has_relevant = True
            # Add to context
            context_parts.append(
                f"[Source {i}: {result.chapter} > {result.section_title}]\n{result.content}\n"
            )
            # Track citation
            citations.append(SourceCitation(
                chapter=result.chapter,
                section=result.section_title,
                url=result.source_url,
                relevance_score=result.score
            ))

    if not context_parts:
        formatted_context = "No relevant context found in the textbook for this query."
    else:
        formatted_context = "\n---\n".join(context_parts)

    return formatted_context, citations, has_relevant


# =============================================================================
# Retrieval Tool (T006)
# =============================================================================

@function_tool
def retrieve_book_context(query: str, top_k: int = DEFAULT_TOP_K) -> str:
    """
    Retrieve relevant content from the Physical AI & Humanoid Robotics textbook.

    Args:
        query: The question or topic to search for in the textbook
        top_k: Number of text chunks to retrieve (default: 5)

    Returns:
        Formatted context from the textbook with source citations
    """
    logger.info(f"Retrieving context for query: {query[:50]}...")

    result_set = semantic_search(query=query, top_k=top_k)
    formatted_context, _, _ = format_context_for_agent(result_set)

    logger.info(f"Retrieved {result_set.total_count} chunks in {result_set.total_time_ms:.0f}ms")
    return formatted_context


# =============================================================================
# Agent Definition (T007)
# =============================================================================

# Create the RAG agent with retrieval tool (initialized lazily)
rag_agent = None

def _get_agent() -> Agent:
    """Get or create the RAG agent with OpenRouter model."""
    global rag_agent
    if rag_agent is None:
        rag_agent = Agent(
            name="Physical AI Textbook Assistant",
            instructions=SYSTEM_INSTRUCTIONS,
            tools=[retrieve_book_context],
            model=_create_openrouter_model(),
        )
    return rag_agent


# =============================================================================
# Programmatic API (T008)
# =============================================================================

async def ask(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    relevance_threshold: float = DEFAULT_RELEVANCE_THRESHOLD
) -> AgentResponse:
    """
    Ask a question to the RAG agent.

    Args:
        query: The question to ask about the Physical AI textbook
        top_k: Number of chunks to retrieve (1-20, default: 5)
        relevance_threshold: Minimum relevance score (0.0-1.0, default: 0.5)

    Returns:
        AgentResponse with answer and source citations

    Raises:
        ValueError: If query is empty or parameters are out of range
    """
    # Validate inputs
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    if not 1 <= top_k <= MAX_TOP_K:
        raise ValueError(f"top_k must be between 1 and {MAX_TOP_K}")
    if not 0.0 <= relevance_threshold <= 1.0:
        raise ValueError("relevance_threshold must be between 0.0 and 1.0")

    total_start = time.perf_counter()

    # First, do retrieval to get citations
    retrieval_start = time.perf_counter()
    result_set = semantic_search(query=query, top_k=top_k)
    retrieval_time_ms = (time.perf_counter() - retrieval_start) * 1000

    # Format context and extract citations
    formatted_context, citations, has_relevant = format_context_for_agent(
        result_set, threshold=relevance_threshold
    )

    # If no relevant context, return early with helpful message
    if not has_relevant:
        return AgentResponse(
            answer=_no_context_message(query),
            sources=[],
            has_relevant_context=False,
            retrieval_time_ms=retrieval_time_ms,
            generation_time_ms=0.0,
            total_time_ms=(time.perf_counter() - total_start) * 1000
        )

    # Run agent with context
    generation_start = time.perf_counter()

    # Construct prompt with context
    prompt_with_context = f"""Context from the Physical AI & Humanoid Robotics textbook:

{formatted_context}

---

User question: {query}

Please answer the question using ONLY the context provided above. Cite your sources."""

    result = await Runner.run(_get_agent(), prompt_with_context)
    generation_time_ms = (time.perf_counter() - generation_start) * 1000

    total_time_ms = (time.perf_counter() - total_start) * 1000

    return AgentResponse(
        answer=result.final_output,
        sources=citations,
        has_relevant_context=True,
        retrieval_time_ms=retrieval_time_ms,
        generation_time_ms=generation_time_ms,
        total_time_ms=total_time_ms
    )


def _no_context_message(query: str) -> str:
    """Generate a helpful message when no relevant context is found."""
    topics_list = "\n".join(f"  - {topic}" for topic in TEXTBOOK_TOPICS)
    return f"""I couldn't find relevant information about "{query}" in the Physical AI & Humanoid Robotics textbook.

This topic may not be covered in the current curriculum. The textbook covers topics including:
{topics_list}

Would you like to ask about one of these topics instead?"""


# =============================================================================
# Response Formatting (T011)
# =============================================================================

def format_response(response: AgentResponse, verbose: bool = False) -> None:
    """Display response in console format."""
    console.print(f"\n[bold blue]Answer:[/bold blue]\n")
    console.print(response.answer)

    if response.sources:
        console.print(f"\n[bold blue]Sources:[/bold blue]")
        for i, src in enumerate(response.sources, 1):
            console.print(f"[{i}] {src.chapter} > {src.section}")
            console.print(f"    {src.url}")

    # Timing info
    console.print(f"\n[dim]Response time: {response.total_time_ms/1000:.1f}s", end="")
    if verbose:
        console.print(f" (retrieval: {response.retrieval_time_ms/1000:.1f}s, generation: {response.generation_time_ms/1000:.1f}s)", end="")
    console.print("[/dim]\n")


def format_response_json(response: AgentResponse) -> str:
    """Format response as JSON string."""
    return json.dumps({
        "query": "",  # Will be filled by caller
        "answer": response.answer,
        "has_relevant_context": response.has_relevant_context,
        "sources": [asdict(src) for src in response.sources],
        "timing": {
            "retrieval_ms": response.retrieval_time_ms,
            "generation_ms": response.generation_time_ms,
            "total_ms": response.total_time_ms
        }
    }, indent=2)


# =============================================================================
# CLI Interface (T012-T013)
# =============================================================================

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="RAG Agent - Ask questions about the Physical AI & Humanoid Robotics textbook"
    )
    parser.add_argument("query", nargs="?", help="Question to ask")
    parser.add_argument("-k", "--top-k", type=int, default=DEFAULT_TOP_K,
                        help=f"Number of chunks to retrieve (default: {DEFAULT_TOP_K})")
    parser.add_argument("-t", "--threshold", type=float, default=DEFAULT_RELEVANCE_THRESHOLD,
                        help=f"Minimum relevance score (default: {DEFAULT_RELEVANCE_THRESHOLD})")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    parser.add_argument("--test", action="store_true", help="Run validation test suite")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed info")
    return parser.parse_args()


async def run_query(query: str, top_k: int, threshold: float, as_json: bool, verbose: bool) -> int:
    """Execute a single query and display results."""
    try:
        response = await ask(query, top_k=top_k, relevance_threshold=threshold)

        if as_json:
            output = json.loads(format_response_json(response))
            output["query"] = query
            print(json.dumps(output, indent=2))
        else:
            console.print(f"\n[bold]Question:[/bold] {query}")
            format_response(response, verbose=verbose)

        return 0 if response.has_relevant_context else 1

    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        return 2
    except Exception as e:
        logger.error(f"Query failed: {e}")
        console.print(f"[red]Error: {e}[/red]")
        return 3


def ask_sync(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    relevance_threshold: float = DEFAULT_RELEVANCE_THRESHOLD
) -> AgentResponse:
    """
    Synchronous version of ask().

    Args:
        query: The question to ask
        top_k: Number of chunks to retrieve
        relevance_threshold: Minimum relevance score

    Returns:
        AgentResponse with answer and source citations
    """
    return asyncio.run(ask(query, top_k, relevance_threshold))


# =============================================================================
# Validation Suite (T022-T024)
# =============================================================================

# Test queries for validation - covering all modules plus out-of-scope
TEST_QUERIES = [
    # In-scope queries (should return relevant context)
    ("What is ROS 2?", "module-1-ros2", True),
    ("How do I simulate a robot in Gazebo?", "module-2-simulation", True),
    ("What is NVIDIA Isaac Sim used for?", "module-3-isaac", True),
    ("How do vision-language-action models work?", "module-4-vla", True),
    ("What are the capstone project requirements?", "capstone", True),
    # Out-of-scope queries (should return no relevant context)
    ("What is quantum computing?", None, False),
    ("How do I build a website?", None, False),
    ("Explain blockchain technology", None, False),
]


@dataclass
class TestResult:
    """Result of a single validation test."""
    query: str
    expected_relevant: bool
    actual_relevant: bool
    expected_chapter: Optional[str]
    actual_chapter: Optional[str]
    passed: bool
    response_time_ms: float
    details: str


@dataclass
class ValidationReport:
    """Summary of all validation tests."""
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    results: list[TestResult]
    avg_response_time_ms: float
    overall_pass: bool


async def run_validation() -> ValidationReport:
    """Run validation test suite against the agent."""
    from datetime import datetime

    results = []
    total_time = 0.0

    console.print(f"\n[bold blue]RAG Agent Validation Suite[/bold blue]")
    console.print("=" * 50)
    console.print(f"Running {len(TEST_QUERIES)} test queries...\n")

    for query, expected_chapter, should_have_context in TEST_QUERIES:
        start = time.perf_counter()

        try:
            response = await ask(query)
            response_time = (time.perf_counter() - start) * 1000
            total_time += response_time

            # Determine actual chapter from top source
            actual_chapter = None
            if response.sources:
                actual_chapter = response.sources[0].chapter

            # Check if test passed
            relevance_match = response.has_relevant_context == should_have_context
            chapter_match = True
            if should_have_context and expected_chapter:
                chapter_match = actual_chapter and expected_chapter in actual_chapter

            passed = relevance_match and chapter_match

            # Build details
            if passed:
                if should_have_context:
                    details = f"Found: {actual_chapter}"
                else:
                    details = "Correctly identified as out-of-scope"
            else:
                if not relevance_match:
                    details = f"Expected relevant={should_have_context}, got {response.has_relevant_context}"
                else:
                    details = f"Expected chapter containing '{expected_chapter}', got '{actual_chapter}'"

            results.append(TestResult(
                query=query,
                expected_relevant=should_have_context,
                actual_relevant=response.has_relevant_context,
                expected_chapter=expected_chapter,
                actual_chapter=actual_chapter,
                passed=passed,
                response_time_ms=response_time,
                details=details
            ))

            # Display result
            status = "[green][PASS][/green]" if passed else "[red][FAIL][/red]"
            chapter_display = actual_chapter if actual_chapter else "[NO CONTEXT]"
            console.print(f"{status} \"{query[:35]}...\" -> {chapter_display} ({response_time/1000:.1f}s)")

            if not passed:
                console.print(f"      [yellow]{details}[/yellow]")

        except Exception as e:
            response_time = (time.perf_counter() - start) * 1000
            total_time += response_time
            results.append(TestResult(
                query=query,
                expected_relevant=should_have_context,
                actual_relevant=False,
                expected_chapter=expected_chapter,
                actual_chapter=None,
                passed=False,
                response_time_ms=response_time,
                details=f"Error: {e}"
            ))
            console.print(f"[red][FAIL][/red] \"{query[:35]}...\" -> Error: {e}")

    # Calculate summary
    passed_count = sum(1 for r in results if r.passed)
    avg_time = total_time / len(TEST_QUERIES) if TEST_QUERIES else 0

    report = ValidationReport(
        timestamp=datetime.now().isoformat(),
        total_tests=len(TEST_QUERIES),
        passed_tests=passed_count,
        failed_tests=len(TEST_QUERIES) - passed_count,
        results=results,
        avg_response_time_ms=avg_time,
        overall_pass=passed_count == len(TEST_QUERIES)
    )

    # Display summary
    console.print(f"\n[bold]Summary[/bold]")
    console.print("-" * 30)
    console.print(f"Tests: {passed_count}/{len(TEST_QUERIES)} passed")
    console.print(f"Average response time: {avg_time/1000:.1f}s")

    in_scope_correct = sum(1 for r in results if r.expected_relevant and r.passed)
    in_scope_total = sum(1 for r in results if r.expected_relevant)
    out_scope_correct = sum(1 for r in results if not r.expected_relevant and r.passed)
    out_scope_total = sum(1 for r in results if not r.expected_relevant)

    console.print(f"In-scope accuracy: {in_scope_correct}/{in_scope_total}")
    console.print(f"Out-of-scope detection: {out_scope_correct}/{out_scope_total}")

    if report.overall_pass:
        console.print(f"\n[bold green][PASS] VALIDATION PASSED[/bold green]")
    else:
        console.print(f"\n[bold red][FAIL] VALIDATION FAILED[/bold red]")

    return report


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> None:
    """Main entry point for CLI."""
    # Note: load_dotenv() already called at module level

    args = parse_args()

    # Handle --test flag
    if args.test:
        try:
            report = asyncio.run(run_validation())
            sys.exit(0 if report.overall_pass else 4)
        except Exception as e:
            console.print(f"[red]Validation failed: {e}[/red]")
            sys.exit(3)

    # Require query for normal mode
    if not args.query:
        console.print("[yellow]Error: Please provide a question to ask[/yellow]")
        console.print("\nUsage: python agent.py \"Your question here\"")
        console.print("       python agent.py --test  (run validation suite)")
        sys.exit(1)

    # Run the query
    exit_code = asyncio.run(run_query(
        args.query,
        args.top_k,
        args.threshold,
        args.json,
        args.verbose
    ))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
