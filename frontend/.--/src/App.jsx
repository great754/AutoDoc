import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import CreateDocumentPage from './pages/CreateDocumentPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/create-document" element={<CreateDocumentPage />} />
      </Routes>
    </Router>
  );
}

export default App;
