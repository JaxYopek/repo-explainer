import json
import hashlib
import os
from pathlib import Path
from typing import Optional
from openai import OpenAI

from .github_client import GitHubClient
from .config import Config


class GitHubSummarizer:
    """Core summarization engine for GitHub repositories."""

    def __init__(self, api_key: Optional[str] = None, github_token: Optional[str] = None):
        """
        Initialize the summarizer.

        Args:
            api_key: OpenAI API key. Defaults to environment variable.
            github_token: Optional GitHub API token.
        """
        self.api_key = api_key or Config.openai_api_key
        self.github_token = github_token or Config.github_token
        self.client = OpenAI(api_key=self.api_key)
        self.github = GitHubClient(token=self.github_token)
        self.cache_dir = Path(Config.cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, owner: str, repo: str) -> str:
        """Generate a cache key for a repository."""
        key = f"{owner}/{repo}".encode()
        return hashlib.sha256(key).hexdigest()

    def _load_cache(self, owner: str, repo: str) -> Optional[dict]:
        """Load cached summary if available."""
        cache_file = self.cache_dir / f"{self._get_cache_key(owner, repo)}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def _save_cache(self, owner: str, repo: str, data: dict) -> None:
        """Save summary to cache."""
        cache_file = self.cache_dir / f"{self._get_cache_key(owner, repo)}.json"
        try:
            with open(cache_file, "w") as f:
                json.dump(data, f)
        except Exception:
            pass

    def _extract_key_files(self, owner: str, repo: str) -> dict:
        """Extract content from important files in the repository."""
        key_files = {
            "readme": None,
            "package_info": None,
            "structure": None,
        }

        # Get README
        readme = self.github.get_readme(owner, repo)
        if readme:
            key_files["readme"] = readme[:2000]  # Limit to first 2000 chars

        # Try to get package.json or setup.py for quick project info
        package_json = self.github.get_file_content(owner, repo, "package.json")
        if package_json:
            key_files["package_info"] = package_json[:1000]
        else:
            setup_py = self.github.get_file_content(owner, repo, "setup.py")
            if setup_py:
                key_files["package_info"] = setup_py[:1000]

        # Get file tree structure
        tree = self.github.get_file_tree(owner, repo)
        key_files["structure"] = str(tree)[:1000]

        return key_files

    def summarize(self, repo_url: str, use_cache: bool = True) -> dict:
        """
        Generate a summary of a GitHub repository.

        Args:
            repo_url: GitHub repository URL or owner/repo format.
            use_cache: Whether to use cached summaries.

        Returns:
            Dictionary containing the summary and metadata.
        """
        owner, repo = self.github.parse_repo_url(repo_url)

        # Check cache
        if use_cache:
            cached = self._load_cache(owner, repo)
            if cached:
                return cached

        # Fetch repository information
        repo_info = self.github.get_repo_info(owner, repo)
        key_files = self._extract_key_files(owner, repo)

        # Build context for AI summarization
        context = f"""
Repository: {repo_info.get('full_name')}
URL: {repo_info.get('html_url')}
Description: {repo_info.get('description', 'No description')}
Language: {repo_info.get('language', 'Unknown')}
Stars: {repo_info.get('stargazers_count')}
Forks: {repo_info.get('forks_count')}
Open Issues: {repo_info.get('open_issues_count')}

README Content (excerpt):
{key_files.get('readme', 'No README found')}

Package/Setup Info:
{key_files.get('package_info', 'No package info found')}

Repository Structure:
{key_files.get('structure', 'Could not retrieve structure')}
"""

        # Generate summary using OpenAI
        response = self.client.chat.completions.create(
            model=Config.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a technical expert who creates concise, accurate summaries of GitHub repositories. Provide practical insights about the project's purpose, main features, technology stack, and potential use cases.",
                },
                {
                    "role": "user",
                    "c                    pip install pyyaml==6.0.1ntent": f"Please provide a comprehensive summary of this GitHub repository:\n\n{context}",
                },
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        summary_text = response.choices[0].message.content

        result = {
            "repository": repo_info.get("full_name"),
            "url": repo_info.get("html_url"),
            "language": repo_info.get("language"),
            "stars": repo_info.get("stargazers_count"),
            "description": repo_info.get("description"),
            "summary": summary_text,
        }

        # Cache the result
        self._save_cache(owner, repo, result)

        return result
