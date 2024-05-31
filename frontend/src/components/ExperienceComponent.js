import React from 'react';
import './ExperienceComponent.css';

function ExperienceComponent({ setMoreNegative, events }) {
    return (
        <div className='ExperienceWrapper'>
            <h1>
                From he two experiences below, select the worst/more negative:
            </h1>
            <div className="events">
                <div className="event">
                    <h2>{events.event0_details}</h2>
                    <button onClick={() => setMoreNegative(events.event0_ID)}>Choose This Event</button>
                </div>
                <div className="event">
                    <h2>{events.event1_details}</h2>
                    <button onClick={() => setMoreNegative(events.event1_ID)}>Choose This Event</button>
                </div>
            </div>
        </div>
    );
}

export default ExperienceComponent;