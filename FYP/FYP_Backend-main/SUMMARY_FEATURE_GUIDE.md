# Session Summary Feature - Implementation Guide

## Overview
The system now automatically generates a conversation summary and tracks the final emotion when a chat session ends.

## Backend Changes

### 1. Database Schema Updates
Added to `session_log` model:
- `summary` (TextField): AI-generated conversation summary
- `final_emotion` (CharField): Last detected emotion from the user
- `emotion_intensity` (IntegerField): Average emotional intensity throughout session

### 2. New API Endpoint
**POST** `/api/sessions/<session_id>/summary/`

Generates and saves:
- Comprehensive conversation summary
- Final user emotion
- Average emotion intensity
- Message count and session metadata

**Example Request:**
```javascript
POST http://127.0.0.1:8000/api/sessions/1/summary/
```

**Example Response:**
```json
{
  "session_id": 1,
  "summary": "The client discussed feelings of anxiety related to work stress...",
  "final_emotion": "hopeful",
  "emotion_intensity": 6,
  "message_count": 15,
  "session_date": "2026-01-04"
}
```

### 3. Updated GET Endpoint
**GET** `/api/sessions/<session_id>/`

Now includes `summary`, `final_emotion`, and `emotion_intensity` fields in response.

## Frontend Integration

### Option 1: Add "End Session" Button in AIGuidance.tsx

```tsx
import { Download, XCircle } from 'lucide-react';

// Add state for session
const [sessionId, setSessionId] = useState(1); // Get from your session management
const [showSummary, setShowSummary] = useState(false);
const [sessionSummary, setSessionSummary] = useState<any>(null);

// Add function to end session
const endSession = async () => {
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/api/sessions/${sessionId}/summary/`
    );
    
    setSessionSummary(response.data);
    setShowSummary(true);
    
    // Optional: Navigate to dashboard
    // navigate('/dashboard');
  } catch (err) {
    console.error("Failed to generate summary:", err);
  }
};

// Add button in your UI
<button 
  className="end-session-btn" 
  onClick={endSession}
  title="End Session & Generate Summary"
>
  <XCircle size={20} />
  End Session
</button>

// Add Summary Modal/Display
{showSummary && sessionSummary && (
  <div className="summary-modal">
    <div className="summary-content">
      <h2>Session Summary</h2>
      <div className="emotion-display">
        <span className="emotion-label">Final Emotion:</span>
        <span className="emotion-value">{sessionSummary.final_emotion}</span>
        <span className="intensity">Intensity: {sessionSummary.emotion_intensity}/10</span>
      </div>
      <div className="summary-text">
        <h3>Conversation Summary:</h3>
        <p>{sessionSummary.summary}</p>
      </div>
      <div className="meta-info">
        <p>Messages: {sessionSummary.message_count}</p>
        <p>Date: {sessionSummary.session_date}</p>
      </div>
      <button onClick={() => setShowSummary(false)}>Close</button>
    </div>
  </div>
)}
```

### Option 2: Dashboard Integration

Create a dashboard component to display all session summaries:

```tsx
// Dashboard.tsx
const fetchSessionSummaries = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/sessions/?client_id=${user.id}`
    );
    
    // Filter sessions that have summaries
    const completedSessions = response.data.filter(
      (session: any) => session.summary
    );
    
    setSessionHistory(completedSessions);
  } catch (err) {
    console.error("Failed to fetch summaries:", err);
  }
};

// Display in dashboard
{sessionHistory.map((session) => (
  <div key={session.session_id} className="session-card">
    <div className="session-header">
      <h3>Session {session.session_id}</h3>
      <span className="date">{session.date}</span>
    </div>
    
    <div className="emotion-indicator">
      <span className={`emotion-badge ${session.final_emotion}`}>
        {session.final_emotion}
      </span>
      <span className="intensity-bar">
        <div 
          className="intensity-fill" 
          style={{ width: `${session.emotion_intensity * 10}%` }}
        />
      </span>
    </div>
    
    <div className="summary-preview">
      <p>{session.summary}</p>
    </div>
    
    <button onClick={() => viewFullSession(session.session_id)}>
      View Details
    </button>
  </div>
))}
```

## Usage Flow

1. **During Chat**: Emotions are detected and tracked for each message
2. **End Session**: User clicks "End Session" button
3. **Summary Generation**: 
   - System retrieves all conversation messages
   - AI generates comprehensive summary
   - Calculates final emotion and average intensity
   - Saves to database
4. **Display**: Summary shown immediately or accessible from dashboard

## CSS Styling Example

```css
.end-session-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  transition: transform 0.2s;
}

.end-session-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.summary-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.summary-content {
  background: white;
  padding: 32px;
  border-radius: 16px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.emotion-display {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-radius: 8px;
  margin: 16px 0;
}

.emotion-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  text-transform: capitalize;
}

.intensity {
  margin-left: auto;
  padding: 4px 12px;
  background: #667eea;
  color: white;
  border-radius: 20px;
  font-size: 0.875rem;
}

.summary-text {
  margin: 24px 0;
  line-height: 1.6;
  color: #333;
}
```

## Testing

1. **Run migrations**: Already completed
2. **Start Django server**: `python manage.py runserver`
3. **Test endpoint**:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/sessions/1/summary/
   ```
4. **Verify in database**: Check session_log table for new fields

## Next Steps

1. Add "End Session" button to your AI chat interface
2. Create dashboard view for session history
3. Add export/download functionality for summaries
4. Implement email notifications with session summaries
5. Add analytics for emotion trends over multiple sessions
