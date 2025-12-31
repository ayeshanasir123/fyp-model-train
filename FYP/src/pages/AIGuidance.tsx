import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Sparkles, Shield, User, Bot, Mic, MicOff } from 'lucide-react'; // Added Mic icons
import axios from 'axios';
import { getCurrentUser } from '../services/authService';
import './AIGuidance.css';

interface Message {
    id: string | number;
    text: string;
    sender: 'user' | 'ai';
    timestamp: Date;
    emotion?: string;        // NEW: detected emotion
    emotionConfidence?: number; // NEW: confidence score
    emotionIntensity?: number;  // NEW: intensity (1-10)
}

const AIGuidance: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [isListening, setIsListening] = useState(false); // New state for voice
    const scrollRef = useRef<HTMLDivElement>(null);
    const user = getCurrentUser();

    // Voice to Text Logic
    const startListening = () => {
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            alert("Your browser does not support voice recognition. Please try Chrome or Edge.");
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = false; // Stops after one sentence
        recognition.interimResults = false;

        recognition.onstart = () => {
            setIsListening(true);
        };

        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setInput(transcript); // Set transcribed text to input field
            setIsListening(false);
        };

        recognition.onerror = (event: any) => {
            console.error("Speech Recognition Error:", event.error);
            setIsListening(false);
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        recognition.start();
    };

    // 1. Fetch Chat History on Load
    useEffect(() => {
        const fetchHistory = async () => {
            if (!user?.id) return;

            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/ai-guidance/?client_id=${user.id}`);
                
                const history = response.data.flatMap((chat: any) => [
                    { 
                        id: `u-${chat.guidance_id}`, 
                        text: chat.user_message, 
                        sender: 'user', 
                        timestamp: new Date(chat.created_at) 
                    },
                    { 
                        id: `a-${chat.guidance_id}`, 
                        text: chat.ai_response, 
                        sender: 'ai', 
                        timestamp: new Date(chat.created_at) 
                    }
                ]);
                
                setMessages(history.length > 0 ? history : [{ id: 1, text: "Welcome back. How are you feeling?", sender: 'ai', timestamp: new Date() }]);
            } catch (err) {
                console.error("Failed to load history", err);
            }
        };
        fetchHistory();
    }, [user?.id]);

    useEffect(() => {
        scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // 2. Real HandleSend with Django/Gemini Integration + Emotion Detection
    const handleSend = async () => {
        if (!input.trim()) return;

        const userMsg: Message = { id: Date.now(), text: input, sender: 'user', timestamp: new Date() };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsTyping(true);

        try {
            // Send message WITHOUT dummy emotion_id - backend will detect it!
            const response = await axios.post('http://127.0.0.1:8000/api/ai-guidance/', {
                client_id: user?.id || 1,
                user_message: input,
                session_id: 1
                // emotion_id removed - backend detects it automatically!
            });

            // AI response with detected emotion data
            const aiMsg: Message = { 
                id: `ai-${Date.now()}`, 
                text: response.data.response, 
                sender: 'ai', 
                timestamp: new Date() 
            };
            
            // Update user message with detected emotion
            if (response.data.emotion_detected) {
                const emotionData = response.data.emotion_detected;
                setMessages(prev => prev.map(msg => 
                    msg.id === userMsg.id 
                        ? { 
                            ...msg, 
                            emotion: emotionData.emotion,
                            emotionConfidence: emotionData.confidence,
                            emotionIntensity: emotionData.intensity
                          }
                        : msg
                ));
                
                console.log(`[Emotion Detected] ${emotionData.emotion} (${(emotionData.confidence * 100).toFixed(1)}% confidence)`);
            }
            
            setMessages(prev => [...prev, aiMsg]);
        } catch (err) {
            console.error("AI Error:", err);
            setMessages(prev => [...prev, { 
                id: `err-${Date.now()}`, 
                text: "I'm having trouble connecting right now. Please try again.", 
                sender: 'ai', 
                timestamp: new Date() 
            }]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <div className="ai-guidance-container">
            <div className="chat-window">
                {messages.map((msg) => (
                    <motion.div 
                        key={msg.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`message-wrapper ${msg.sender}`}
                    >
                        <div className="avatar-icon">
                            {msg.sender === 'ai' ? <Bot size={20} /> : <User size={20} />}
                        </div>
                        <div className="message-bubble">
                            <p>{msg.text}</p>
                            {msg.emotion && (
                                <div className="emotion-badge">
                                    <Sparkles size={12} />
                                    <span>{msg.emotion}</span>
                                    {msg.emotionConfidence && (
                                        <span className="confidence">
                                            {(msg.emotionConfidence * 100).toFixed(0)}%
                                        </span>
                                    )}
                                </div>
                            )}
                            <span className="time">{msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                        </div>
                    </motion.div>
                ))}
                {isTyping && (
                    <div className="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                )}
                <div ref={scrollRef} />
            </div>

            <footer className="chat-input-area">
                <div className="input-wrapper">
                    {/* Microphone Toggle Button */}
                    <button 
                        className={`voice-btn ${isListening ? 'active' : ''}`} 
                        onClick={startListening}
                        title="Voice to Text"
                        type="button"
                    >
                        {isListening ? <MicOff size={20} color="#ef4444" /> : <Mic size={20} />}
                    </button>

                    <input 
                        type="text" 
                        placeholder={isListening ? "Listening..." : "Share what's on your mind..."}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    />
                    <button className="send-btn" onClick={handleSend} disabled={!input.trim() || isTyping}>
                        <Send size={20} />
                    </button>
                </div>
                <p className="disclaimer">Not a crisis line. If you are in immediate danger, please contact emergency services.</p>
            </footer>
        </div>
    );
};

export default AIGuidance;