import React from "react";
import "./InstructionPage2.css";

function InstructionPage2({ nextPage }) {
    return (
        <div className="InstructionWrapper">
            {/* <h1>Instruction screen 2</h1> */}
            <h2 className="instrucion-header">THERE ARE NO RIGHT OR WRONG ANSWERS IN THIS TASK.</h2>
            <p>
                We simply want to understand public opinion when comparing life events.
            </p>
            <h3>
                ◆
            </h3>
            <p>
                After reading both scenarios presented, please select the option that you intuitively believe is better or worse. Do not spend too much time trying to consider the scenarios in a wider context than how they have been presented.
            </p>
            <p>
                <b>When you are ready to start the study press the button at the bottom of this screen.</b>
            </p>
            <button onClick={nextPage} className='NextButton'>Next</button>
        </div>
    );
}

export default InstructionPage2;