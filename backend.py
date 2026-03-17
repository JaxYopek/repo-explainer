from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from src.summarizer import GitHubSummarizer
from src.config import Config

app = FastAPI(title="GitHub Repo Summarizer", version="0.1.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepositoryRequest(BaseModel):
    repository_url: str


class RepositorySummary(BaseModel):
    repository: str
    url: str
    language: str
    stars: int
    description: str
    summary: str


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/summarize", response_model=RepositorySummary)
async def summarize_repository(request: RepositoryRequest):
    """
    Summarize a GitHub repository.

    Args:
        request: Repository request containing the GitHub URL.

    Returns:
        Repository summary with metadata and AI-generated analysis.

    Raises:
        HTTPException: If summarization fails or repo is invalid.
    """
    try:
        Config.validate()
        summarizer = GitHubSummarizer()
        result = summarizer.summarize(request.repository_url, use_cache=True)
        return RepositorySummary(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")
