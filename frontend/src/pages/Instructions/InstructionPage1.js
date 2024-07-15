import React, { useState } from 'react';
import './InstructionPage1.css';

function InstructionPage1({ nextPage }) {

    const [selectedEvent, setSelectedEvent] = useState(null);

    return (
        <div className='InstructionWrapper'>
            <h2 className='instrucion-header'>Significant Event Scenarios List</h2>
            <p>
                <b>Participant Instructions:</b>
            </p>
            <p>
                You will be presented with <b>two statements</b> that represent <b>different scenarios</b> that may impact a person's mood. For each pair of statements, you need to decide <ins>in your opinion</ins> which scenario is <ins className='better'>BETTER</ins> or <ins className='worse'>WORSE</ins>, depending on the <b>specific instruction at the of the screen.</b> E.G.:
            </p>
            <h3>
                IN YOUR OPINION, WHICH OF THESE SCENARIOS IS <ins className='better'>BETTER</ins>?
            </h3>
            <div className="events">
                <div
                    className={`event ${selectedEvent === 0 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent(0)}
                >
                    <h2>My dog is sick.</h2>
                </div>
                <div
                    className={`event ${selectedEvent === 1 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent(1)}
                >
                    <h2>I wanted to go out for a walk but it started raining and now my clothes are wet.</h2>
                </div>
            </div>
            <button onClick={nextPage} className='NextButton'>Next</button>
        </div>
    );
}

export default InstructionPage1;