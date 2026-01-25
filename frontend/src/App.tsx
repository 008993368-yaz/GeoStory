import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout';
import Home from './pages/Home';
import StoryCreate from './pages/StoryCreate';

function App() {
  return (
    <Router>
      <AppLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/stories/new" element={<StoryCreate />} />
        </Routes>
      </AppLayout>
    </Router>
  );
}

export default App;
