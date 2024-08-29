// src/pages/LandingPage.js
import React from 'react';
import { Link } from 'react-router-dom';
import Icon from '../components/Icon'; // Import the Icon component
import './LandingPage.css';

const LandingPage = () => {
    return (
        <div className="landing-container">
            <div className="content-wrapper">
                <Icon size={300} /> {/* Add the icon at the top */}
                <h1>Welcome to the AI Private Teacher App</h1>
                <p>Your personal assistant for learning and progress tracking.</p>

                <div className="button-group">
                    <Link to="/profile">
                        <button className="styled-button">Profile Page</button>
                    </Link>

                    <Link to="/generate-lesson">
                        <button className="styled-button">Lesson Generation</button>
                    </Link>

                    <Link to="/progress">
                        <button className="styled-button">Progress Page</button>
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
