#!/usr/bin/env python3
"""
RAG Pipeline - Retrieval Module

Performs semantic search against the Qdrant vector database using Cohere embeddings.
Read-only operations only - no data mutation or re-ingestion.
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

import cohere
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from rich.console import Console

# Initialize rich console for formatted output
console = Console()

# =============================================================================
# Constants (matching main.py)
# =============================================================================

COLLECTION_NAME = "physical-ai-textbook"
EMBEDDING_MODEL = "embed-english-v3.0"
EMBEDDING_DIMENSIONS = 1024


# =============================================================================
# Data Structures
# =============================================================================

@dataclass
class SearchResult:
    """A single retrieved chunk with metadata."""
    score: float
    content: str
    source_url: str
    section_title: str
    chunk_id: str
    chapter: str
    page_title: str
    position: int
    content_hash: str


@dataclass
class ResultSet:
    """Collection of search results with timing metadata."""
    query: str
    results: list[SearchResult]
    total_count: int
    query_time_ms: float
    search_time_ms: float
    total_time_ms: float


@dataclass
class ValidationResult:
    """Result of a single validation test."""
    query_text: str
    expected_chapter: str
    top_chapter: str
    relevance_pass: bool
    metadata_complete: bool
    latency_ms: float
    latency_pass: bool
    pass_all: bool


@dataclass
class ValidationReport:
    """Summary of all validation tests."""
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    results: list[ValidationResult]
    avg_latency_ms: float
    overall_pass: bool


# =============================================================================
# Client Initialization (reused patterns from main.py)
# =============================================================================

def create_cohere_client() -> cohere.Client:
    """Initialize Cohere client with API key."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        console.print("[red]Error: COHERE_API_KEY environment variable not set[/red]")
        sys.exit(2)
    return cohere.Client(api_key)


def create_qdrant_client() -> QdrantClient:
    """Connect to Qdrant Cloud."""
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        console.print("[red]Error: QDRANT_URL and QDRANT_API_KEY must be set[/red]")
        sys.exit(2)

    try:
        client = QdrantClient(url=url, api_key=api_key)
        client.get_collections()  # Test connection
        return client
    except Exception as e:
        console.print(f"[red]Error connecting to Qdrant: {e}[/red]")
        sys.exit(3)


def check_collection_exists(client: QdrantClient) -> bool:
    """Check if the collection exists (read-only, no create)."""
    try:
        collections = client.get_collections().collections
        return any(c.name == COLLECTION_NAME for c in collections)
    except Exception:
        return False


def get_collection_stats(client: QdrantClient) -> dict:
    """Get vector collection statistics (read-only)."""
    try:
        if not check_collection_exists(client):
            return {
                "collection_name": COLLECTION_NAME,
                "vector_count": 0,
                "status": "not_found"
            }
        info = client.get_collection(COLLECTION_NAME)
        return {
            "collection_name": COLLECTION_NAME,
            "vector_count": info.points_count,
            "status": "ready" if info.points_count > 0 else "empty"
        }
    except Exception as e:
        return {
            "collection_name": COLLECTION_NAME,
            "vector_count": 0,
            "status": f"error: {e}"
        }


# =============================================================================
# Core Retrieval Functions
# =============================================================================

def generate_query_embedding(client: cohere.Client, query: str) -> list[float]:
    """Generate embedding for search query using Cohere."""
    response = client.embed(
        texts=[query],
        model=EMBEDDING_MODEL,
        input_type="search_query",
        truncate="END"
    )
    return response.embeddings[0]


def semantic_search(
    query: str,
    top_k: int = 5,
    chapter_filter: Optional[str] = None,
    cohere_client: Optional[cohere.Client] = None,
    qdrant_client: Optional[QdrantClient] = None
) -> ResultSet:
    """Perform semantic search against the vector database."""
    total_start = time.perf_counter()

    # Initialize clients if not provided
    if cohere_client is None:
        cohere_client = create_cohere_client()
    if qdrant_client is None:
        qdrant_client = create_qdrant_client()

    # Check collection exists
    if not check_collection_exists(qdrant_client):
        console.print("[red]Error: Collection not found. Run ingestion pipeline first.[/red]")
        sys.exit(3)

    # Generate query embedding
    query_start = time.perf_counter()
    query_vector = generate_query_embedding(cohere_client, query)
    query_time_ms = (time.perf_counter() - query_start) * 1000

    # Search Qdrant (fetch more if filtering, for post-filter)
    search_start = time.perf_counter()
    fetch_limit = top_k * 3 if chapter_filter else top_k
    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=fetch_limit
    )
    search_time_ms = (time.perf_counter() - search_start) * 1000

    # Convert to SearchResult objects (with optional post-filtering)
    search_results = []
    for hit in results.points:
        payload = hit.payload or {}
        search_results.append(SearchResult(
            score=hit.score,
            content=payload.get("content", ""),
            source_url=payload.get("source_url", ""),
            section_title=payload.get("section_title", ""),
            chunk_id=payload.get("chunk_id", ""),
            chapter=payload.get("chapter", ""),
            page_title=payload.get("page_title", ""),
            position=payload.get("position", 0),
            content_hash=payload.get("content_hash", "")
        ))

    # Apply post-filter if chapter specified
    if chapter_filter:
        search_results = [r for r in search_results if chapter_filter in r.chapter][:top_k]

    total_time_ms = (time.perf_counter() - total_start) * 1000

    return ResultSet(
        query=query,
        results=search_results,
        total_count=len(search_results),
        query_time_ms=query_time_ms,
        search_time_ms=search_time_ms,
        total_time_ms=total_time_ms
    )


# =============================================================================
# Validation Functions
# =============================================================================

def validate_metadata(result: SearchResult) -> bool:
    """Check if all required metadata fields are present."""
    return all([
        result.source_url,
        result.section_title,
        result.chunk_id,
        result.chapter,
        result.content
    ])


def validate_content_integrity(result: SearchResult) -> bool:
    """Check if content hash is present (integrity marker)."""
    return bool(result.content_hash) and bool(result.content)


# Test queries covering all modules
TEST_QUERIES = [
    ("What is ROS 2 and how does it work?", "module-1-ros2"),
    ("How do I simulate a robot in Gazebo?", "module-2-simulation"),
    ("What is NVIDIA Isaac Sim used for?", "module-3-isaac"),
    ("How do vision-language-action models work?", "module-4-vla"),
    ("What are the capstone project requirements?", "capstone"),
]


def run_validation_suite(
    cohere_client: cohere.Client,
    qdrant_client: QdrantClient
) -> ValidationReport:
    """Run validation test suite with representative queries."""
    results = []
    total_latency = 0.0

    for query_text, expected_chapter in TEST_QUERIES:
        start = time.perf_counter()
        result_set = semantic_search(
            query=query_text,
            top_k=5,
            cohere_client=cohere_client,
            qdrant_client=qdrant_client
        )
        latency_ms = (time.perf_counter() - start) * 1000
        total_latency += latency_ms

        # Check results
        top_chapter = result_set.results[0].chapter if result_set.results else ""
        relevance_pass = expected_chapter in top_chapter or any(
            expected_chapter in r.chapter for r in result_set.results[:3]
        )
        metadata_complete = all(validate_metadata(r) for r in result_set.results)
        latency_pass = latency_ms < 2000  # < 2 seconds

        results.append(ValidationResult(
            query_text=query_text,
            expected_chapter=expected_chapter,
            top_chapter=top_chapter,
            relevance_pass=relevance_pass,
            metadata_complete=metadata_complete,
            latency_ms=latency_ms,
            latency_pass=latency_pass,
            pass_all=relevance_pass and metadata_complete and latency_pass
        ))

    passed = sum(1 for r in results if r.pass_all)
    avg_latency = total_latency / len(TEST_QUERIES) if TEST_QUERIES else 0

    return ValidationReport(
        timestamp=datetime.now().isoformat(),
        total_tests=len(TEST_QUERIES),
        passed_tests=passed,
        failed_tests=len(TEST_QUERIES) - passed,
        results=results,
        avg_latency_ms=avg_latency,
        overall_pass=passed == len(TEST_QUERIES) and avg_latency < 1000
    )


# =============================================================================
# Output Formatting
# =============================================================================

def format_results(result_set: ResultSet) -> None:
    """Display search results in console format."""
    console.print(f"\n[bold blue]RAG Retrieval Results[/bold blue]")
    console.print("=" * 50)
    console.print(f"Query: \"{result_set.query}\"")
    console.print(f"Results: {result_set.total_count} | Time: {result_set.total_time_ms/1000:.3f}s\n")

    for i, result in enumerate(result_set.results, 1):
        console.print(f"[bold]{i}. [{result.score:.2f}][/bold] {result.chapter}")
        console.print(f"   Section: {result.section_title}")
        console.print(f"   URL: {result.source_url}")
        preview = result.content[:150] + "..." if len(result.content) > 150 else result.content
        console.print(f"   Preview: {preview}\n")


def format_results_json(result_set: ResultSet) -> str:
    """Format results as JSON string."""
    return json.dumps({
        "query": result_set.query,
        "total_count": result_set.total_count,
        "total_time_ms": result_set.total_time_ms,
        "results": [asdict(r) for r in result_set.results]
    }, indent=2)


def display_validation_report(report: ValidationReport) -> None:
    """Display validation report with pass/fail summary."""
    console.print(f"\n[bold blue]RAG Retrieval Validation[/bold blue]")
    console.print("=" * 50)
    console.print(f"Running {report.total_tests} test queries...\n")

    for i, result in enumerate(report.results, 1):
        status = "[green][PASS][/green]" if result.pass_all else "[red][FAIL][/red]"
        console.print(f"{i}. {status} \"{result.query_text[:30]}...\" -> {result.top_chapter} ({result.latency_ms/1000:.2f}s)")

        if not result.pass_all:
            if not result.relevance_pass:
                console.print(f"   [yellow]Expected: {result.expected_chapter}[/yellow]")
            if not result.metadata_complete:
                console.print(f"   [yellow]Metadata incomplete[/yellow]")
            if not result.latency_pass:
                console.print(f"   [yellow]Latency exceeded 2s[/yellow]")

    console.print(f"\n[bold]Summary[/bold]")
    console.print("-" * 30)
    console.print(f"Tests: {report.passed_tests}/{report.total_tests} passed")
    console.print(f"Average latency: {report.avg_latency_ms/1000:.2f}s")

    metadata_ok = all(r.metadata_complete for r in report.results)
    console.print(f"Metadata integrity: {'100%' if metadata_ok else 'INCOMPLETE'}")

    if report.overall_pass:
        console.print("\n[bold green][PASS] VALIDATION PASSED[/bold green]")
    else:
        console.print("\n[bold red][FAIL] VALIDATION FAILED[/bold red]")


def display_stats(stats: dict) -> None:
    """Display collection statistics."""
    console.print(f"\n[bold blue]Collection Statistics[/bold blue]")
    console.print("=" * 50)
    console.print(f"Collection: {stats['collection_name']}")
    console.print(f"Vectors: {stats['vector_count']}")
    console.print(f"Status: {stats['status']}")


# =============================================================================
# CLI Entry Point
# =============================================================================

def main() -> None:
    """Main entry point for retrieval CLI."""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="RAG Retrieval - Semantic search against the textbook vector database"
    )
    parser.add_argument("query", nargs="?", help="Search query text")
    parser.add_argument("-k", "--top-k", type=int, default=5, help="Number of results (default: 5)")
    parser.add_argument("-c", "--chapter", type=str, help="Filter by chapter name")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    parser.add_argument("-v", "--validate", action="store_true", help="Run validation suite")
    parser.add_argument("-s", "--stats", action="store_true", help="Show collection stats")

    args = parser.parse_args()

    # Handle --stats flag
    if args.stats:
        qdrant_client = create_qdrant_client()
        stats = get_collection_stats(qdrant_client)
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            display_stats(stats)
        sys.exit(0)

    # Handle --validate flag
    if args.validate:
        cohere_client = create_cohere_client()
        qdrant_client = create_qdrant_client()
        report = run_validation_suite(cohere_client, qdrant_client)
        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            display_validation_report(report)
        sys.exit(0 if report.overall_pass else 4)

    # Require query for search
    if not args.query:
        parser.print_help()
        console.print("\n[yellow]Error: Query required for search[/yellow]")
        sys.exit(1)

    # Validate query
    if not args.query.strip():
        console.print("[red]Error: Query cannot be empty[/red]")
        sys.exit(1)

    # Execute search
    result_set = semantic_search(
        query=args.query,
        top_k=args.top_k,
        chapter_filter=args.chapter
    )

    # Display results
    if args.json:
        print(format_results_json(result_set))
    else:
        format_results(result_set)

    # Exit with appropriate code
    sys.exit(0 if result_set.total_count > 0 else 1)


if __name__ == "__main__":
    main()
