import React, { useEffect } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { 
  Home, 
  BookOpen, 
  Settings, 
  LogOut, 
  Sparkles, 
  Users, 
  Bell, 
  Activity,
  History 
} from 'lucide-react';
import { getCurrentUser, logout } from '../services/authService';
import './Dashboard.css';

const DashboardLayout: React.FC = () => {
    const navigate = useNavigate();
    const user = getCurrentUser();
    
    // Improved role check: ensures it handles case-sensitivity from Django
    const userRole = user?.role?.toLowerCase();
    const isCoach = userRole === 'coach';
    const isClient = userRole === 'client';

    // SECURITY: Redirect if no user session found
    useEffect(() => {
        if (!user) {
            console.log("No session found, redirecting to login...");
            navigate('/');
        }
    }, [user, navigate]);

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    // Helper to get initials for the avatar (e.g., "Haseeb" -> "HA")
    const getInitials = (name: string) => {
        if (!name) return "??";
        const parts = name.split(' ');
        if (parts.length > 1) {
            return (parts[0][0] + parts[1][0]).toUpperCase();
        }
        return name.substring(0, 2).toUpperCase();
    };

    if (!user) return null; 

    return (
        <div className="dashboard-wrapper">
            <aside className="sidebar">
                <div className="logo-section">
                    <div className="logo-icon"><Sparkles size={24} color="#007AFF" /></div>
                    <div className="logo-text">MindWell AI</div>
                </div>

                <nav className="nav-menu">
                    <p className="menu-label">Main Menu</p>
                    <NavLink to="/dashboard" end className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                        <Home size={20} /> Overview
                    </NavLink>
                    
                    {/* CLIENT SPECIFIC NAVIGATION */}
                    {isClient && (
                        <>
                            <NavLink to="/dashboard/ai-assistant" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                                <Sparkles size={20} /> AI Guidance
                            </NavLink>
                            <NavLink to="/dashboard/mood-tracker" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                                <Activity size={20} /> Emotion Logs
                            </NavLink>
                            <NavLink to="/dashboard/journal" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                                <BookOpen size={20} /> Journal
                            </NavLink>
                        </>
                    )}

                    {/* COACH SPECIFIC NAVIGATION */}
                    {isCoach && (
                        <>
                            <NavLink to="/dashboard/patients" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                                <Users size={20} /> My Clients
                            </NavLink>
                            <NavLink to="/dashboard/session-logs" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                                <History size={20} /> Session Logs
                            </NavLink>
                        </>
                    )}
                    
                    <p className="menu-label">Account</p>
                    <NavLink to="/dashboard/notifications" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                        <Bell size={20} /> Notifications
                    </NavLink>
                    <NavLink to="/dashboard/settings" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                        <Settings size={20} /> Settings
                    </NavLink>
                </nav>

                <div className="sidebar-footer">
                    <div className="user-info-mini">
                        <span className="user-email-text">{user.email}</span>
                    </div>
                    <button className="logout-btn" onClick={handleLogout}>
                        <LogOut size={20} /> Logout
                    </button>
                </div>
            </aside>
            
            <main className="content">
                <header className="top-bar">
                    <div className="welcome-text">
                        <h2>Welcome back, {user.name}</h2>
                        <span className={`role-badge ${isCoach ? 'coach-badge' : 'client-badge'}`}>
                            {isCoach ? 'Clinical Portal' : 'Personal Sanctuary'}
                        </span>
                    </div>
                    
                    <div className="top-bar-actions">
                        <button className="icon-btn" title="Notifications">
                            <Bell size={20} />
                        </button>
                        <div className="user-profile">
                            <div className="avatar">
                                {getInitials(user.name)}
                            </div>
                        </div>
                    </div>
                </header>

                <div className="page-container">
                    {/* This renders the specific page content like Journal or Mood Tracker */}
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default DashboardLayout;