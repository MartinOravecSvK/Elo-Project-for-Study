import React, { useState } from 'react';
import config from '../../config';
import './TestPage1.css';

function TestPage1({ nextPage, userId, setError, setFailedAttention }) {
    const [selectedEvent1, setSelectedEvent1] = useState(null);
    const [selectedEvent2, setSelectedEvent2] = useState(null);

    const checkThenNext = async () => {
        if (selectedEvent2 === 1) {
            setFailedAttention(true);
            nextPage();
        } else {
            nextPage();
        }
    }

    return (
        <div>
            <h2 className='description'>
                The following 4 questions are to assess your understanding of the terms "better" and "worse". Please select ONE answer per question
            </h2>
            <h3>
                1. Which of these scenarios is <ins className='worse'>WORSE</ins>?
            </h3>
            <div className="events">
                <div
                    className={`event ${selectedEvent1 === 1 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent1(1)}
                >
                    <h2>Budgeting your money wisely to sustain your future goals.</h2>
                </div>
                <div
                    className={`event ${selectedEvent1 === 2 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent1(2)}
                >
                    <h2>Spending all your money impusively and getting into debt and losing your house.</h2>
                </div>
            </div>
            <h3>
                2. Which of these scenarios is <ins className='worse'>WORSE</ins>?
            </h3>
            <div className="events">
                <div
                    className={`event ${selectedEvent2 === 1 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent2(1)}
                >
                    <h2>Feeling safe.</h2>
                </div>
                <div
                    className={`event ${selectedEvent2 === 2 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent2(2)}
                >
                    <h2>Feeling unsafe and in danger.</h2>
                </div>
            </div>
            {selectedEvent1 && selectedEvent2 && <button onClick={checkThenNext} className='NextButton'>Next</button>}
        </div>
    );
}

export default TestPage1;