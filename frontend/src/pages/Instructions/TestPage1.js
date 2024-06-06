import React, { useState } from 'react';
import './TestPage1.css';

function TestPage1({ nextPage }) {
    const [selectedEvent0, setSelectedEvent0] = useState(null);
    const [selectedEvent1, setSelectedEvent1] = useState(null);

    const checkThenNext = () => {
        if (selectedEvent1 === 0) {
            // Add backend endpoint to block this user
            alert('Select sensible answer');
        } else {
            nextPage();
        }
    }

    return (
        <div>
            <h1>Test to check understand better/worse judgements</h1>
            <h2 className='description'>
                The following 4 questions are to asses your understanding of the terms "better" and "worse". Please select ONE answer per question
            </h2>
            <h3>
                1. Which of these scenarios is <ins className='worse'>WORSE</ins>?
            </h3>
            <div className="events">
                <div
                    className={`event ${selectedEvent0 === 0 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent0(0)}
                >
                    <h2>Budgeting your money wisely to sustain your future goals.</h2>
                </div>
                <div
                    className={`event ${selectedEvent0 === 1 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent0(1)}
                >
                    <h2>Spending all your money impusively and getting into debt and losing your house.</h2>
                </div>
            </div>
            <h3>
                2. Which of these scenarios is <ins className='worse'>WORSE</ins>?
            </h3>
            <div className="events">
                <div
                    className={`event ${selectedEvent1 === 0 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent1(0)}
                >
                    <h2>Feeling safe.</h2>
                </div>
                <div
                    className={`event ${selectedEvent1 === 1 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent1(1)}
                >
                    <h2>Feeling unsafe and in danger.</h2>
                </div>
            </div>
            <button onClick={checkThenNext} className='NextButton'>Next</button>
        </div>
    );
}

export default TestPage1;