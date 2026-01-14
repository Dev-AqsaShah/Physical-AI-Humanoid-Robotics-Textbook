# Quickstart: RAG Pipeline Ingestion

**Feature**: 001-rag-pipeline
**Time to complete**: ~15 minutes

## Prerequisites

1. **Python 3.11+** installed
2. **uv** package manager installed ([install guide](https://github.com/astral-sh/uv))
3. **Cohere API Key** ([sign up free](https://dashboard.cohere.com/))
4. **Qdrant Cloud Account** ([sign up free](https://cloud.qdrant.io/))

## Setup Steps

### 1. Create Backend Directory

```bash
cd hackathon-1
mkdir backend
cd backend
```

### 2. Initialize Python Project with uv

```bash
uv init
uv add cohere qdrant-client python-dotenv rich
```

### 3. Configure Environment Variables

Create `.env` file:

```bash
# backend/.env
COHERE_API_KEY=your-cohere-api-key-here
QDRANT_URL=https://your-cluster.region.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key-here
```

Create `.env.example` template:

```bash
# backend/.env.example
COHERE_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
```

### 4. Get Credentials

**Cohere API Key**:
1. Go to [dashboard.cohere.com](https://dashboard.cohere.com/)
2. Navigate to API Keys
3. Create a new key or copy existing

**Qdrant Cloud**:
1. Go to [cloud.qdrant.io](https://cloud.qdrant.io/)
2. Create a free cluster
3. Copy the cluster URL and API key from cluster details

### 5. Run Ingestion

```bash
# From backend/ directory
uv run python main.py
```

### 6. Verify Results

The pipeline will:
1. Read 40 markdown files from the textbook
2. Chunk content into ~150-200 segments
3. Generate embeddings via Cohere
4. Store vectors in Qdrant
5. Run a verification query

Expected output:
```
RAG Pipeline Ingestion
======================
Pages processed: 40/40
Chunks created: 187
Vectors stored: 187

Verification: ✓ Top results are semantically relevant
```

## Troubleshooting

### "Missing environment variables"

Ensure `.env` file exists in `backend/` with all three variables set.

### "Cohere rate limit exceeded"

Free tier has 100 calls/minute. The pipeline handles this with automatic retries.

### "Cannot connect to Qdrant"

1. Verify cluster is running in Qdrant Cloud dashboard
2. Check URL includes port `:6333`
3. Verify API key is correct

### "No files found"

Ensure the book exists at `../Physical-AI-Humanoid-Robotics-Textbook/book/docs/`

## Next Steps

After successful ingestion:
1. Vectors are ready for retrieval queries
2. Use Qdrant dashboard to inspect stored data
3. Build retrieval API (separate feature)
