import React, { useState } from 'react';
import axios from 'axios';
import Icon from '../components/Icon';
import ReturnButton from '../components/ReturnButton';
import './ProfilePage.css';

const ProfilePage = () => {
    const [name, setName] = useState('');
    const [age, setAge] = useState('');
    const [hobbies, setHobbies] = useState('');
    const [learningPreferences, setLearningPreferences] = useState('');
    const [pdfFile, setPdfFile] = useState(null);

    const handlePdfUpload = (e) => {
        setPdfFile(e.target.files[0]);
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
    
        const studentProfile = {
            name,
            age: parseInt(age),
            hobbies: hobbies.split(',').map(hobby => hobby.trim()),
            learning_preferences: learningPreferences.split(',').map(pref => pref.trim())
        };
    
        try {
            // Send the profile to the backend
            await axios.post('http://localhost:8000/api/save-profile', studentProfile);
    
            if (pdfFile) {
                // Upload the PDF file along with the student's name
                const formData = new FormData();
                formData.append('file', pdfFile);
                formData.append('student_name', name);  // Add student name to the form data
    
                const response = await axios.post('http://localhost:8000/api/upload-pdf', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
    
                alert("Profile and PDF saved successfully");
                console.log('Profile and PDF saved:', response.data);
            } else {
                alert("Profile saved successfully");
                console.log('Profile saved without PDF');
            }
        } catch (error) {
            console.error('There was an error saving the profile and/or PDF!', error);
        }
    };
    
    return (
        <div className="profile-page">
            <div className="profile-card">
                <Icon size={130} />
                <h1 className="text-center mb-4">Student Profile</h1>
                <form onSubmit={handleSubmit}>
                    <div className="form-group mb-3">
                        <label htmlFor="name">Name:</label>
                        <input
                            type="text"
                            id="name"
                            className="form-control"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Enter your name"
                        />
                    </div>
                    <div className="form-group mb-3">
                        <label htmlFor="age">Age:</label>
                        <input
                            type="number"
                            id="age"
                            className="form-control"
                            value={age}
                            onChange={(e) => setAge(e.target.value)}
                            placeholder="Enter your age"
                        />
                    </div>
                    <div className="form-group mb-3">
                        <label htmlFor="hobbies">Hobbies (comma-separated):</label>
                        <input
                            type="text"
                            id="hobbies"
                            className="form-control"
                            value={hobbies}
                            onChange={(e) => setHobbies(e.target.value)}
                            placeholder="e.g. reading, coding, swimming"
                        />
                    </div>
                    <div className="form-group mb-4">
                        <label htmlFor="learningPreferences">Learning Preferences (comma-separated):</label>
                        <input
                            type="text"
                            id="learningPreferences"
                            className="form-control"
                            value={learningPreferences}
                            onChange={(e) => setLearningPreferences(e.target.value)}
                            placeholder="e.g. math, english, history"
                        />
                    </div>
                    <div className="form-group mb-4">
                        <label htmlFor="pdfFile">Upload PDF for Lesson:</label>
                        <input
                            type="file"
                            id="pdfFile"
                            className="form-control"
                            onChange={handlePdfUpload}
                            accept="application/pdf"
                        />
                    </div>
                    <div className="d-grid gap-2">
                        <button type="submit" className="btn btn-primary btn-lg">
                            Save Profile
                        </button>
                    </div>
                </form>
                <ReturnButton />
            </div>
        </div>
    );
};

export default ProfilePage;
