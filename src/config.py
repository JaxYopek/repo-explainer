import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration management."""

    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    cache_dir = os.getenv("CACHE_DIR", "./cache")
    github_token = os.getenv("GITHUB_TOKEN", "")

    @staticmethod
    def validate():
        """Validate that all required configuration is present."""
        if not Config.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return True


# Ensure cache directory exists
os.makedirs(Config.cache_dir, exist_ok=True)
