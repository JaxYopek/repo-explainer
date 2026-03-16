#!/usr/bin/env python3
"""Entry point for the GitHub repository summarizer."""

import sys
import argparse
import json

from src.summarizer import GitHubSummarizer
from src.config import Config


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate AI-powered summaries of GitHub repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://github.com/openai/gpt-4
  python main.py openai/gpt-4
        """,
    )

    parser.add_argument("repository", help="GitHub repository URL or owner/repo format")
    parser.add_argument("--no-cache", action="store_true", help="Ignore cached summaries")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    try:
        # Validate configuration
        Config.validate()

        # Create summarizer and generate summary
        summarizer = GitHubSummarizer()
        result = summarizer.summarize(args.repository, use_cache=not args.no_cache)

        if args.raw:
            print(json.dumps(result, indent=2))
        else:
            print(f"\n📦 Repository: {result['repository']}")
            print(f"🔗 URL: {result['url']}")
            print(f"⭐ Stars: {result['stars']}")
            print(f"🛠️ Language: {result['language']}")
            print(f"\n📝 Summary:\n{result['summary']}")
            print("\n")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
