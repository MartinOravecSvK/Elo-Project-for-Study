import React, { useState } from 'react';
import './InstructionPage1.css';

function InstructionPage1({ nextPage }) {

    const [selectedEvent, setSelectedEvent] = useState(null);

    return (
        <div className='InstructionWrapper'>
            <h1>Instruction screen 1</h1>
            <p>
                You will be presented with <b>two statements</b> that represent <b>different scenarios</b> that may impact a person's mood. For each pair of statements, you need to decide <ins>in your opinion</ins> which scenario is <ins className='better'>BETTER</ins> or <ins className='worse'>WORSE</ins>, depending on the <b>specific instruction at the of the screen.</b> E.G.:
            </p>
            <h3>
                From the two experiences below, select the less/more better:
            </h3>
            <div className="events">
                <div
                    className={`event ${selectedEvent === 0 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent(0)}
                >
                    <h2>My partner cheated on me</h2>
                </div>
                <div
                    className={`event ${selectedEvent === 1 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent(1)}
                >
                    <h2>I missed a flight and had to pay extra to hire a car.</h2>
                </div>
            </div>
            <button onClick={nextPage} className='NextButton'>Next</button>
        </div>
    );
}

export default InstructionPage1;