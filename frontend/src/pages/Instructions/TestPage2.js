import React from 'react';
import './TestPage2.css';

function TestPage2({ nextPage }) {
    return (
        <div className='TestPage2Wrapper'>
            <h1>Test Page 2</h1>
            <button onClick={nextPage} className='NextButton'>Next</button>
        </div>
    );
}

export default TestPage2;