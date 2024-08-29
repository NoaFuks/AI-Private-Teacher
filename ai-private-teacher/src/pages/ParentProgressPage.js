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
    
    const getProgressBarWidth = (percentage) => {
        const parsedPercentage = parseFloat(percentage);
        return parsedPercentage > 0 ? `${parsedPercentage}%` : '5px';
    };

    const getBarClass = (percentage) => {
        const parsedPercentage = parseFloat(percentage);
        return parsedPercentage >= 50 ? 'correct-bar' : 'incorrect-bar';
    };

    const renderFeelingIcon = (feeling) => {
        switch(feeling) {
            case 'happy':
                return <span role="img" aria-label="Happy">😊</span>;
            case 'neutral':
                return <span role="img" aria-label="Neutral">😐</span>;
            case 'confused':
                return <span role="img" aria-label="Confused">😕</span>;
            case 'sad':
                return <span role="img" aria-label="Sad">😞</span>;
            default:
                return null;
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
                        <p><strong>Total Questions:</strong> {progressData['Total Questions']}</p>
                       <div className="progress-bar-container">
                            <div className={`progress-bar`}>
                                <div
                                    className={`progress-bar-filled ${getBarClass(progressData['Correct Percentage'])}`}
                                    style={{ width: getProgressBarWidth(progressData['Correct Percentage']) }}
                                />
                                <span className="progress-text">
                                    {parseFloat(progressData['Correct Percentage']).toFixed(2)}%
                                </span>
                            </div>
                            <div className={`progress-bar`}>
                                <div
                                    className={`progress-bar-filled ${getBarClass(progressData['Incorrect Percentage'])}`}
                                    style={{ width: getProgressBarWidth(progressData['Incorrect Percentage']) }}
                                />
                                <span className="progress-text">
                                    {parseFloat(progressData['Incorrect Percentage']).toFixed(2)}%
                                </span>
                            </div>
                        </div>
                        <p className="topics-title"><strong>Topics Covered:</strong></p>
                        <ol>
                            {Array.isArray(progressData['Topics Covered']) ? progressData['Topics Covered']
                                .filter(topic => topic)  // Filter out empty or falsy values
                                .map((topic, index) => (
                                    <li key={index}>{topic}</li>
                                )) : 'No topics covered'}
                        </ol>
                        <p><strong>AI Opinion:</strong> {progressData['AI Opinion']}</p>
                        {/* New section for displaying feelings */}
                        <p className="topics-title"><strong>Student Feelings Timeline:</strong></p>
                        <div className="feelings-timeline">
                            {Array.isArray(progressData['Feelings']) ? progressData['Feelings']
                                .slice()  // Create a shallow copy of the array
                                .reverse()  // Reverse the order for reverse chronological display
                                .map((feeling, index) => (
                                    <React.Fragment key={index}>
                                        <div className="timeline-item">
                                            {renderFeelingIcon(feeling)}
                                        </div>
                                        {index < progressData['Feelings'].length - 1 && <div className="timeline-connector"></div>}
                                    </React.Fragment>
                                )) : 'No feelings recorded'}
                        </div>
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

