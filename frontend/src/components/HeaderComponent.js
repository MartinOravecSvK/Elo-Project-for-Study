import React from 'react';
import UoB_CMYK_24 from '../images/UoB_CMYK_24.svg';
import './HeaderComponent.css';

function HeaderComponent({ eventsNum, eventsDone, visible }) {

    // Calculate the progress percentage up to 2 decimal places
    const progressPercentage = ((eventsDone / eventsNum) * 100).toFixed(2);

    if (visible === false) {
        return null;
    }

    return (
        <header className='HeaderWrapper'>
            <img
                className='Logo'
                src={UoB_CMYK_24}
                alt="University of Bristol Logo"
            />
            <div className='ProgressContainer'>
                <span>{`${eventsDone} / ${eventsNum} Completed`}</span>
                <div className='ProgressBarWrapper'>
                    <progress className='ProgressBar' value={progressPercentage} max="100"></progress>
                    <div className='ProgressLabel'>{`${progressPercentage}%`}</div>
                </div>
            </div>
            <h1 className='StudyName'>Comparing Life Experiences</h1>
        </header>
    );
}

export default HeaderComponent;