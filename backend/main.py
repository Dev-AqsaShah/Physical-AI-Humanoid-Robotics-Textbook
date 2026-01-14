#!/usr/bin/env python3
"""
RAG Pipeline - Content Ingestion, Embeddings, and Vector Storage

Ingests Physical AI textbook markdown files, generates embeddings via Cohere,
and stores vectors in Qdrant Cloud for RAG retrieval.
"""

import hashlib
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Optional

import cohere
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

# Initialize rich console for formatted output
console = Console()

# Constants
COLLECTION_NAME = "physical-ai-textbook"
EMBEDDING_MODEL = "embed-english-v3.0"
EMBEDDING_DIMENSIONS = 1024
BOOK_DOCS_PATH = "../book/docs"
BASE_URL = "https://physical-ai-humanoid-robotics-textb-two-ecru.vercel.app/docs"


# =============================================================================
# Phase 2: Foundational Functions
# =============================================================================

def discover_markdown_files(docs_path: str) -> list[Path]:
    """
    T007: Discover all markdown files in the book docs directory.

    Args:
        docs_path: Path to the docs directory

    Returns:
        List of Path objects for all .md files
    """
    docs_dir = Path(docs_path)
    if not docs_dir.exists():
        console.print(f"[red]Error: Docs directory not found: {docs_path}[/red]")
        return []

    md_files = list(docs_dir.rglob("*.md"))
    # Sort for consistent processing order
    md_files.sort()
    return md_files


def parse_frontmatter(content: str) -> dict:
    """
    T008: Extract YAML frontmatter from markdown content.

    Args:
        content: Raw markdown content

    Returns:
        Dictionary with frontmatter fields (title, sidebar_position, description)
    """
    frontmatter = {}

    # Match YAML frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                frontmatter[key] = value

    return frontmatter


def extract_content(content: str) -> str:
    """
    T009: Strip frontmatter and return body text.

    Args:
        content: Raw markdown content

    Returns:
        Body content without frontmatter
    """
    # Remove YAML frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    # Clean up excessive whitespace
    content = content.strip()
    return content


# =============================================================================
# Phase 3: User Story 1 - Content Ingestion
# =============================================================================

def chunk_content(content: str, min_size: int = 500, max_size: int = 1500) -> list[dict]:
    """
    T010: Split content on H2/H3 headers into semantic chunks.

    Args:
        content: Markdown body content
        min_size: Minimum chunk size in characters
        max_size: Maximum chunk size in characters

    Returns:
        List of dicts with 'content' and 'section_title' keys
    """
    chunks = []

    # Split on H2 headers (## )
    sections = re.split(r'\n(?=## )', content)

    for section in sections:
        if not section.strip():
            continue

        # Extract section title
        title_match = re.match(r'^##\s+(.+?)(?:\n|$)', section)
        section_title = title_match.group(1).strip() if title_match else "Introduction"

        # Remove the header from content for chunking
        section_content = re.sub(r'^##\s+.+?\n', '', section).strip()

        if not section_content:
            continue

        # If section is within size limits, keep as one chunk
        if len(section_content) <= max_size:
            if len(section_content) >= min_size // 2:  # Allow smaller final chunks
                chunks.append({
                    'content': section_content,
                    'section_title': section_title
                })
        else:
            # Split large sections on H3 headers or paragraphs
            subsections = re.split(r'\n(?=### )', section_content)
            current_chunk = ""
            current_title = section_title

            for subsection in subsections:
                # Check for H3 title
                h3_match = re.match(r'^###\s+(.+?)(?:\n|$)', subsection)
                if h3_match:
                    sub_title = f"{section_title} > {h3_match.group(1).strip()}"
                    subsection = re.sub(r'^###\s+.+?\n', '', subsection).strip()
                else:
                    sub_title = section_title

                if len(current_chunk) + len(subsection) <= max_size:
                    current_chunk += ("\n\n" if current_chunk else "") + subsection
                else:
                    # Save current chunk if it has content
                    if current_chunk and len(current_chunk) >= min_size // 2:
                        chunks.append({
                            'content': current_chunk.strip(),
                            'section_title': current_title
                        })
                    current_chunk = subsection
                    current_title = sub_title

            # Don't forget the last chunk
            if current_chunk and len(current_chunk) >= min_size // 4:
                chunks.append({
                    'content': current_chunk.strip(),
                    'section_title': current_title
                })

    return chunks


def compute_content_hash(content: str) -> str:
    """
    T021: Compute MD5 hash of chunk content for change detection.

    Args:
        content: Chunk text content

    Returns:
        MD5 hash string
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def generate_chunk_id(file_path: str, chunk_index: int) -> str:
    """
    T011/T022: Generate deterministic UUID from path and index for idempotency.

    Args:
        file_path: Source file path
        chunk_index: Position of chunk in document

    Returns:
        Deterministic UUID string
    """
    # Create deterministic hash from path + index
    hash_input = f"{file_path}:{chunk_index}"
    hash_bytes = hashlib.sha256(hash_input.encode()).hexdigest()[:32]
    return str(uuid.UUID(hash_bytes))


def build_source_url(file_path: Path, docs_base: str) -> str:
    """
    T017: Derive web URL from file path.

    Args:
        file_path: Path to markdown file
        docs_base: Base path of docs directory

    Returns:
        Full URL for the page
    """
    # Get relative path from docs directory
    try:
        rel_path = file_path.relative_to(Path(docs_base).resolve())
    except ValueError:
        rel_path = file_path

    # Convert to URL path (remove .md extension)
    url_path = str(rel_path).replace('\\', '/').replace('.md', '')

    # Handle index files
    if url_path.endswith('/index'):
        url_path = url_path[:-6]

    return f"{BASE_URL}/{url_path}" if url_path else BASE_URL


def get_chapter_name(file_path: Path) -> str:
    """
    Extract chapter/module name from file path.

    Args:
        file_path: Path to markdown file

    Returns:
        Chapter name (parent directory)
    """
    return file_path.parent.name if file_path.parent.name != "docs" else "intro"


def create_cohere_client() -> cohere.Client:
    """
    T012: Initialize Cohere client with API key.

    Returns:
        Configured Cohere client

    Raises:
        SystemExit: If COHERE_API_KEY is not set
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        console.print("[red]Error: COHERE_API_KEY environment variable not set[/red]")
        console.print("Please set it in your .env file or environment")
        sys.exit(2)

    return cohere.Client(api_key)


def generate_embeddings(client: cohere.Client, texts: list[str], max_retries: int = 3) -> list[list[float]]:
    """
    T013/T032: Generate embeddings with retry logic for rate limits.

    Args:
        client: Cohere client
        texts: List of text strings to embed
        max_retries: Maximum retry attempts

    Returns:
        List of embedding vectors
    """
    for attempt in range(max_retries):
        try:
            response = client.embed(
                texts=texts,
                model=EMBEDDING_MODEL,
                input_type="search_document",
                truncate="END"
            )
            return response.embeddings
        except cohere.RateLimitError:
            wait_time = (2 ** attempt) * 30  # Exponential backoff: 30s, 60s, 120s
            console.print(f"[yellow]Rate limit hit. Waiting {wait_time}s (attempt {attempt + 1}/{max_retries})[/yellow]")
            time.sleep(wait_time)
        except Exception as e:
            console.print(f"[red]Cohere API error: {e}[/red]")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                raise

    raise Exception("Max retries exceeded for Cohere API")


def create_qdrant_client() -> QdrantClient:
    """
    T014: Connect to Qdrant Cloud.

    Returns:
        Configured Qdrant client

    Raises:
        SystemExit: If credentials are not set
    """
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        console.print("[red]Error: QDRANT_URL and QDRANT_API_KEY must be set[/red]")
        console.print("Please set them in your .env file or environment")
        sys.exit(2)

    try:
        client = QdrantClient(url=url, api_key=api_key)
        # Test connection
        client.get_collections()
        return client
    except Exception as e:
        console.print(f"[red]Error connecting to Qdrant: {e}[/red]")
        console.print("Please verify your QDRANT_URL and QDRANT_API_KEY")
        sys.exit(3)


def ensure_collection(client: QdrantClient) -> None:
    """
    T015: Create Qdrant collection if it doesn't exist.

    Args:
        client: Qdrant client
    """
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if COLLECTION_NAME not in collection_names:
        console.print(f"[blue]Creating collection: {COLLECTION_NAME}[/blue]")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=EMBEDDING_DIMENSIONS,
                distance=models.Distance.COSINE
            )
        )
    else:
        console.print(f"[blue]Collection exists: {COLLECTION_NAME}[/blue]")


def store_vectors(
    client: QdrantClient,
    vectors: list[list[float]],
    payloads: list[dict],
    ids: list[str]
) -> int:
    """
    T016/T023: Upsert vectors with payload metadata (idempotent).

    Args:
        client: Qdrant client
        vectors: List of embedding vectors
        payloads: List of metadata dicts
        ids: List of point IDs

    Returns:
        Number of vectors stored
    """
    points = [
        models.PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        )
        for point_id, vector, payload in zip(ids, vectors, payloads)
    ]

    # Upsert handles both insert and update (idempotent)
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    return len(points)


def process_page(
    file_path: Path,
    docs_base: str,
    cohere_client: cohere.Client,
    qdrant_client: QdrantClient
) -> tuple[int, int]:
    """
    T018: Orchestrate extract → chunk → embed → store for one page.

    Args:
        file_path: Path to markdown file
        docs_base: Base docs directory
        cohere_client: Cohere client
        qdrant_client: Qdrant client

    Returns:
        Tuple of (chunks_created, vectors_stored)
    """
    # Read file
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[yellow]Warning: Could not read {file_path}: {e}[/yellow]")
        return 0, 0

    # Parse frontmatter and extract body
    frontmatter = parse_frontmatter(content)
    body = extract_content(content)

    # T033: Skip empty content
    if not body or len(body.strip()) < 50:
        console.print(f"[yellow]Skipping {file_path.name}: empty or minimal content[/yellow]")
        return 0, 0

    # Chunk content
    chunks = chunk_content(body)
    if not chunks:
        return 0, 0

    # Prepare metadata
    source_url = build_source_url(file_path, docs_base)
    chapter = get_chapter_name(file_path)
    page_title = frontmatter.get('title', file_path.stem)

    # Prepare for embedding
    texts = [chunk['content'] for chunk in chunks]

    # Generate embeddings
    try:
        embeddings = generate_embeddings(cohere_client, texts)
    except Exception as e:
        console.print(f"[red]Error generating embeddings for {file_path.name}: {e}[/red]")
        return len(chunks), 0

    # Prepare vectors and payloads
    ids = []
    payloads = []

    for i, chunk in enumerate(chunks):
        chunk_id = generate_chunk_id(str(file_path), i)
        content_hash = compute_content_hash(chunk['content'])

        ids.append(chunk_id)
        payloads.append({
            'source_url': source_url,
            'section_title': chunk['section_title'],
            'chunk_id': f"{hashlib.md5(str(file_path).encode()).hexdigest()[:8]}_{i}",
            'chapter': chapter,
            'page_title': page_title,
            'position': i,
            'content_hash': content_hash,
            'content': chunk['content']
        })

    # Store in Qdrant
    stored = store_vectors(qdrant_client, embeddings, payloads, ids)

    return len(chunks), stored


# =============================================================================
# Phase 5: User Story 3 - Verification
# =============================================================================

def verify_ingestion(qdrant_client: QdrantClient) -> int:
    """
    T025: Query and return vector count.

    Args:
        qdrant_client: Qdrant client

    Returns:
        Total vector count in collection
    """
    try:
        collection_info = qdrant_client.get_collection(COLLECTION_NAME)
        return collection_info.points_count
    except Exception as e:
        console.print(f"[red]Error getting collection info: {e}[/red]")
        return 0


def run_sample_query(
    cohere_client: cohere.Client,
    qdrant_client: QdrantClient,
    query: str = "What is ROS 2 and how does it work?"
) -> list[dict]:
    """
    T026: Execute a sample semantic search query.

    Args:
        cohere_client: Cohere client
        qdrant_client: Qdrant client
        query: Search query text

    Returns:
        List of search results with scores and metadata
    """
    # Generate query embedding
    response = cohere_client.embed(
        texts=[query],
        model=EMBEDDING_MODEL,
        input_type="search_query",
        truncate="END"
    )
    query_vector = response.embeddings[0]

    # Search Qdrant using query_points (qdrant-client >= 1.16)
    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=5
    )

    return [
        {
            'score': hit.score,
            'source_url': hit.payload.get('source_url', ''),
            'section_title': hit.payload.get('section_title', ''),
            'chapter': hit.payload.get('chapter', ''),
            'content_preview': hit.payload.get('content', '')[:150] + '...'
        }
        for hit in results.points
    ]


def display_results(results: list[dict], query: str) -> None:
    """
    T027: Display top-5 results with scores and metadata.

    Args:
        results: Search results from run_sample_query
        query: Original query string
    """
    console.print(f"\n[bold blue]Verification Query Results[/bold blue]")
    console.print(f"Query: \"{query}\"\n")

    for i, result in enumerate(results, 1):
        console.print(f"[bold]{i}. [{result['score']:.2f}][/bold] {result['chapter']}")
        console.print(f"   Section: {result['section_title']}")
        console.print(f"   URL: {result['source_url']}")
        console.print(f"   Preview: {result['content_preview']}\n")


def check_verification_passed(results: list[dict], min_relevant: int = 3) -> bool:
    """
    T028: Check if at least min_relevant results are relevant.

    Args:
        results: Search results
        min_relevant: Minimum number of relevant results required

    Returns:
        True if verification passes
    """
    # Consider a result relevant if score > 0.5 and related to ROS
    relevant_count = sum(
        1 for r in results
        if r['score'] > 0.5 and ('ros' in r['chapter'].lower() or 'ros' in r['section_title'].lower())
    )
    return relevant_count >= min_relevant


# =============================================================================
# Phase 6: Polish - Main Entry Point
# =============================================================================

def main() -> None:
    """
    T020/T035: Main ingestion pipeline entry point.
    """
    start_time = time.time()

    console.print("[bold blue]RAG Pipeline Ingestion[/bold blue]")
    console.print("=" * 50)

    # Load environment variables
    load_dotenv()

    # Get docs path (relative to script location)
    script_dir = Path(__file__).parent
    docs_path = (script_dir / BOOK_DOCS_PATH).resolve()

    console.print(f"Book path: {docs_path}")
    console.print(f"Collection: {COLLECTION_NAME}\n")

    # Discover files
    md_files = discover_markdown_files(str(docs_path))
    if not md_files:
        console.print("[red]No markdown files found. Exiting.[/red]")
        sys.exit(1)

    console.print(f"Found {len(md_files)} markdown files\n")

    # Initialize clients
    console.print("[blue]Connecting to services...[/blue]")
    cohere_client = create_cohere_client()
    qdrant_client = create_qdrant_client()

    # Ensure collection exists
    ensure_collection(qdrant_client)
    console.print()

    # Process all files
    total_chunks = 0
    total_vectors = 0
    failed_pages = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Processing pages...", total=len(md_files))

        for i, file_path in enumerate(md_files, 1):
            progress.update(task, description=f"[{i}/{len(md_files)}] {file_path.name}")

            try:
                chunks, vectors = process_page(
                    file_path,
                    str(docs_path),
                    cohere_client,
                    qdrant_client
                )
                total_chunks += chunks
                total_vectors += vectors

                if vectors == 0 and chunks > 0:
                    failed_pages.append(file_path.name)

            except Exception as e:
                console.print(f"[red]Error processing {file_path.name}: {e}[/red]")
                failed_pages.append(file_path.name)

            progress.advance(task)

    # T034: Final summary
    elapsed = time.time() - start_time

    console.print("\n[bold blue]Summary[/bold blue]")
    console.print("-" * 30)
    console.print(f"Pages processed: {len(md_files) - len(failed_pages)}/{len(md_files)}")
    console.print(f"Chunks created: {total_chunks}")
    console.print(f"Vectors stored: {total_vectors}")
    console.print(f"Time elapsed: {elapsed:.1f}s")

    if failed_pages:
        console.print(f"\n[yellow]Failed pages ({len(failed_pages)}):[/yellow]")
        for page in failed_pages:
            console.print(f"  - {page}")

    # T029: Run verification
    console.print("\n[bold blue]Running Verification...[/bold blue]")

    vector_count = verify_ingestion(qdrant_client)
    console.print(f"Total vectors in collection: {vector_count}")

    if vector_count > 0:
        query = "What is ROS 2 and how does it work?"
        results = run_sample_query(cohere_client, qdrant_client, query)
        display_results(results, query)

        if check_verification_passed(results):
            console.print("[bold green][PASS] Verification PASSED[/bold green]")
        else:
            console.print("[bold yellow][WARN] Verification: Results may need review[/bold yellow]")
    else:
        console.print("[red][FAIL] Verification FAILED: No vectors stored[/red]")
        sys.exit(1)

    console.print("\n[bold green]Ingestion complete![/bold green]")


if __name__ == "__main__":
    main()
