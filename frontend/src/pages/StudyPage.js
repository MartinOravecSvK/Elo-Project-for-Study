import React, { useEffect, useState } from 'react';
import './StudyPage.css';

import ExperienceComponent from '../components/ExperienceComponent';
import CategoryComponent from '../components/CategoryComponent';
import ClassificationComponent from '../components/ClassificationComponent';

// TODO:
// - Make it easy to toggle Categories

function StudyPage({ setFinishedStudy, setEventsNum, setEventsDone, worseStart, blockSize }) {
    const useCategory = true;
    const useClassification = true;
    const [events, setEvents] = useState({});
    const [counter, setCounter] = useState(0);

    // event ID of the event with more negative sentiment
    const [loser_id, setLoser_id] = useState(null);
    // event ID of the event with more positive sentiment
    const [winner_id, setWinner_id] = useState(null);

    // Right now just using the more negative event ID and deriving the other on the backend
    // const [morePositive, setMorePositive] = useState(null);
    
    // Category of the event with more negative sentiment
    // Categories include: [Health, Financial, Relationship, Bereavement, Work, Crime]
    const [category, setCategory] = useState(null);

    // Classification, Daily or Major
    const [classification, setClassification] = useState(null);

    // Replace 'some-unique-user-id' with a unique identifier for the user (generate some and store it in browser's local storage)
    const userId = localStorage.getItem('user_id') || null;
    console.log('User ID:', userId);

    if (!userId) {
        console.error('User ID not found in local storage');
    }

    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const response = await fetch(`http://localhost:5000/next?user_id=${userId}`);
            const data = await response.json();
            if (data.events) {
                setEvents(data.events);
                // For production, remove console.log
                console.log('New events fetched:', data.events)
                setEventsDone(data.progress.current_completed);
                setEventsNum(data.progress.number_of_questions);
            } else {
                // For production, remove console.log 
                console.log(data.error || data.message || 'No events found')
                setEvents({});
                // Check to see if the study is completed
                if (data.message === 'Study completed') {
                    setFinishedStudy(true);
                    setEventsDone(data.progress.current_completed);
                    setEventsNum(data.progress.number_of_questions);
                }
            }
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

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

        try {
            console.log(counter, blockSize, worseStart)
            // These statements handle switching for different questions
            // Asking which scenario is worse and which is better
            if (counter <= blockSize && worseStart) {
                let temp = loser_id;
                setLoser_id(winner_id);
                setWinner_id(temp);
            } else if(counter > blockSize && !worseStart) {
                let temp = loser_id;
                setLoser_id(winner_id);
                setWinner_id(temp);
            }
            setCounter(counter + 1);

            const response = await fetch('http://localhost:5000/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    loser_id: loser_id,
                    winner_id: winner_id,
                    category: category,
                    classification: classification,
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
            // Reset the states
            setLoser_id(null);
            setWinner_id(null);
            setCategory(null);
            setClassification(null);
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    };

    return (
        <div className='StudyPage'>
            {events && Object.keys(events).length > 0 ? (
                <ExperienceComponent 
                    setLoser_id={setLoser_id} 
                    setWinner_id={setWinner_id} events={events}  
                    counter={counter} 
                    blockSize={blockSize} 
                    worseStart={worseStart}
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