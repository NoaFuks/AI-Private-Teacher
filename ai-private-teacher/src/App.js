// src/App.js
import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import ProfilePage from './pages/ProfilePage';
import LessonGenerationPage from './pages/LessonGenerationPage';
import ParentProgressPage from './pages/ParentProgressPage';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
    useEffect(() => {
        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.async = true;
        script.innerHTML = `
            window.smartlook||(function(d) {
                var o=smartlook=function(){ o.api.push(arguments)},h=d.getElementsByTagName('head')[0];
                var c=d.createElement('script');o.api=new Array();c.async=true;c.type='text/javascript';
                c.charset='utf-8';c.src='https://web-sdk.smartlook.com/recorder.js';h.appendChild(c);
            })(document);
            smartlook('init', '84cd0e258accf0e4ede457d5ad1fdecde94e1b7b', { region: 'eu' });
            console.log('Smartlook initialized');
        `;
        document.head.appendChild(script);
    }, []);
    

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
