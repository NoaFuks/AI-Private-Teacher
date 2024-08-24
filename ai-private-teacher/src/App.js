// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ProfilePage from './pages/ProfilePage';
import LessonGenerationPage from './pages/LessonGenerationPage';
import ParentProgressPage from './pages/ParentProgressPage';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/generate-lesson" element={<LessonGenerationPage />} />
                <Route path="/progress" element={<ParentProgressPage />} />
            </Routes>
        </Router>
    );
};

export default App;
