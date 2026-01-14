# Quickstart: RAG Retrieval Module

**Feature**: 002-rag-retrieval
**Time to complete**: ~5 minutes (assumes Feature 001 complete)

## Prerequisites

1. **Feature 001 Complete**: Ingestion pipeline must have run successfully
2. **Environment Configured**: `.env` file with API keys in `backend/`
3. **Python Dependencies**: Already installed from Feature 001

## Verify Prerequisites

### Check Collection Exists

```bash
cd backend
python -c "
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os
load_dotenv()
client = QdrantClient(url=os.getenv('QDRANT_URL'), api_key=os.getenv('QDRANT_API_KEY'))
info = client.get_collection('physical-ai-textbook')
print(f'Collection: physical-ai-textbook')
print(f'Vectors: {info.points_count}')
"
```

Expected output:
```
Collection: physical-ai-textbook
Vectors: 150-200
```

If vectors = 0 or collection not found, run `python main.py` first.

## Usage

### 1. Basic Search

```bash
python retrieve.py "What is ROS 2?"
```

### 2. Search with More Results

```bash
python retrieve.py "robot navigation" --top-k 10
```

### 3. Filter by Chapter

```bash
python retrieve.py "sensors" --chapter module-2-simulation
```

### 4. Run Validation Suite

```bash
python retrieve.py --validate
```

Expected output:
```
RAG Retrieval Validation
========================
Tests: 5/5 passed
Average latency: 0.812s
Metadata integrity: 100%

✓ VALIDATION PASSED
```

### 5. JSON Output

```bash
python retrieve.py "voice control" --json
```

## Test Queries

Try these representative queries:

| Query | Expected Results |
|-------|-----------------|
| "What is ROS 2 and how does it work?" | Module 1 (ROS 2) content |
| "How do I simulate a robot in Gazebo?" | Module 2 (Simulation) content |
| "What is NVIDIA Isaac Sim?" | Module 3 (Isaac) content |
| "How does voice control work?" | Module 4 (VLA) content |
| "What is the capstone project?" | Capstone content |

## Validation Criteria

The validation suite checks:

1. **Relevance**: At least 3 of top-5 results from expected chapter
2. **Metadata**: All results have source_url, section_title, chunk_id
3. **Latency**: Each query completes in under 2 seconds
4. **Integrity**: Content matches stored chunks (no corruption)

## Troubleshooting

### "Collection is empty"
Run the ingestion pipeline first:
```bash
python main.py
```

### "Cohere API error"
Check your `COHERE_API_KEY` in `.env`

### "Qdrant connection failed"
Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`

### Low relevance scores
This is expected for queries outside the book's scope. Try queries related to:
- ROS 2, robotics, simulation
- Gazebo, Isaac Sim, navigation
- Voice control, humanoid robots

## Next Steps

After validation passes:
1. Integration with AI agent (separate feature)
2. Frontend search UI (separate feature)
3. Advanced retrieval optimization (future enhancement)
