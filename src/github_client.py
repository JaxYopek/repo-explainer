import requests
from typing import Optional, Dict, List
import re


class GitHubClient:
    """Handles interactions with the GitHub API."""

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub client.

        Args:
            token: Optional GitHub API token for higher rate limits.
        """
        self.token = token
        self.headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        """Build request headers with optional authentication."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def parse_repo_url(self, url: str) -> tuple[str, str]:
        """
        Extract owner and repository name from GitHub URL.

        Args:
            url: GitHub repository URL or owner/repo format.

        Returns:
            Tuple of (owner, repo_name).

        Raises:
            ValueError: If URL format is invalid.
        """
        url = url.strip().rstrip("/")

        # Handle https://github.com/owner/repo format
        match = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", url)
        if match:
            return match.group(1), match.group(2)

        # Handle owner/repo format
        if "/" in url and "://" not in url:
            parts = url.split("/")
            if len(parts) == 2:
                return parts[0], parts[1]

        raise ValueError(f"Invalid GitHub URL format: {url}")

    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """
        Fetch repository metadata from GitHub API.

        Args:
            owner: Repository owner username.
            repo: Repository name.

        Returns:
            Dictionary containing repository information.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """
        Fetch the README file content from a repository.

        Args:
            owner: Repository owner username.
            repo: Repository name.

        Returns:
            README content as string, or None if not found.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                # Decode the base64 content
                import base64
                return base64.b64decode(response.json()["content"]).decode()
        except requests.exceptions.HTTPError:
            pass
        return None

    def get_file_tree(self, owner: str, repo: str, path: str = "", depth: int = 0, max_depth: int = 2) -> List[Dict]:
        """
        Recursively fetch the repository file structure.

        Args:
            owner: Repository owner username.
            repo: Repository name.
            path: Current path in the repository.
            depth: Current recursion depth.
            max_depth: Maximum recursion depth to prevent excessive calls.

        Returns:
            List of file/directory information.
        """
        if depth > max_depth:
            return []

        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            items = response.json()

            if not isinstance(items, list):
                return []

            result = []
            for item in items:
                if item["type"] == "dir" and depth < max_depth:
                    result.append({"type": "dir", "name": item["name"], "path": item["path"]})
                elif item["type"] == "file":
                    result.append({"type": "file", "name": item["name"], "path": item["path"], "size": item["size"]})

            return result
        except requests.exceptions.HTTPError:
            return []

    def get_file_content(self, owner: str, repo: str, path: str) -> Optional[str]:
        """
        Fetch content of a specific file from the repository.

        Args:
            owner: Repository owner username.
            repo: Repository name.
            path: File path in repository.

        Returns:
            File content as string, or None if not found.
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{path}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                import base64
                content = response.json().get("content", "")
                return base64.b64decode(content).decode(errors="ignore")
        except requests.exceptions.HTTPError:
            pass
        return None
