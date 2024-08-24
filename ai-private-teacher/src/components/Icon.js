// src/components/Icon.js
import React from 'react';

const Icon = ({ size = 50 }) => {
    return (
        <img
            src={require('../assets/icon.png')} // Adjust the path as needed
            alt="AI Private Teacher Icon"
            style={{ width: size, height: size }}
        />
    );
};

export default Icon;
