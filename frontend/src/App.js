import React, { useEffect, useState } from 'react';
import './App.css';
import StudyPage from './pages/StudyPage';
import FinishedStudyPage from './pages/FinishedStudyPage';

function App() {
    const [finishedStudy, setFinishedStudy] = useState(false);

    // This useEffect hook handled getting the participant ID from the URL and storing it in the browser's local storage
    // The participant ID is appended to the URL by Prolific when the study is launched
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const participantId = params.get('participant_id');
        if (participantId) {
            localStorage.setItem('participant_id', participantId);
        } else {
            // For production, uncomment the line below
            // console.error('Participant ID not found in URL');
        }
    }, []);

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
        console.log('User ID:', localStorage.getItem('user_id'), 'Study finished:', finishedStudy);
    }, [finishedStudy]);

    return (
        <div className="App">
            {finishedStudy ? <FinishedStudyPage /> : <StudyPage setFinishedStudy={setFinishedStudy} />}
        </div>
    );
}

export default App;
