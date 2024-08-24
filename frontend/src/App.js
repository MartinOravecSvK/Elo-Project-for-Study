import React, { useCallback, useEffect, useState } from 'react';
import './App.css';
import config from './config';

import InstructionPage1 from './pages/Instructions/InstructionPage1';
import InstructionPage2 from './pages/Instructions/InstructionPage2';
import TestPage1 from './pages/Instructions/TestPage1';
import TestPage2 from './pages/Instructions/TestPage2';
import ParticipantInformationPage from './pages/ParticipationInformationPage';

import StudyPage from './pages/StudyPage';
import FinishedStudyPage from './pages/FinishedStudyPage';
import FailedPage from './pages/FailedPage';

import HeaderComponent from './components/HeaderComponent';

function App() {
    const [error, setError] = useState(null);
    const [userId, setUserId] = useState(localStorage.getItem('user_id') || '');
    const [currentPageIndex, setcurrentPageIndex] = useState(0);
    const [finishedStudy, setFinishedStudy] = useState(false);
    const [eventsNum, setEventsNum] = useState(parseInt(localStorage.getItem('eventsNum')) || 0);
    const [eventsDone, setEventsDone] = useState(localStorage.getItem('counter') || 0);
    const [counter, setCounter] = useState(parseInt(localStorage.getItem('counter')) || 0);
    
    const [startWorse, setStartWorse] = useState(null);
    const [blockSize, setBlockSize] = useState(parseInt(localStorage.getItem('bloackSize')) || 0);

    const [failedAttention, setFailedAttention] = useState(false);
    const [blocked, setBlocked] = useState(localStorage.getItem('blocked') === 'true');
    
    const [visibleHeader, setVisibleHeader] = useState(false);

    const generateUserId = useCallback(async () => {
        // Generate a random 8-character user ID
        const user_id = Math.random().toString(36).substr(2, 8);
        try {
            const response = await fetch(`${config.apiBaseUrl}/check_user_id`, {
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
                setUserId(user_id);
                setBlockSize(Math.trunc(data.questions_num/2));
                localStorage.setItem('bloackSize', Math.trunc(data.questions_num/2));
                setEventsNum(data.questions_num);
                localStorage.setItem('eventsNum', data.questions_num);
            }
        } catch (error) {
            console.error();
        }
    }, []);

    const blockUser = async (userId) => {
        try {
            const response = await fetch(`${config.apiBaseUrl}/block_user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                }),
            });
            const data = await response.json();
            setError(data.message);
        }
        catch (error) {
            console.error('Error blocking user:', error);
        }
        localStorage.setItem('blocked', true);
    }

    // This useEffect hook handled getting the participant ID from the URL and storing it in the browser's local storage
    // The participant ID is appended to the URL by Prolific when the study is launched
    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const participantId = params.get('PROLIFIC_PID');
        const studyId = params.get('STUDY_ID');
        const sessionID = params.get('SESSION_ID');
        
        if (participantId) {
            localStorage.setItem('PROLIFIC_PID', participantId);
            localStorage.setItem('STUDY_ID', studyId);
            localStorage.setItem('SESSION_ID', sessionID);
        } else {
            // For production, uncomment the line below
            // console.error('Participant ID not found in URL');
        }
    }, []);

    // Check the local storage for the current page index and the counter
    useEffect(() => {
        if (localStorage.getItem('currentPageIndex') !== null) {
            setcurrentPageIndex(parseInt(localStorage.getItem('currentPageIndex')));
        }
        if (localStorage.getItem('counter') !== null) {
            setCounter(parseInt(localStorage.getItem('counter')));
        }
        if (localStorage.getItem('finishedStudy') !== null) {
            setFinishedStudy(localStorage.getItem('finishedStudy') === 'true');
        }
        if (localStorage.getItem('startWorse') !== null) {
            setStartWorse(localStorage.getItem('startWorse') === 'true');
        } else if (localStorage.getItem('startWorse') === null) {
            const isStartWorse = Math.random() >= 0.5;
            setStartWorse(isStartWorse);
            localStorage.setItem('startWorse', isStartWorse);
        }
    }, []);
    
    // This useEffect hook is used to generate a random 8-character user ID and store it in the browser's local storage
    // This will be changed later to make sure there are no clashing user IDs
    // For that a new backend API will be created to generate a unique user ID
    useEffect(() => {
        // Check if user ID is already set in local storage
        if (!localStorage.getItem('user_id')) {
            generateUserId();
        } 
    }, [generateUserId]);

    useEffect(() => {
        if (currentPageIndex > 3) {
            if (failedAttention) {
                blockUser(localStorage.getItem('user_id'));
                setBlocked(true);
            }
        }
    }, [currentPageIndex, failedAttention]);

    const nextPage = () => {
        setcurrentPageIndex((prevIndex) => {
            const newIndex = prevIndex + 1;
            localStorage.setItem('currentPageIndex', newIndex.toString());
            return newIndex;
        });
    }


    if (blocked) {
        return (
            <FailedPage />
        )
    }

    // Fix the wording

    return (
        error != null ? (
            <div>
                Error: {error.toString()}
            </div>
        ) : (
        <div className="App">
            {currentPageIndex === 0 && <ParticipantInformationPage nextPage={nextPage} />}
            {currentPageIndex === 1 && <InstructionPage1 nextPage={nextPage} />}
            {currentPageIndex === 2 && <TestPage1 nextPage={nextPage} userId={localStorage.getItem('user_id')} setError={setError} setFailedAttention={setFailedAttention} />}
            {currentPageIndex === 3 && <TestPage2 nextPage={nextPage} userId={localStorage.getItem('user_id')} setError={setError} setFailedAttention={setFailedAttention} />}
            {currentPageIndex === 4 && <InstructionPage2 nextPage={nextPage} />}
            {currentPageIndex > 4 && (
                finishedStudy ? 
                    <FinishedStudyPage /> :
                        <>
                            <HeaderComponent eventsNum={eventsNum} eventsDone={eventsDone} visible={visibleHeader} />
                            <StudyPage 
                                setFinishedStudy={setFinishedStudy} 
                                setEventsNum={setEventsNum} 
                                setEventsDone={setEventsDone}  
                                blockSize={blockSize} 
                                setBlockSize={setBlockSize}
                                worseStart={startWorse}
                                setError={setError}
                                counter={counter}
                                setCounter={setCounter}
                                userId={userId}
                                setVisibleHeader={setVisibleHeader}
                            />
                        </>
            )}
        </div>
        )
    );
}

export default App;
