import React from "react";
import "./InstructionPage2.css";

function InstructionPage2({ nextPage }) {
    return (
        <div className="InstructionWrapper">
            <h1>Instruction screen 2</h1>
            <button onClick={nextPage} className='NextButton'>Next</button>
        </div>
    );
}

export default InstructionPage2;