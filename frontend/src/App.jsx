import { useState } from 'react';
import axios from 'axios';
import './App.css';

export default function App() {
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSummary(null);
    setLoading(true);

    try {
      const response = await axios.post('/api/summarize', {
        repository_url: url,
      });
      setSummary(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          err.message ||
          'Failed to summarize repository'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>GitHub Repo Summarizer</h1>
        <p>Get AI-powered summaries of any public GitHub repository</p>
      </div>

      <form onSubmit={handleSubmit} className="search-form">
        <div className="input-group">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter GitHub URL (e.g., https://github.com/owner/repo)"
            disabled={loading}
            className="url-input"
          />
          <button
            type="submit"
            disabled={!url || loading}
            className="submit-button"
          >
            {loading ? 'Analyzing...' : 'Summarize'}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {summary && (
        <div className="summary-card">
          <div className="summary-header">
            <h2>{summary.repository}</h2>
            <a href={summary.url} target="_blank" rel="noopener noreferrer">
              View on GitHub →
            </a>
          </div>

          <div className="summary-metadata">
            <div className="metadata-item">
              <span className="label">Language:</span>
              <span className="value">{summary.language || 'N/A'}</span>
            </div>
            <div className="metadata-item">
              <span className="label">Stars:</span>
              <span className="value">⭐ {summary.stars}</span>
            </div>
          </div>

          {summary.description && (
            <div className="description">
              <strong>Description:</strong>
              <p>{summary.description}</p>
            </div>
          )}

          <div className="summary-content">
            <h3>Summary</h3>
            <p>{summary.summary}</p>
          </div>
        </div>
      )}

      {!summary && !error && !loading && (
        <div className="welcome-message">
          <p>Paste a GitHub repository URL above to get started!</p>
        </div>
      )}
    </div>
  );
}
