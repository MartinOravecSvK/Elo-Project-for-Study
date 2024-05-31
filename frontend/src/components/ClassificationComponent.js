import React from 'react';
import './ClassificationComponent.css';

function ClassificationComponent({ setClassification }) {
    return (
        <div className='ClassificationWrapper'>
            <h1>
                Would you classify this as a "Daily" or "Major" life event?
            </h1>
            <div className='ClassificationButtons'>
                <button onClick={() => setClassification('Daily')}>Daily</button>
                <button onClick={() => setClassification('Major')}>Major</button>
            </div>
        </div>
    );
}

export default ClassificationComponent;