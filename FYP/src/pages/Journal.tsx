import React, { useState } from 'react';
import axios from 'axios';
import { getCurrentUser } from '../services/authService';

const Journal = () => {
    const [entry, setEntry] = useState('');
    const user = getCurrentUser();

    const saveEntry = async () => {
        try {
            // This connects to your emotion_data Django app
            await axios.post('http://127.0.0.1:8000/api/emotion-data/', {
                user_id: user.user_id,
                text_content: entry,
                timestamp: new Date().toISOString()
            });
            alert("Journal saved! AI is now analyzing your mood...");
            setEntry('');
        } catch (err) {
            console.error("Save failed", err);
        }
    };

    return (
        <div className="journal-container">
            <h1>Daily Reflection</h1>
            <textarea 
                placeholder="How are you feeling today?" 
                value={entry} 
                onChange={(e) => setEntry(e.target.value)}
            />
            <button onClick={saveEntry} className="main-btn">Save Entry</button>
        </div>
    );
};

export default Journal;