import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Book, Activity, ArrowRight, TrendingUp } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { getCurrentUser } from '../services/authService';
import './Overview.css';

const Overview: React.FC = () => {
    const navigate = useNavigate();
    const user = getCurrentUser();
    const [latestMood, setLatestMood] = useState<any>(null);
    const [entryCount, setEntryCount] = useState(0);

    useEffect(() => {
        const fetchSummary = async () => {
            try {
                // Fetch all data for this client
                const response = await axios.get('http://127.0.0.1:8000/api/emotion-data/?client_id=1');
                if (response.data.length > 0) {
                    setLatestMood(response.data[0]); // Most recent because of our '-emotion_id' order
                    setEntryCount(response.data.length);
                }
            } catch (err) {
                console.error("Failed to fetch summary", err);
            }
        };
        fetchSummary();
    }, []);

    return (
        <motion.div className="overview-container" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <div className="welcome-hero">
                <h1>Peace be with you, {user?.name}</h1>
                <p>You have completed <strong>{entryCount}</strong> reflections this month. Keep up the great work!</p>
            </div>

            <div className="stats-grid">
                {/* Mood Card */}
                <div className="stat-card">
                    <div className="stat-icon mood-bg"><Activity size={24} /></div>
                    <div className="stat-info">
                        <span>Current Vibe</span>
                        <h3>{latestMood?.emotion || "No data"}</h3>
                    </div>
                    <div className="stat-badge">Stable</div>
                </div>

                {/* Resilience Card */}
                <div className="stat-card">
                    <div className="stat-icon resilience-bg"><TrendingUp size={24} /></div>
                    <div className="stat-info">
                        <span>Resilience Score</span>
                        <h3>{latestMood ? `${latestMood.intensity}%` : "--"}</h3>
                    </div>
                </div>
            </div>

            <div className="main-grid">
                {/* Recent Reflection */}
                <div className="content-card journal-preview">
                    <div className="card-header">
                        <h3><Book size={20} /> Latest Reflection</h3>
                        <button onClick={() => navigate('/dashboard/journal')}>View All</button>
                    </div>
                    <div className="preview-body">
                        {latestMood?.notes ? (
                            <p>"{latestMood.notes.substring(0, 150)}..."</p>
                        ) : (
                            <p className="empty-text">You haven't written anything yet. Start your journey today.</p>
                        )}
                    </div>
                </div>

                {/* AI Suggestions */}
                <div className="content-card ai-card">
                    <div className="card-header">
                        <h3><Sparkles size={20} /> AI Suggestion</h3>
                    </div>
                    <div className="ai-body">
                        <p>Based on your {latestMood?.emotion || 'recent'} entries, we recommend a 5-minute breathing exercise to maintain your focus.</p>
                        <button className="action-link">Start Exercise <ArrowRight size={16} /></button>
                    </div>
                </div>
            </div>
        </motion.div>
    );
};

export default Overview;