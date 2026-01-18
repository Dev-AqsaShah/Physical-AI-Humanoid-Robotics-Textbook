#!/usr/bin/env python3
"""
FastAPI Backend for RAG Agent

Exposes the RAG agent via REST API for frontend integration.
"""

import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import the agent
from agent import ask, AgentResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for querying the Physical AI & Humanoid Robotics textbook",
    version="1.0.0"
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# Pydantic models
class QueryRequest(BaseModel):
    """Request body for /ask endpoint."""
    question: str = Field(..., min_length=1, max_length=2000)
    selected_text: Optional[str] = Field(None, max_length=5000)
    top_k: int = Field(5, ge=1, le=20)
    threshold: float = Field(0.5, ge=0.0, le=1.0)


class SourceCitation(BaseModel):
    """Source citation in response."""
    chapter: str
    section: str
    url: str
    relevance_score: float


class TimingInfo(BaseModel):
    """Timing information for response."""
    retrieval_ms: float
    generation_ms: float
    total_ms: float


class QueryResponse(BaseModel):
    """Response body for /ask endpoint."""
    answer: str
    sources: list[SourceCitation]
    has_relevant_context: bool
    timing: TimingInfo


class ErrorResponse(BaseModel):
    """Error response body."""
    error: str
    message: str
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    agent_ready: bool


# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check if the API and agent are ready."""
    return HealthResponse(status="healthy", agent_ready=True)


@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """
    Ask a question about the textbook.

    Returns a grounded answer with source citations.
    """
    try:
        # Build query with optional selected text context
        query = request.question
        if request.selected_text:
            query = f"Context: {request.selected_text}\n\nQuestion: {request.question}"

        # Call the agent
        response: AgentResponse = await ask(
            query=query,
            top_k=request.top_k,
            relevance_threshold=request.threshold
        )

        # Convert to API response
        sources = [
            SourceCitation(
                chapter=src.chapter,
                section=src.section,
                url=src.url,
                relevance_score=src.relevance_score
            )
            for src in response.sources
        ]

        return QueryResponse(
            answer=response.answer,
            sources=sources,
            has_relevant_context=response.has_relevant_context,
            timing=TimingInfo(
                retrieval_ms=response.retrieval_time_ms,
                generation_ms=response.generation_time_ms,
                total_ms=response.total_time_ms
            )
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
