import React, { useState } from 'react';
import './ExperienceComponent.css';

function ExperienceComponent({ setLoser_id, setWinner_id, events, counter, blockSize, worseStart, setPolarization }) {
    const [selectedEvent, setSelectedEvent] = useState(null);

    const handleEventClick = (winnerEventId, loserEventId) => {
        setSelectedEvent(winnerEventId);
        setLoser_id(loserEventId);
        setWinner_id(winnerEventId);
    };

    let question = <span>In your opinion, which of these scenarios is <span className="highlight-better">BETTER</span></span>;
    const shouldSwitch = (counter < blockSize && worseStart) || (counter >= blockSize && !worseStart);
    if (shouldSwitch) {
        setPolarization('negative');
        question = <span>In your opinion, which of these scenarios is <span className="highlight-worse">WORSE</span></span>;
    } else {
        setPolarization('positive');
    }

    return (
        <div className='ExperienceWrapper'>
            <h1 className='experience_question'>
                {question}
            </h1>
            <div className="events">
                <div
                    className={`event ${selectedEvent === events.event0_ID ? 'selected' : ''}`}
                    onClick={() => handleEventClick(events.event0_ID, events.event1_ID)}
                >
                    <h2>{events.event0_details}</h2>
                </div>
                <div
                    className={`event ${selectedEvent === events.event1_ID ? 'selected' : ''}`}
                    onClick={() => handleEventClick(events.event1_ID, events.event0_ID)}
                >
                    <h2>{events.event1_details}</h2>
                </div>
            </div>
        </div>
    );
}

export default ExperienceComponent;