import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Smile, Frown, Meh, AlertCircle, Calendar, Plus, Activity } from 'lucide-react';
import axios from 'axios';
import { getCurrentUser } from '../services/authService';
import './MoodTracker.css';

const MoodTracker: React.FC = () => {
    const [selectedMood, setSelectedMood] = useState<number | null>(null);
    const [history, setHistory] = useState([]);
    const [isSaving, setIsSaving] = useState(false);
    const user = getCurrentUser();

    // 1. FETCH HISTORY FROM DJANGO
    useEffect(() => {
        const fetchMoods = async () => {
            try {
                // We filter by client_id (hardcoded as 1 for now until your client profile is ready)
                const response = await axios.get('http://127.0.0.1:8000/api/emotion-data/?client_id=1');
                
                // Format Django data for the Recharts Chart
                const formattedData = response.data.map((item: any) => ({
                    date: new Date(item.created_at || Date.now()).toLocaleDateString('en-US', { weekday: 'short' }),
                    score: item.intensity / 20, // Scale 0-100 down to 0-5
                    label: item.emotion
                }));
                setHistory(formattedData);
            } catch (err) {
                console.error("Failed to fetch mood history", err);
            }
        };
        fetchMoods();
    }, []);

    // 2. SAVE MOOD TO DJANGO
    const handleSaveMood = async () => {
        if (selectedMood === null) {
            alert("Please select an emoji first!");
            return;
        }

        const moodObj = moodOptions.find(m => m.level === selectedMood);
        
        const data = {
            client_id: 1, // Change this to your actual client ID later
            session_id: 1, // Change this to your actual session ID later
            emotion: moodObj?.label,
            intensity: selectedMood * 20 // Convert 1-5 scale to 0-100 for your model
        };

        try {
            setIsSaving(true);
            await axios.post('http://127.0.0.1:8000/api/emotion-data/', data);
            alert("Mood logged successfully!");
            window.location.reload(); // Refresh to see the new point on the chart
        } catch (err: any) {
            console.error("Save failed", err.response?.data);
            alert("Error saving mood. Make sure Client #1 and Session #1 exist in Django Admin.");
        } finally {
            setIsSaving(false);
        }
    };

    const moodOptions = [
        { level: 1, icon: <Frown />, label: 'Low', color: '#EB5757' },
        { level: 2, icon: <Meh />, label: 'Anxious', color: '#F2994A' },
        { level: 3, icon: <Meh />, label: 'Neutral', color: '#F2C94C' },
        { level: 4, icon: <Smile />, label: 'Good', color: '#27AE60' },
        { level: 5, icon: <Smile />, label: 'Great', color: '#2D9CDB' },
    ];

    return (
        <motion.div className="mood-container" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <header className="page-header">
                <div>
                    <h1>Mood Analytics</h1>
                    <p>Tracking your emotional resilience over time.</p>
                </div>
                <div className="risk-indicator-chip">
                    <AlertCircle size={16} /> 
                    <span>Stability: <strong>High</strong></span>
                </div>
            </header>

            <section className="chart-section">
                <div className="chart-header">
                    <h3>Weekly Emotional Trend</h3>
                </div>
                <div className="chart-wrapper">
                    <ResponsiveContainer width="100%" height={300}>
                        <AreaChart data={history.length > 0 ? history : []}>
                            <defs>
                                <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#007AFF" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#007AFF" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                            <XAxis dataKey="date" stroke="#636366" axisLine={false} tickLine={false} />
                            <YAxis domain={[0, 5]} hide />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#1c1c1e', border: '1px solid #3a3a3c', borderRadius: '10px' }}
                                itemStyle={{ color: '#fff' }}
                            />
                            <Area 
                                type="monotone" 
                                dataKey="score" 
                                stroke="#007AFF" 
                                fillOpacity={1} 
                                fill="url(#colorScore)" 
                                strokeWidth={3}
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </section>

            <div className="mood-grid-layout">
                <section className="log-mood-card">
                    <h3>How are you right now?</h3>
                    <div className="mood-selector">
                        {moodOptions.map((mood) => (
                            <button 
                                key={mood.level}
                                className={`mood-btn ${selectedMood === mood.level ? 'active' : ''}`}
                                onClick={() => setSelectedMood(mood.level)}
                                style={{ '--active-color': mood.color } as any}
                            >
                                {mood.icon}
                                <span>{mood.label}</span>
                            </button>
                        ))}
                    </div>
                    <textarea placeholder="Any specific triggers? (Optional)" className="mood-note"></textarea>
                    <button 
                        className="submit-mood-btn" 
                        onClick={handleSaveMood}
                        disabled={isSaving}
                    >
                        {isSaving ? "Saving..." : <><Plus size={18} /> Save Entry</>}
                    </button>
                </section>

                <section className="insights-card">
                    <h3>AI Insights</h3>
                    <div className="insight-item">
                        <Calendar size={18} color="#007AFF" />
                        <p>Total logs found: <strong>{history.length}</strong></p>
                    </div>
                </section>
            </div>
        </motion.div>
    );
};

export default MoodTracker;