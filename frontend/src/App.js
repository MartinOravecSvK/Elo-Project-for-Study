import React, { useEffect, useState } from 'react';
import './App.css';

import InstructionPage1 from './pages/Instructions/InstructionPage1';
import InstructionPage2 from './pages/Instructions/InstructionPage2';
import TestPage1 from './pages/Instructions/TestPage1';
import TestPage2 from './pages/Instructions/TestPage2';

import StudyPage from './pages/StudyPage';
import FinishedStudyPage from './pages/FinishedStudyPage';

import HeaderComponent from './components/HeaderComponent';

function App() {
    const [error, setError] = useState(null);
    const [currentPageIndex, setcurrentPageIndex] = useState(0);
    const [finishedStudy, setFinishedStudy] = useState(false);
    const [eventsNum, setEventsNum] = useState(0);
    const [eventsDone, setEventsDone] = useState(0);

    const [startWorse, setStartWorse] = useState(false);
    const [blockSize, setBlockSize] = useState(0);
    
    // Sets the first block of questions to be for users to select worse scebario
    useEffect(() => {
        setStartWorse(Math.random() >= 0.5);
    }, []);

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
            generateUserId();
        } else {
            console.log('User ID:', localStorage.getItem('user_id'));
        }
    }, []);

    useEffect(() => {
        console.log('User ID:', localStorage.getItem('user_id'), 'Study finished:', finishedStudy);
    }, [finishedStudy]);

    const generateUserId = async () => {
        // Generate a random 8-character user ID
        const user_id = Math.random().toString(36).substr(2, 8);
        try {
            const response = await fetch('http://localhost:5000/check_user_id', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: user_id,
                }),
            });
            const data = await response.json();
            if (data.message === 'User ID already exists') {
                generateUserId();
            } else {
                localStorage.setItem('user_id', user_id);
                console.log('Data: ', data);
                setBlockSize(Math.trunc(data.questions_num/2));
                setEventsNum(data.questions_num);
            }
        } catch (error) {
            console.error();
        }
    }

    const nextPage = () => {
        setcurrentPageIndex((prevIndex) => prevIndex + 1);
    }

    return (
        error != null ? (
            <div>
                Error: {error.toString()}
            </div>
        ) : (
        <div className="App">
            {currentPageIndex === 0 && <InstructionPage1 nextPage={nextPage} />}
            {currentPageIndex === 1 && <InstructionPage2 nextPage={nextPage} />}
            {currentPageIndex === 2 && <TestPage1 nextPage={nextPage} userId={localStorage.getItem('user_id')} setError={setError} />}
            {currentPageIndex === 3 && <TestPage2 nextPage={nextPage} userId={localStorage.getItem('user_id')} setError={setError} />}
            {currentPageIndex > 3 && (
                finishedStudy ? 
                    <FinishedStudyPage /> : 
                    <>
                        <HeaderComponent eventsNum={eventsNum} eventsDone={eventsDone} />
                        <StudyPage 
                            setFinishedStudy={setFinishedStudy} 
                            setEventsNum={setEventsNum} 
                            setEventsDone={setEventsDone}  
                            blockSize={blockSize} 
                            setBlockSize={setBlockSize}
                            worseStart={startWorse}
                            setError={setError}
                        />
                    </>
            )}
        </div>
        )
    );
}

export default App;
