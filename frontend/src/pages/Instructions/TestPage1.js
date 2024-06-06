import React from 'react';
import './TestPage1.css';

function TestPage1({ nextPage }) {
    return (
        <div>
            <h1>Test Page 1</h1>
            <button onClick={nextPage} className='NextButton'>Next</button>
        </div>
    );
}

export default TestPage1;