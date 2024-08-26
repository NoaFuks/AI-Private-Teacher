// // src/pages/ParentProgressPage.js
// import React, { useState, useEffect } from 'react';
// import axios from 'axios';
// import Icon from '../components/Icon';
// import ReturnButton from '../components/ReturnButton';
// import './ParentProgressPage.css';

// const ParentProgressPage = () => {
//     const [progressData, setProgressData] = useState({});

//     useEffect(() => {
//         // Fetch progress data from the backend
//         axios.get('http://localhost:8000/api/get-progress?student_name=child')
//             .then(response => {
//                 setProgressData(response.data);
//             })
//             .catch(error => {
//                 console.error('Error fetching progress:', error);
//             });
//     }, []);

//     return (
//         <div className="progress-page">
//             <div className="progress-card">
//                 <Icon size={80} />
//                 <h1 className="text-center mb-4">Parent Progress Page</h1>
//                 {Object.keys(progressData).length > 0 ? (
//                     <div className="progress-content">
//                         <h2>Student Progress</h2>
//                         <pre>{JSON.stringify(progressData, null, 2)}</pre>
//                     </div>
//                 ) : (
//                     <p>No progress data available.</p>
//                 )}
//                 <ReturnButton />
//             </div>
//         </div>
//     );
// };

// export default ParentProgressPage;


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
                        <p><strong>Total Lessons:</strong> {progressData['Total Lessons']}</p>
                        <p><strong>Total Questions:</strong> {progressData['Total Questions']}</p>
                        <p><strong>Correct Answers:</strong> {progressData['Correct Answers']}</p>
                        <p><strong>Incorrect Answers:</strong> {progressData['Incorrect Answers']}</p>
                        <p><strong>Topics Covered:</strong> {Array.isArray(progressData['Topics Covered']) ? progressData['Topics Covered'].join(', ') : 'No topics covered'}</p>
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

