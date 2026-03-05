import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/ProcessDetailPage.css';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const API_BASE_URL = 'http://localhost:8000';

function ProcessDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [process, setProcess] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);

  // Fetch process details
  useEffect(() => {
    const fetchProcess = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await fetch(`${API_BASE_URL}/process/${id}`);

        if (!response.ok) {
          throw new Error(`Failed to load process (${response.status})`);
        }

        const data = await response.json();
        setProcess(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchProcess();
    }
  }, [id]);

  const handleAnalyze = async () => {
    if (!process) return;

    setAnalyzing(true);
    setAnalysisError(null);

    try {
      // Trigger analysis
      const response = await fetch(`${API_BASE_URL}/process/${id}/analyze`, {
        method: 'POST',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to start analysis');
      }

      // Poll for completion
      let attempts = 0;
      const maxAttempts = 300; // 5 minutes with 1 second intervals
      const pollInterval = 1000; // 1 second

      const pollAnalysis = async () => {
        try {
          const checkResponse = await fetch(`${API_BASE_URL}/process/${id}`);
          if (!checkResponse.ok) throw new Error('Failed to check status');

          const updatedProcess = await checkResponse.json();
          setProcess(updatedProcess);

          if (updatedProcess.status === 'processed' || updatedProcess.status === 'error') {
            return; // Analysis complete
          }

          attempts++;
          if (attempts < maxAttempts) {
            setTimeout(pollAnalysis, pollInterval);
          } else {
            setAnalysisError('Analysis took too long. Please check back later.');
          }
        } catch (err) {
          setAnalysisError(`Poll error: ${err.message}`);
        }
      };

      // Start polling after a brief delay
      setTimeout(pollAnalysis, pollInterval);
    } catch (err) {
      setAnalysisError(err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleBackHome = () => {
    navigate('/home');
  };

  if (loading) {
    return (
      <div className="process-detail-container">
        <header className="process-header">
          <h1>Process Details</h1>
          <button className="back-btn" onClick={handleBackHome}>
            Back to Home
          </button>
        </header>
        <div className="loading-message">Loading process details...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="process-detail-container">
        <header className="process-header">
          <h1>Process Details</h1>
          <button className="back-btn" onClick={handleBackHome}>
            Back to Home
          </button>
        </header>
        <div className="error-message">Error: {error}</div>
      </div>
    );
  }

  if (!process) {
    return (
      <div className="process-detail-container">
        <header className="process-header">
          <h1>Process Details</h1>
          <button className="back-btn" onClick={handleBackHome}>
            Back to Home
          </button>
        </header>
        <div className="error-message">Process not found</div>
      </div>
    );
  }

  return (
    <div className="process-detail-container">
      <header className="process-header">
        <h1>Process Details</h1>
        <button className="back-btn" onClick={handleBackHome}>
          Back to Home
        </button>
      </header>

      <main className="process-main">
        {/* Process Metadata Section */}
        <section className="metadata-section">
          <h2>{process.project_name}</h2>

          <div className="metadata-grid">
            <div className="metadata-item">
              <h3>Purpose</h3>
              <p>{process.purpose}</p>
            </div>

            <div className="metadata-item">
              <h3>Business Summary</h3>
              <p>{process.business_summary}</p>
            </div>

            <div className="metadata-item">
              <h3>Stakeholders</h3>
              <ul className="stakeholder-list">
                {process.stakeholders.map((stakeholder, idx) => (
                  <li key={idx}>
                    <strong>{stakeholder.name}</strong> - {stakeholder.role}
                  </li>
                ))}
              </ul>
            </div>

            {process.flow_filename && (
              <div className="metadata-item">
                <h3>Power Automate Flow</h3>
                <p className="file-name">📄 {process.flow_filename}</p>
              </div>
            )}

            <div className="metadata-item">
              <h3>Status</h3>
              <p className={`status-badge status-${process.status}`}>{process.status}</p>
            </div>

            <div className="metadata-item">
              <h3>Created</h3>
              <p>{new Date(process.created_at).toLocaleString()}</p>
            </div>
          </div>
        </section>

        {/* Analysis Section */}
        <section className="analysis-section">
          <div className="analysis-header">
            <h2>AI Analysis</h2>
            {process.status !== 'processed' && !analyzing && (
              <button
                className="analyze-btn"
                onClick={handleAnalyze}
                disabled={analyzing}
              >
                Generate Documentation
              </button>
            )}
            {analyzing && <span className="analyzing-indicator">Analyzing...</span>}
          </div>

          {analysisError && (
            <div className="error-message">{analysisError}</div>
          )}

          {process.error_message && process.status === 'error' && (
            <div className="error-message">Analysis failed: {process.error_message}</div>
          )}

          {process.status === 'pending' && !analyzing && (
            <div className="pending-message">
              Click "Generate Documentation" to start AI analysis of your process.
            </div>
          )}

          {process.status === 'processing' && (
            <div className="processing-message">
              ⏳ Analysis in progress... This may take a few minutes.
            </div>
          )}

          {process.status === 'processed' && process.ollama_analysis && (
            <div className="analysis-content">
              <div className="markdown-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {process.ollama_analysis}
                </ReactMarkdown>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default ProcessDetailPage;
