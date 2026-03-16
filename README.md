# GitHub Repo Summarizer

A tool that generates concise summaries of GitHub repositories using AI, analyzing code structure, documentation, and key components to provide meaningful insights.

## Features

- Fetches repository metadata and file structure from GitHub
- Analyzes README, main files, and directory layout
- Generates comprehensive summaries using OpenAI's GPT models
- Caches results to minimize API calls
- Supports both GitHub URLs and owner/repo format

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd repo-explainer
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Usage

### Command line:
```bash
python main.py https://github.com/owner/repo-name
```

### As a module:
```python
from src.summarizer import GitHubSummarizer

summarizer = GitHubSummarizer(api_key="your-openai-key")
summary = summarizer.summarize("https://github.com/owner/repo-name")
print(summary)
```

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (default: gpt-4o-mini)
- `CACHE_DIR` - Directory for caching summaries (default: ./cache)
- `GITHUB_TOKEN` - Optional GitHub token for higher rate limits

## Project Structure

```
repo-explainer/
├── src/
│   ├── summarizer.py      # Core summarization logic
│   ├── github_client.py    # GitHub API interactions
│   └── config.py           # Configuration management
├── main.py                 # Entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

## License

MIT
