import React, { useState } from 'react';
import './ClassificationComponent.css';

function ClassificationComponent({ setClassification }) {
    const [selectedClassification, setSelectedClassification] = useState(null);

    const handleClassificationClick = (classification) => {
        setSelectedClassification(classification);
        setClassification(classification);
    };

    return (
        <div className='ClassificationWrapper'>
            <h1 className='question'>
                Would you classify this as a "Daily" or "Major" life event?
            </h1>
            <div className='ClassificationButtons'>
                {['Daily', 'Major'].map((classification) => (
                    <div
                        key={classification}
                        className={`classification-button ${selectedClassification === classification ? 'selected' : ''}`}
                        onClick={() => handleClassificationClick(classification)}
                    >
                        {classification}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ClassificationComponent;
