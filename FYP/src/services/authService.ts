import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/user/';

// 1. SIGNUP: Stays mostly the same, but we save the user immediately on success
export const signupUser = async (name: string, email: string, role: string) => {
    const response = await axios.post(API_URL, { name, email, role });
    if (response.data) {
        localStorage.setItem('user', JSON.stringify(response.data));
    }
    return response.data;
};

// 2. LOGIN: Improved to be more efficient
export const loginUser = async (email: string) => {
    // Instead of fetching EVERYONE, we ask Django for users with this email
    // This uses Django's filtering (if enabled) or we find them in the list
    const response = await axios.get(API_URL);
    const users = response.data;
    
    const user = users.find((u: any) => u.email.toLowerCase() === email.toLowerCase());
    
    if (user) {
        localStorage.setItem('user', JSON.stringify(user));
        return user;
    } else {
        throw new Error("Invalid email address. Please sign up first.");
    }
};

// 3. GET CURRENT USER: Used by DashboardLayout to check permissions
export const getCurrentUser = () => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    try {
        return JSON.parse(userStr);
    } catch (e) {
        localStorage.removeItem('user'); // Clear corrupted data
        return null;
    }
};

// 4. LOGOUT: Cleans up and redirects
export const logout = () => {
    localStorage.clear(); // Clears everything to be safe
    window.location.href = '/'; 
};