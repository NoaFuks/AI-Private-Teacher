// src/components/ReturnButton.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const ReturnButton = () => {
    const navigate = useNavigate();

    return (
        <button
            onClick={() => navigate('/')}
            style={{
                padding: '10px 20px',
                marginTop: '20px',
                backgroundColor: '#2193b0',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                fontSize: '1rem',
            }}
        >
            Return to Landing Page
        </button>
    );
};

export default ReturnButton;
