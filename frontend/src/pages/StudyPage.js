import React, { useEffect, useState } from 'react';
import './StudyPage.css';
import config from '../config';

import ExperienceComponent from '../components/ExperienceComponent';
import CategoryComponent from '../components/CategoryComponent';
import ClassificationComponent from '../components/ClassificationComponent';
import AttentionPage from './AttentionPage';

function StudyPage({ 
    setFinishedStudy, 
    setEventsNum, 
    setEventsDone, 
    worseStart, 
    blockSize, 
    setBlockSize, 
    setError, 
    counter, 
    setCounter, 
    userId,
    setVisibleHeader,
}) {
    const otherFields = false;
    
    const [events, setEvents] = useState(JSON.parse(localStorage.getItem('events')) || null);
    const [loser_id, setLoser_id] = useState(null);
    const [winner_id, setWinner_id] = useState(null);
    const [polarization, setPolarization] = useState(null);
    const [category, setCategory] = useState(null);
    const [classification, setClassification] = useState(null);

    const [attention1, setAttention1] = useState(localStorage.getItem('attention1') === 'true');
    const [attention2, setAttention2] = useState(localStorage.getItem('attention2') === 'true');
    
    const attention1Word = worseStart ? "worse" : "better";
    const attention2Word = worseStart ? "better" : "worse";
    
    useEffect(() => {
        if (!userId) {
            console.error('User ID not found');
        }
        if (!events) {
            fetchEvents();
        }
    }, []);

    const fetchEvents = async () => {
        try {
            const response = await fetch(`${config.apiBaseUrl}/next?user_id=${userId}`);
            const data = await response.json();
            if (data.events) {
                setEvents(data.events);
                localStorage.setItem('events', JSON.stringify(data.events));
                setEventsDone(data.progress.current_completed);
                setEventsNum(data.progress.number_of_questions);
                setBlockSize(Math.trunc(data.progress.number_of_questions/2));
            } else {
                setEvents({});
                if (data.message === 'Study completed') {
                    setFinishedStudy(true);
                    setEventsDone(data.progress.current_completed);
                    setEventsNum(data.progress.number_of_questions);
                }
                if (data.message === "You are no longer a participant") {
                    setError(data.message);
                }
            }
        } catch (error) {
            console.error('Error fetching events:', error);
            setError(error);
        }
    };

    const switchLoserWinnerIds = () => {
        setLoser_id((prevLoserId) => {
            setWinner_id(prevLoserId);
            return winner_id;
        });
    };

    useEffect(() => {
        if ((counter < blockSize && worseStart) || (counter >= blockSize && !worseStart)) {
            switchLoserWinnerIds();
        }
    }, [counter]);

    const submitAnswer = async () => {
        // First check that all the required states are set
        // If not show to the user that they need to select one from each option

        if (!userId) {
            console.error('User ID not found in local storage');
            return;
        }

        if (!loser_id) {
            // Change this to show a message to the user
            console.error('More negative event ID not found');
            return;
        }
        if (!winner_id) {
            // Change this to show a message to the user
            console.error('More positive event ID not found');
            return;
        }

        if (otherFields) {
            if (!category) {
                // Change this to show a message to the user
                console.error('Category not found');
                return;
            }
            if (!classification) {
                // Change this to show a message to the user
                console.error('Classification not found');
                return;
            }
        }

        const shouldSwitch = (counter < blockSize && worseStart) || (counter >= blockSize && !worseStart);
        const finalLoserId = shouldSwitch ? winner_id : loser_id;
        const finalWinnerId = shouldSwitch ? loser_id : winner_id;

        localStorage.setItem('counter', counter + 1);
        setCounter(counter + 1);
        
        try {
            const response = await fetch(`${config.apiBaseUrl}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    loser_id: finalLoserId,
                    winner_id: finalWinnerId,
                    category: category,
                    classification: classification,
                    polarization: polarization,
                }),
            });
            const data = await response.json();
            if (data.events) {
                setEvents(data.events);
                setEventsDone(data.progress.current_completed);
                setEventsNum(data.progress.number_of_questions);
                localStorage.setItem('events', JSON.stringify(data.events));
            } else {    
                setEvents({});
                if (data.message === 'Study completed') {
                    setFinishedStudy(true);
                    localStorage.setItem('finishedStudy', 'true');
                    setEventsDone(data.progress.current_completed);
                    setEventsNum(data.progress.number_of_questions);
                }
            }
            resetStates();
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    };

    const resetStates = () => {
        setLoser_id(null);
        setWinner_id(null);
        setCategory(null);
        setClassification(null);
    };

    if (!attention1) {
        setVisibleHeader(false);
        return <AttentionPage 
            word={attention1Word} 
            buttonText={"Start"} 
            start={true}
            onContinue={() => {
                setAttention1(!attention1);
                localStorage.setItem('attention1', 'true');
            }}
        />
    }

    if (!attention2 && counter === blockSize) {
        setVisibleHeader(false);
        if (!attention2) {
            return <AttentionPage 
                word={attention2Word} 
                buttonText={"Continue"} 
                start={false}
                onContinue={() => {
                    setAttention2(!attention2);
                    localStorage.setItem('attention2', 'true');
                }}
            />
        }
    }

    setVisibleHeader(true);

    return (
        <div className='StudyPage'>
            {events && Object.keys(events).length > 0 ? (
                <ExperienceComponent 
                    setLoser_id={setLoser_id} 
                    setWinner_id={setWinner_id} 
                    events={events}  
                    counter={counter} 
                    blockSize={blockSize} 
                    worseStart={worseStart}
                    setPolarization={setPolarization}
                />
            ) : (
                // <p>No more events to show. Study completed!</p>
                <p>Please wait for the server to respond, if this takes too long please refresh your browser</p>
            )}
            {otherFields && winner_id != null && loser_id != null && (
                <CategoryComponent setCategory={setCategory} />
            )}
            {otherFields && category != null && (
                <ClassificationComponent setClassification={setClassification} />
            )}
            {(classification != null || (!otherFields && winner_id != null && loser_id != null)) && (
                <button onClick={submitAnswer} className='NextButton'>Next</button>
            )}
        </div>
    );
}

export default StudyPage;