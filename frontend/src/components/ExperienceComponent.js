import React, { useState } from 'react';
import './ExperienceComponent.css';

function ExperienceComponent({ setMoreNegative, events }) {
    const [selectedEvent, setSelectedEvent] = useState(null);

    const handleEventClick = (eventId) => {
        setSelectedEvent(eventId);
        setMoreNegative(eventId);
    };

    return (
        <div className='ExperienceWrapper'>
            <h1>
                From the two experiences below, select the worst/more negative:
            </h1>
            <div className="events">
                <div
                    className={`event ${selectedEvent === events.event0_ID ? 'selected' : ''}`}
                    onClick={() => handleEventClick(events.event0_ID)}
                >
                    <h2>{events.event0_details}</h2>
                </div>
                <div
                    className={`event ${selectedEvent === events.event1_ID ? 'selected' : ''}`}
                    onClick={() => handleEventClick(events.event1_ID)}
                >
                    <h2>{events.event1_details}</h2>
                </div>
            </div>
        </div>
    );
}

export default ExperienceComponent;