import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sun, Moon, ShieldCheck, Heart, Award, Users } from 'lucide-react';
import './Auth.css';
import ParticleBackground from '../components/ui/ParticleBackground';
import { signupUser, loginUser } from '../services/authService';

const Auth: React.FC = () => {
    const [isSignUp, setIsSignUp] = useState(false);
    const [theme, setTheme] = useState('dark');
    const [role, setRole] = useState<'client' | 'coach'>('client');
    const [isPending, setIsPending] = useState(false);

    // Form States
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [age, setAge] = useState('25');
    const [gender, setGender] = useState('Male');

    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
    };

    const handleAuthAction = async () => {
        // Validation logic
        if (!email || !password || (isSignUp && !name)) {
            alert("Please fill in all required fields.");
            return;
        }

        try {
            if (isSignUp) {
                console.log("🚀 Starting Signup Process...");
                
                // 1. Create the BASE USER in Django
                const userData = await signupUser(name, email, role);
                console.log("✅ User created successfully:", userData);

                // Note: If you haven't set up apiService yet, 
                // we just store the basic info and move on.
                localStorage.setItem('userRole', role);
                localStorage.setItem('userName', name);
                localStorage.setItem('userEmail', email);

                if (role === 'coach') {
                    setIsPending(true);
                } else {
                    window.location.href = '/dashboard';
                }
            } else {
                // LOGIN FLOW
                console.log("🔑 Starting Login Process...");
                const loggedInUser = await loginUser(email);
                console.log("✅ Logged in:", loggedInUser);
                window.location.href = '/dashboard';
            }
        } catch (error: any) {
            console.error("❌ Auth Error Details:", error);
            
            // Check if Django sent a specific error message (like "Email already exists")
            if (error.response && error.response.data) {
                const backendErrors = JSON.stringify(error.response.data);
                alert(`Backend Error: ${backendErrors}`);
            } else {
                alert("Connection error. Ensure your Django server is running and CORS is enabled.");
            }
        }
    };

    if (isPending) {
        return (
            <div className="auth-wrapper">
                <ParticleBackground theme={theme} />
                <motion.div 
                    className="auth-container pending-view" 
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                >
                    <ShieldCheck size={80} color="#6FCF97" />
                    <h1>Verification in Progress</h1>
                    <p>Our clinical team is verifying your professional credentials for the <strong>{name}</strong> coach profile.</p>
                    <button className="main-btn" onClick={() => setIsPending(false)}>BACK TO LOGIN</button>
                </motion.div>
            </div>
        );
    }

    return (
        <div className="auth-wrapper">
            <ParticleBackground theme={theme} />
            <div className="theme-toggle" onClick={toggleTheme}>
                {theme === 'light' ? <Moon size={24} /> : <Sun size={24} color="#FDB813" />}
            </div>

            <div className="auth-container">
                {/* LOGIN PANEL (Left) */}
                <div className="panel">
                    <div className="auth-form">
                        <h1>Welcome back</h1>
                        <p>Sign in to your MindWell sanctuary.</p>
                        <input className="input-field" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                        <input className="input-field" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        <button className="main-btn" onClick={handleAuthAction}>SIGN IN</button>
                    </div>
                </div>

                {/* SIGNUP PANEL (Right) */}
                <div className="panel">
                    <div className="auth-form">
                        <h1>Create safe space</h1>
                        <div className="role-selector">
                            <button className={role === 'client' ? 'active' : ''} onClick={() => setRole('client')}><Users size={16} /> Client</button>
                            <button className={role === 'coach' ? 'active' : ''} onClick={() => setRole('coach')}><Award size={16} /> Coach</button>
                        </div>

                        <input className="input-field" type="text" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} />
                        <input className="input-field" type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                        
                        <AnimatePresence>
                            {role === 'client' && (
                                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="extra-fields">
                                    <div className="field-row">
                                        <input className="input-field half" type="number" placeholder="Age" value={age} onChange={(e) => setAge(e.target.value)} />
                                        <select className="input-field half" value={gender} onChange={(e) => setGender(e.target.value)}>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                            <option value="Non-binary">Non-binary</option>
                                        </select>
                                    </div>
                                </motion.div>
                            )}
                        </AnimatePresence>

                        <input className="input-field" type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        <button className="main-btn" onClick={handleAuthAction}>
                            {role === 'coach' ? 'REQUEST VERIFICATION' : 'CREATE ACCOUNT'}
                        </button>
                    </div>
                </div>

                {/* OVERLAY SECTION */}
                <motion.div 
                    className="overlay-container" 
                    animate={{ x: isSignUp ? '-100%' : '0%' }} 
                    transition={{ type: "spring", stiffness: 80, damping: 17 }}
                >
                    <div className="overlay">
                        <AnimatePresence mode="wait">
                            {isSignUp ? (
                                <motion.div key="to-signin" className="overlay-content" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                                    <Heart size={50} />
                                    <h2>Already a member?</h2>
                                    <p>Login to continue your journey.</p>
                                    <button className="ghost-btn" onClick={() => setIsSignUp(false)}>SIGN IN</button>
                                </motion.div>
                            ) : (
                                <motion.div key="to-signup" className="overlay-content" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                                    <ShieldCheck size={50} />
                                    <h2>New here?</h2>
                                    <p>Begin your secure, AI-guided therapy experience today.</p>
                                    <button className="ghost-btn" onClick={() => setIsSignUp(true)}>SIGN UP</button>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default Auth;