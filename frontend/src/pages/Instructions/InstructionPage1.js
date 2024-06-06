import React from 'react';
import './InstructionPage1.css';

function InstructionPage1({ nextPage }) {


    return (
        <div className='InstructionWrapper'>
            <h1>Instruction screen 1</h1>
            <button onClick={nextPage} className='NextButton'>Next</button>
        </div>
    );
}

export default InstructionPage1;