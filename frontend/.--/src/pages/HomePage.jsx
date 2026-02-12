import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import '../styles/HomePage.css';
import logo from '../assets/image.png';

function HomePage() {
  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (!user) {
      navigate('/');
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    navigate('/');
  };

  const handleCreateDocument = () => {
    navigate('/create-document');
  };

  return (
    <div className="home-container">
      <header className="home-header">
        <img src={logo} alt="Logo" className="home-logo" />
        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <main className="home-main">
        <div className="welcome-section">
          <h2>Welcome to Auto-Document</h2>
          <p>Create comprehensive documentation for your Power Automate flows</p>
        </div>

        <button className="create-document-btn" onClick={handleCreateDocument}>
          Create New Document
        </button>
      </main>
    </div>
  );
}

export default HomePage;
