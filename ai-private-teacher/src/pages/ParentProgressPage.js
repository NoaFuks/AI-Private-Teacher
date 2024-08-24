// src/pages/ParentProgressPage.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Icon from '../components/Icon';
import ReturnButton from '../components/ReturnButton';
import './ParentProgressPage.css';

const ParentProgressPage = () => {
    const [progressData, setProgressData] = useState({});

    useEffect(() => {
        // Fetch progress data from the backend
        axios.get('http://localhost:8000/api/get-progress?student_name=child')
            .then(response => {
                setProgressData(response.data);
            })
            .catch(error => {
                console.error('Error fetching progress:', error);
            });
    }, []);

    return (
        <div className="progress-page">
            <div className="progress-card">
                <Icon size={80} />
                <h1 className="text-center mb-4">Parent Progress Page</h1>
                {Object.keys(progressData).length > 0 ? (
                    <div className="progress-content">
                        <h2>Student Progress</h2>
                        <pre>{JSON.stringify(progressData, null, 2)}</pre>
                    </div>
                ) : (
                    <p>No progress data available.</p>
                )}
                <ReturnButton />
            </div>
        </div>
    );
};

export default ParentProgressPage;
