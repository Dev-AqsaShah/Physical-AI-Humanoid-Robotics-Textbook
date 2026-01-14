# External API Contracts: RAG Pipeline

**Date**: 2026-01-12
**Feature**: 001-rag-pipeline

## 1. Cohere Embed API

### Endpoint

```
POST https://api.cohere.ai/v1/embed
```

### Request

```json
{
  "texts": ["chunk 1 content", "chunk 2 content", "..."],
  "model": "embed-english-v3.0",
  "input_type": "search_document",
  "truncate": "END"
}
```

### Request Headers

```
Authorization: Bearer {COHERE_API_KEY}
Content-Type: application/json
```

### Request Constraints

| Parameter | Constraint |
|-----------|------------|
| texts | Max 96 items per request |
| text length | Max 512 tokens per text |
| input_type | `search_document` for ingestion |

### Response (Success - 200)

```json
{
  "id": "abc123",
  "texts": ["chunk 1 content", "chunk 2 content"],
  "embeddings": [
    [0.123, -0.456, 0.789, ...],  // 1024 floats
    [0.321, -0.654, 0.987, ...]   // 1024 floats
  ],
  "meta": {
    "api_version": { "version": "1" },
    "billed_units": { "input_tokens": 150 }
  }
}
```

### Response (Error - 429 Rate Limit)

```json
{
  "message": "You have exceeded the rate limit. Please try again later."
}
```

**Retry Strategy**: Exponential backoff starting at 60s, max 3 retries

### Response (Error - 401 Unauthorized)

```json
{
  "message": "invalid api token"
}
```

## 2. Qdrant REST API

### Base URL

```
https://{cluster-id}.{region}.cloud.qdrant.io:6333
```

### Authentication

```
api-key: {QDRANT_API_KEY}
```

---

### Create Collection

```
PUT /collections/{collection_name}
```

**Request Body**:
```json
{
  "vectors": {
    "size": 1024,
    "distance": "Cosine"
  }
}
```

**Response (200)**:
```json
{
  "result": true,
  "status": "ok",
  "time": 0.023
}
```

---

### Upsert Points

```
PUT /collections/{collection_name}/points
```

**Request Body**:
```json
{
  "points": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "vector": [0.123, -0.456, ...],
      "payload": {
        "source_url": "https://...",
        "section_title": "Introduction",
        "chunk_id": "a1b2c3d4_0",
        "chapter": "module-1-ros2",
        "position": 0,
        "content_hash": "d41d8cd98f00b204e9800998ecf8427e",
        "content": "Original text content..."
      }
    }
  ]
}
```

**Response (200)**:
```json
{
  "result": {
    "operation_id": 123,
    "status": "completed"
  },
  "status": "ok",
  "time": 0.045
}
```

**Batch Size**: Max 100 points per request

---

### Search Points

```
POST /collections/{collection_name}/points/search
```

**Request Body**:
```json
{
  "vector": [0.123, -0.456, ...],
  "limit": 5,
  "with_payload": true
}
```

**Response (200)**:
```json
{
  "result": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "version": 1,
      "score": 0.89,
      "payload": {
        "source_url": "https://...",
        "section_title": "Introduction",
        "content": "Original text..."
      }
    }
  ],
  "status": "ok",
  "time": 0.012
}
```

---

### Get Collection Info

```
GET /collections/{collection_name}
```

**Response (200)**:
```json
{
  "result": {
    "status": "green",
    "vectors_count": 187,
    "points_count": 187,
    "segments_count": 1,
    "config": {
      "params": {
        "vectors": {
          "size": 1024,
          "distance": "Cosine"
        }
      }
    }
  },
  "status": "ok",
  "time": 0.001
}
```

---

### Count Points

```
POST /collections/{collection_name}/points/count
```

**Request Body**:
```json
{
  "exact": true
}
```

**Response (200)**:
```json
{
  "result": {
    "count": 187
  },
  "status": "ok",
  "time": 0.002
}
```

## Error Handling Summary

| Service | Error | HTTP Code | Action |
|---------|-------|-----------|--------|
| Cohere | Rate limit | 429 | Retry with backoff |
| Cohere | Invalid key | 401 | Fail with config error |
| Cohere | Server error | 500 | Retry 3x then fail |
| Qdrant | Collection exists | 409 | Ignore (expected) |
| Qdrant | Invalid key | 403 | Fail with config error |
| Qdrant | Quota exceeded | 413 | Fail with storage error |
| Qdrant | Server error | 500 | Retry 3x then fail |
