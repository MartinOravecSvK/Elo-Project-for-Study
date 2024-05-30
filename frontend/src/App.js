import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
    const [events, setEvents] = useState({});

    // Replace 'some-unique-user-id' with a unique identifier for the user (generate some and store it in browser's local storage)
    const userId = 'some-unique-user-id';

    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const response = await fetch(`http://localhost:5000/next?user_id=${userId}`);
            const data = await response.json();
            if (data.events) {
                setEvents(data.events);
                console.log('New events fetched:', data.events)
            } else {
                console.log(data.error || data.message || 'No events found')
                setEvents({});
            }
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    };

    const submitAnswer = async (winnerId) => {
        try {
            const response = await fetch('http://localhost:5000/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    winner_id: winnerId,
                }),
            });
            const data = await response.json();
            if (data.events) {
                setEvents(data.events);
                console.log('New events fetched:', data.events)
            } else {    
                console.log(data.error || data.message || 'No events found')
                setEvents({});
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
        }
    };

    return (
        <div className="App">
            <h1>Choose the Event</h1>
            {events != {} ? (
                <div className="events">
                    <div className="event">
                        <h2>{events.event0_details}</h2>
                        <button onClick={() => submitAnswer(events.event0_ID)}>Choose This Event</button>
                    </div>
                    <div className="event">
                        <h2>{events.event1_details}</h2>
                        <button onClick={() => submitAnswer(events.event1_ID)}>Choose This Event</button>
                    </div>
                </div>
            ) : (
                <p>No more events to show. Study completed!</p>
            )}
        </div>
    );
}

export default App;
