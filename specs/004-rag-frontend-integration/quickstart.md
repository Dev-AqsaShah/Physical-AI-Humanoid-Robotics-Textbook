# Quickstart: RAG Pipeline – Backend and Frontend Integration

**Feature**: 004-rag-frontend-integration
**Date**: 2026-01-17

## Prerequisites

- Python 3.11+
- Node.js 20+
- Existing `.env` file with:
  - `OPENROUTER_API_KEY`
  - `COHERE_API_KEY`
  - `QDRANT_URL`
  - `QDRANT_API_KEY`

## Setup

### 1. Install Backend Dependencies

```bash
# From project root
cd backend
pip install -e .
pip install fastapi uvicorn
```

### 2. Install Frontend Dependencies

```bash
# From book directory
cd book
npm install
```

## Running Locally

### Terminal 1: Start Backend

```bash
# From project root
uvicorn app:app --reload --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Started reloader process
```

### Terminal 2: Start Frontend

```bash
# From book directory
cd book
npm start
```

Expected output:
```
[SUCCESS] Docusaurus website is running at http://localhost:3000/
```

## Verification

### Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "agent_ready": true}
```

### Test Query Endpoint

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2?"}'
```

Expected response (truncated):
```json
{
  "answer": "ROS 2 (Robot Operating System 2) is...",
  "sources": [...],
  "has_relevant_context": true,
  "timing": {...}
}
```

### Test Frontend

1. Open http://localhost:3000 in browser
2. Look for chatbot button at bottom-right
3. Click to open chat interface
4. Type: "What is ROS 2?"
5. Verify answer appears with source citations

## Troubleshooting

### CORS Errors

If you see CORS errors in browser console:
- Ensure backend is running on port 8000
- Check that `CORSMiddleware` is configured in `app.py`

### Agent Errors

If queries fail:
- Check `.env` file has all required API keys
- Verify Qdrant database is accessible
- Check backend logs for detailed error messages

### Frontend Not Loading

If Docusaurus fails to start:
```bash
cd book
npm run clear
npm install
npm start
```

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/ask` | POST | Submit question, get answer |
| `/health` | GET | Check service health |

See `contracts/api.yaml` for full OpenAPI specification.
