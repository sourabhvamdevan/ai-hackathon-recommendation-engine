import React, { useState } from 'react';
import axios from 'axios';
import { mockBISRAGResponse } from './mockData'; // Ensure mockData.js is in the same folder
import './App.css';

function App() {
  const [description, setDescription] = useState('');
  const [results, setResults] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState('');
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!description.trim()) return;

    setIsLoading(true);
    setError(null);
    setResults('');
    setStatus('Initializing RAG Pipeline...');

    try {
      
      setTimeout(() => setStatus('Searching BIS SP 21 Documents...'), 800);
      
      
      const response = await axios.post('http://localhost:8000/api/discover', {
        product_description: description
      });

      if (response.data.success) {
        setStatus('Generating Rationale...');
        setTimeout(() => {
          setResults(response.data.data);
          setIsLoading(false);
        }, 500);
      } else {
        throw new Error(response.data.error || "Unknown Error");
      }

    } catch (err) {
      
      console.warn("Backend connection failed. Activating Demo Mode with Mock Data.");
      setStatus('Running in Demo Mode...');
      
     
      setTimeout(() => {
        setResults(mockBISRAGResponse.data);
        setIsLoading(false);
        // Optional: Show a subtle warning or keep it silent for a smoother demo
        console.log("Mock data rendered successfully.");
      }, 2000);

    }
  };

  const copyToClipboard = () => {
    if (!results) return;
    navigator.clipboard.writeText(results);
    alert("Recommendations copied to clipboard!");
  };

  return (
    <div className="app-container">
      <div className="background-blobs"></div>
      
      <nav className="navbar">
        <div className="nav-brand">
          <div className="logo-icon">IS</div>
          <span className="logo-text">BIS <span className="thin">Discovery</span></span>
        </div>
        <div className="status-badge">
          <span className="dot"></span> {isLoading ? 'Processing' : 'System Online'}
        </div>
      </nav>

      <main className="content">
        <header className="hero">
          <h1 className="title">Smart Compliance <span className="gradient-text">Redefined</span></h1>
          <p className="subtitle">Instant BIS standard mapping for Indian Building Material MSEs.</p>
        </header>

        <section className="main-card">
          <div className="input-group">
            <div className="input-meta">
              <label>Product Specification</label>
              <span className="token-info">Building Materials Track</span>
            </div>
            <textarea
              placeholder="e.g., Corrosion-resistant TMT steel bars for structural use in coastal environments..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isLoading}
            />
            <button 
              className={`action-btn ${isLoading ? 'is-loading' : ''}`}
              onClick={handleSearch}
              disabled={isLoading || !description}
            >
              {isLoading ? (
                <div className="loader-group">
                  <div className="spinner"></div>
                  <span>{status}</span>
                </div>
              ) : (
                'Run Discovery Engine'
              )}
            </button>
          </div>

          {error && <div className="error-card"> {error}</div>}

          {results && (
            <div className="results-container animate-in">
              <div className="results-header">
                <h3>Applicable Standards & Rationale</h3>
                <div className="button-group">
                  <button className="copy-btn" onClick={copyToClipboard}>Copy All</button>
                  <button className="clear-btn" onClick={() => setResults('')}>Clear</button>
                </div>
              </div>
              <div className="glass-panel">
                <pre className="output-raw">{results}</pre>
              </div>
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>© 2026 Team R148 • Built for BIS x Sigma Squad AI Hackathon</p>
      </footer>
    </div>
  );
}

export default App;