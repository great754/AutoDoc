import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/CreateDocumentPage.css';

function CreateDocumentPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    businessReason: '',
    processSummary: '',
    stakeholders: '',
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/json') {
      setFile(selectedFile);
    } else {
      alert('Please upload a valid JSON file');
      e.target.value = '';
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Placeholder for future API call
    console.log('Form submitted:', {
      ...formData,
      file: file?.name,
    });

    // Simulate processing
    setTimeout(() => {
      setLoading(false);
      alert('Form submitted successfully! (No action taken yet)');
    }, 1000);
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
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="businessReason">
              Why does this project exist?
              <span className="required">*</span>
            </label>
            <textarea
              id="businessReason"
              name="businessReason"
              value={formData.businessReason}
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
            <textarea
              id="stakeholders"
              name="stakeholders"
              value={formData.stakeholders}
              onChange={handleInputChange}
              placeholder="List the stakeholders involved in this project..."
              rows="3"
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="flowFile">
              Upload Power Automate Flow (JSON)
              <span className="required">*</span>
            </label>
            <input
              type="file"
              id="flowFile"
              accept=".json"
              onChange={handleFileChange}
              required
              disabled={loading}
            />
            {file && (
              <div className="file-info">
                Selected: {file.name}
              </div>
            )}
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
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default CreateDocumentPage;
