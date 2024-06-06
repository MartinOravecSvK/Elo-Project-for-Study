import React, { useEffect, useState } from 'react';
import './StudyPage.css';

import ExperienceComponent from '../components/ExperienceComponent';
import CategoryComponent from '../components/CategoryComponent';
import ClassificationComponent from '../components/ClassificationComponent';

// TODO:
// - Make it easy to toggle Categories
// - Refactor the code to make it more readable

function StudyPage({ setFinishedStudy, setEventsNum, setEventsDone, worseStart, blockSize, setBlockSize, setError }) {
    const otherFields = true;
    const [events, setEvents] = useState({});
    const [counter, setCounter] = useState(0);
    const [loser_id, setLoser_id] = useState(null);
    const [winner_id, setWinner_id] = useState(null);
    const [polarization, setPolarization] = useState(null);
    const [category, setCategory] = useState(null);
    const [classification, setClassification] = useState(null);
    
    // Replace 'some-unique-user-id' with a unique identifier for the user (generate some and store it in browser's local storage)
    const userId = localStorage.getItem('user_id') || null;
    
    useEffect(() => {
        if (!userId) {
            console.error('User ID not found in local storage');
        }
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const response = await fetch(`http://localhost:5000/next?user_id=${userId}`);
            const data = await response.json();
            if (data.events) {
                setEvents(data.events);
                setEventsDone(data.progress.current_completed);
                setEventsNum(data.progress.number_of_questions);
                setBlockSize(Math.trunc(data.progress.number_of_questions/2));
            } else {
                console.log(data.error || data.message || 'No events found')
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

        console.log(counter, blockSize, worseStart)
        const shouldSwitch = (counter < blockSize && worseStart) || (counter >= blockSize && !worseStart);
        const finalLoserId = shouldSwitch ? winner_id : loser_id;
        const finalWinnerId = shouldSwitch ? loser_id : winner_id;

        setCounter(counter + 1);
        console.log('Counter: ', counter)
        
        try {

            const response = await fetch('http://localhost:5000/submit', {
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
                console.log('New events fetched:', data.events)
                setEventsDone(data.progress.current_completed);
                setEventsNum(data.progress.number_of_questions);
            } else {    
                console.log(data.error || data.message || 'No events found')
                setEvents({});
                if (data.message === 'Study completed') {
                    setFinishedStudy(true);
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
                <p>No more events to show. Study completed!</p>
            )}
            {winner_id != null && loser_id != null && (
                <CategoryComponent setCategory={setCategory} />
            )}
            {category != null && (
                <ClassificationComponent setClassification={setClassification} />
            )}
            {classification != null && (
                <button onClick={submitAnswer} className='NextButton'>Next</button>
            )}
        </div>
    );
}

export default StudyPage;