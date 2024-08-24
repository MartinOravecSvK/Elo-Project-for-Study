import React, { useState } from 'react';
import config from '../../config';
import './TestPage2.css';

function TestPage2({ nextPage, userId, setError, setFailedAttention }) {
    const [selectedEvent1, setSelectedEvent1] = useState(null);
    const [selectedEvent2, setSelectedEvent2] = useState(null);

    const checkThenNext = async () => {
        if (selectedEvent2 === 2) {
            setFailedAttention(true);
            nextPage();
        } else {
            nextPage();
        }
    }

    return (
        <div className='TestPage2Wrapper'>
            <h3>
                3. Which of these scenarios is <ins className='better'>BETTER</ins>?
            </h3>
            <div className="events">
                <div
                    className={`event ${selectedEvent1 === 1 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent1(1)}
                >
                    <h2>I broke my leg.</h2>
                </div>
                <div
                    className={`event ${selectedEvent1 === 2 ? 'selected' : ''}`}
                    onClick={() => setSelectedEvent1(2)}
                >
                    <h2>I found £100 in my desk I didn't know I had.</h2>
                </div>
            </div>
            <h3>
                4. Which of these scenarios is <ins className='better'>BETTER</ins>?
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
            {/* <button onClick={checkThenNext} className='NextButton'>Next</button> */}
        </div>
    );
}

export default TestPage2;