import React, { useEffect, useState } from 'react';
import './App.css';
import StudyPage from './pages/StudyPage';

function App() {
    const [finshedStudy, setFinishedStudy] = useState(false);

    // This useEffect hook is used to generate a random 8-character user ID and store it in the browser's local storage
    // This will be changed later to make sure there are no clashing user IDs
    // For that a new backend API will be created to generate a unique user ID
    useEffect(() => {
        // Check if user ID is already set in local storage
        if (!localStorage.getItem('user_id')) {
            // Generate a random 8-character user ID
            const userId = 'user-' + Math.random().toString(36).substr(2, 8);
            localStorage.setItem('user_id', userId);
        }
    }, []);

    useEffect(() => {
        if (finshedStudy) {
            console.log('Study completed');
        }
    }, [finshedStudy]);

    return (
        <div className="App">
            <StudyPage setFinishedStudy={setFinishedStudy} />
        </div>
    );
}

export default App;
