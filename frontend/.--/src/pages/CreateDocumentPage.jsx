import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/CreateDocumentPage.css';

const API_BASE_URL = 'http://localhost:8000';

function CreateDocumentPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    projectName: '',
    purpose: '',
    processSummary: '',
    stakeholders: '',
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    setError(null); // Clear error when user types
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && (selectedFile.type === 'application/xml' || selectedFile.type === 'text/xml' || selectedFile.name.endsWith('.xml'))) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please upload a valid XML file');
      e.target.value = '';
    }
  };

  const parseStakeholders = (stakeholdersText) => {
    /**
     * Parse stakeholders from text format:
     * "John Doe - Finance Manager\nJane Smith - Approver"
     * Returns array of {name, role} objects
     */
    return stakeholdersText
      .split('\n')
      .map((line) => {
        const [name, role] = line.split('-').map((s) => s.trim());
        return { name, role: role || 'Stakeholder' };
      })
      .filter((s) => s.name);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Validate required fields
      if (!formData.projectName.trim()) {
        throw new Error('Project name is required');
      }
      if (!formData.purpose.trim()) {
        throw new Error('Purpose is required');
      }
      if (!formData.processSummary.trim()) {
        throw new Error('Process summary is required');
      }
      if (!formData.stakeholders.trim()) {
        throw new Error('Stakeholders are required');
      }
      if (!file) {
        throw new Error('Power Automate flow file is required');
      }

      // Parse stakeholders
      const stakeholders = parseStakeholders(formData.stakeholders);
      if (stakeholders.length === 0) {
        throw new Error('Please enter stakeholders in format: "Name - Role" (one per line)');
      }

      // Create FormData for multipart request (needed for file upload)
      const submitData = new FormData();
      submitData.append('project_name', formData.projectName);
      submitData.append('purpose', formData.purpose);
      submitData.append('business_summary', formData.processSummary);
      submitData.append('stakeholders', JSON.stringify(stakeholders));
      submitData.append('flow_file', file);

      // Make API call
      const response = await fetch(`${API_BASE_URL}/process/`, {
        method: 'POST',
        body: submitData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create process');
      }

      const result = await response.json();
      setSuccess(true);

      // Redirect to process details page after 2 seconds
      setTimeout(() => {
        navigate(`/process/${result.id}`);
      }, 2000);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/home');
  };

  return (
    <div className="create-document-container">
      <header className="create-document-header">
        <h1>Create New Document</h1>
        <button className="back-btn" onClick={handleCancel}>
          Back to Home
        </button>
      </header>

      <main className="form-container">
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">✓ Process created successfully! Redirecting...</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="projectName">
              Project Name
              <span className="required">*</span>
            </label>
            <input
              type="text"
              id="projectName"
              name="projectName"
              value={formData.projectName}
              onChange={handleInputChange}
              placeholder="e.g., Invoice Processing Automation"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="purpose">
              Why does this project exist?
              <span className="required">*</span>
            </label>
            <textarea
              id="purpose"
              name="purpose"
              value={formData.purpose}
              onChange={handleInputChange}
              placeholder="Describe the business reason for this project..."
              rows="4"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="processSummary">
              High level summary of what the process does
              <span className="required">*</span>
            </label>
            <textarea
              id="processSummary"
              name="processSummary"
              value={formData.processSummary}
              onChange={handleInputChange}
              placeholder="Describe step by step what the process does..."
              rows="6"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="stakeholders">
              Who are the stakeholders?
              <span className="required">*</span>
            </label>
            <span className="helper-text">
              Format: "Name - Role" (one per line). Example: "John Doe - Finance Manager"
            </span>
            <textarea
              id="stakeholders"
              name="stakeholders"
              value={formData.stakeholders}
              onChange={handleInputChange}
              placeholder="John Doe - Finance Manager&#10;Jane Smith - Approver"
              rows="3"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="flowFile">
              Upload Power Automate Flow (XML)
              <span className="required">*</span>
            </label>
            <input
              type="file"
              id="flowFile"
              accept=".xml"
              onChange={handleFileChange}
              required
              disabled={loading}
            />
            {file && <div className="file-info">✓ Selected: {file.name}</div>}
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="cancel-btn"
              onClick={handleCancel}
              disabled={loading}
            >
              Cancel
            </button>
            <button type="submit" className="submit-btn" disabled={loading || success}>
              {loading ? 'Submitting...' : success ? 'Submitted!' : 'Submit'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default CreateDocumentPage;
