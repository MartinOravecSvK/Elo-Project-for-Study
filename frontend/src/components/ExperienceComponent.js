import React, { useState } from 'react';
import './ExperienceComponent.css';

function ExperienceComponent({ setLoser_id, setWinner_id, events, counter, blockSize, worseStart }) {
    const [selectedEvent, setSelectedEvent] = useState(null);

    const handleEventClick = (winnerEventId, loserEventId) => {
        setSelectedEvent(winnerEventId);
        setLoser_id(loserEventId);
        setWinner_id(winnerEventId);
    };

    console.log("ExperienceComponent: ", counter, blockSize, worseStart)
    let question = 'From the two experiences below, select the more better:';
    const shouldSwitch = (counter < blockSize && worseStart) || (counter >= blockSize && !worseStart);
    if (shouldSwitch) {
        question = 'From the two experiences below, select the more negative:';
    }

    return (
        <div className='ExperienceWrapper'>
            <h1 className='question'>
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