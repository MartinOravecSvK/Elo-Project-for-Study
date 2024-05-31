import React, { useEffect, useState } from 'react';
import './StudyPage.css';

import ExperienceComponent from '../components/ExperienceComponent';
import CategoryComponent from '../components/CategoryComponent';
import ClassificationComponent from '../components/ClassificationComponent';

function StudyPage({ setFinishedStudy }) {
    const [events, setEvents] = useState({});
    // event ID of the event with more negative sentiment
    const [moreNegative, setMoreNegative] = useState(null);
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
            } else {
                // For production, remove console.log 
                console.log(data.error || data.message || 'No events found')
                setEvents({});
                // Check to see if the study is completed
                if (data.message === 'Study completed') {
                    setFinishedStudy(true);
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

        if (!moreNegative) {
            // Change this to show a message to the user
            console.error('More negative event ID not found');
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
            const response = await fetch('http://localhost:5000/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    winner_id: moreNegative,
                    category: category,
                    classification: classification,
                }),
            });
            const data = await response.json();
            if (data.events) {
                setEvents(data.events);
                console.log('New events fetched:', data.events)
            } else {    
                console.log(data.error || data.message || 'No events found')
                setEvents({});
                if (data.message === 'Study completed') {
                    setFinishedStudy(true);
                }
            }
            // Reset the states
            setMoreNegative(null);
            setCategory(null);
            setClassification(null);
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    };

    return (
        <div className='StudyPage'>
            {events != {} ? ExperienceComponent({ setMoreNegative, events }) : <p>No more events to show. Study completed!</p>}
            {moreNegative != null ? CategoryComponent({ setCategory }) : null}
            {category != null ? ClassificationComponent({ setClassification }) : null}
            {classification != null ? <button onClick={submitAnswer} className='NextButton'>Submit</button> : null}
        </div>
    );
}

export default StudyPage;