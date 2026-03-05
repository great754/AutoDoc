import { useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import '../styles/HomePage.css';
import logo from '../assets/image.png';

const API_BASE_URL = 'http://localhost:8000';

function HomePage() {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [projectsLoading, setProjectsLoading] = useState(true);

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (!user) {
      navigate('/');
    }
  }, [navigate]);

  // Fetch previous projects
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/process/`);
        if (response.ok) {
          const data = await response.json();
          setProjects(data);
        }
      } catch (err) {
        console.error('Failed to load projects:', err);
      } finally {
        setProjectsLoading(false);
      }
    };
    fetchProjects();
  }, []);

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

        {/* Previous Projects Section */}
        {projects.length > 0 && (
          <section className="previous-projects-section">
            <h2>Recent Projects</h2>
            <div className="projects-grid">
              {projects.map((project) => (
                <div
                  key={project.id}
                  className="project-card"
                  onClick={() => navigate(`/process/${project.id}`)}
                >
                  <div className="project-card-header">
                    <h3>{project.project_name}</h3>
                    <span className={`status-badge status-${project.status}`}>
                      {project.status}
                    </span>
                  </div>
                  <p className="project-purpose">{project.purpose}</p>
                  <div className="project-footer">
                    <span className="project-date">
                      {new Date(project.created_at).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default HomePage;
