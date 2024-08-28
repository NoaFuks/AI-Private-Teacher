import React, { useState } from 'react';
import axios from 'axios';
import Icon from '../components/Icon';
import ReturnButton from '../components/ReturnButton';
import './ParentProgressPage.css';

const ParentProgressPage = () => {
    const [childName, setChildName] = useState('');
    const [progressData, setProgressData] = useState(null);
    const [error, setError] = useState('');

    const handleInputChange = (event) => {
        setChildName(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (childName) {
            // Fetch progress data from the backend
            axios.get(`http://localhost:8000/api/get-progress?student_name=${childName}`)
                .then(response => {
                    console.log("Received Progress Data: ", response.data);
                    setProgressData(response.data);
                    setError('');
                })
                .catch(error => {
                    console.error('Error fetching progress:', error);
                    setError('Could not fetch progress data for the specified child.');
                });
        } else {
            setError('Please enter a valid child name.');
        }
    };

    return (
        <div className="progress-page">
            <div className="progress-card">
                <Icon size={80} />
                <h1 className="text-center mb-4">Parent Progress Page</h1>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="childName">Enter Child's Name:</label>
                    <input
                        type="text"
                        id="childName"
                        value={childName}
                        onChange={handleInputChange}
                        placeholder="Child's Name"
                        required
                    />
                    <button type="submit">Submit</button>
                </form>
                {error && <p className="error-message">{error}</p>}
                {progressData ? (
                    <div className="progress-content">
                        <h2>Student Progress</h2>
                        <p><strong>Correct Percentage:</strong> {progressData['Correct Percentage']}</p>
                        <p><strong>Incorrect Percentage:</strong> {progressData['Incorrect Percentage']}</p>
                        <p><strong>Total Questions:</strong> {progressData['Total Questions']}</p>
                        <p className="topics-title"><strong>Topics Covered:</strong></p>
                        <ol>
                            {Array.isArray(progressData['Topics Covered']) ? progressData['Topics Covered']
                                .filter(topic => topic)  // Filter out empty or falsy values
                                .map((topic, index) => (
                                    <li key={index}>{topic}</li>
                                )) : 'No topics covered'}
                        </ol>
                        <p><strong>AI Opinion:</strong> {progressData['AI Opinion']}</p>
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

