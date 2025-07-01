# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a news clustering API that automatically groups similar news articles and generates summaries for each cluster. The system uses:
- Sentence Transformers for article embeddings (512-dimensional vectors)
- HDBSCAN for automatic clustering without predefined cluster counts
- OpenAI GPT for generating cluster titles and summaries
- FastAPI for the REST API server

## Key Commands

### Running the Server
```bash
python run_server.py
```
The server runs on http://localhost:8000 with automatic reload enabled.

### Running Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_clustering.py

# Run with coverage
pytest --cov=app tests/
```

### Linting and Type Checking
Currently, no linting or type checking tools are configured. Consider adding:
- `ruff` or `flake8` for linting
- `mypy` for type checking

## Architecture Overview

### Service Layer (`app/services/`)
The core business logic is organized into services:

1. **EmbeddingService** (`embedding.py`): Converts article text to 384-dimensional vectors using `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
2. **ClusteringService** (`clustering.py`): Performs HDBSCAN clustering and selects representative articles based on cosine similarity to cluster centroids
3. **SummarizationService** (`summarization.py`): Uses OpenAI GPT API to generate cluster titles (15 chars) and summaries (50 chars)
4. **NewsClusteringService** (`news_clustering.py`): Orchestrates the entire pipeline by coordinating the above services

### API Layer (`app/api/`)
- Single endpoint: `POST /api/v1/cluster`
- Accepts list of articles with id and content
- Returns clusters with titles and summaries

### Models (`app/models/article.py`)
- `Article`: Input article with id and content
- `ArticleCluster`: Output cluster with articles, title, and summary
- `ClusteringRequest/Response`: API request/response models

## Important Implementation Details

1. **Embedding Dimension**: The PRD mentions 512-dimensional vectors, but the actual implementation uses 384 dimensions (the output of the chosen model)

2. **Environment Variables**: Requires `OPENAI_API_KEY` in `.env` file

3. **Error Handling**: The API returns 500 errors with error details. In production, consider hiding internal error details.

4. **Model Loading**: The embedding model is loaded lazily on first use to reduce startup time

5. **Representative Selection**: Uses top 3 articles closest to cluster centroid for summary generation

## Development Rules

1. **README Updates**: Always update README.md when making significant changes to:
   - API endpoints or request/response formats
   - Installation or setup procedures
   - Environment variables or configuration
   - Dependencies or requirements

2. **Testing**: Write tests for new services and API endpoints

3. **Logging**: Use the configured logger for debugging and monitoring

4. **Type Hints**: Maintain type hints for all function parameters and returns

## Performance Considerations

- Target: Process 1,000 articles in under 10 seconds
- Embeddings are computed locally (no API calls)
- GPT API calls are limited to representative articles only (max 3 per cluster)