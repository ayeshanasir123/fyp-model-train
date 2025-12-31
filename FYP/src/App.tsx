import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Auth from './pages/Auth';
import DashboardLayout from './pages/Dashboard'; // Ensure this file has the <Outlet />
import Overview from './pages/Overview';
import Journal from './pages/Journal';
import MoodTracker from './pages/MoodTracker';
import Patients from './pages/Patients';
import AIGuidance from './pages/AIGuidance'; // <--- ADDED THIS

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Route: Login/Signup */}
        <Route path="/" element={<Auth />} />

        {/* Protected Dashboard Routes */}
        <Route path="/dashboard" element={<DashboardLayout />}>
          
          {/* Default view: /dashboard */}
          <Route index element={<Overview />} />
          
          {/* Client Specific Routes */}
          <Route path="journal" element={<Journal />} />
          <Route path="mood-tracker" element={<MoodTracker />} />
          <Route path="ai-assistant" element={<AIGuidance />} /> {/* <--- ADDED THIS */}
          
          {/* Coach Specific Routes */}
          <Route path="patients" element={<Patients />} />
          
          {/* Dashboard Catch-all: Redirects unknown dashboard paths to Overview */}
          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Route>

        {/* Global Catch-all: Redirects everything else to Login */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;