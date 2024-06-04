import React from 'react';
import './HeaderComponent.css';

function HeaderComponent({ eventsNum, eventsDone }) {

    // Calculate the progress percentage up to 2 decimal places
    const progressPercentage = ((eventsDone / eventsNum) * 100).toFixed(2);

    return (
        <header className='HeaderWrapper'>
            <img
                className='Logo'
                src="/UoBLogo.svg"
                alt="University of Bristol Logo"
            />
            {/* <div className='ProgressContainer'>
                <progress className='ProgressBar' value={progressPercentage} max="100"></progress>
                <span>{`${eventsDone} / ${eventsNum} completed`}</span>
            </div> */}
            <div className='ProgressContainer'>
                <span>{`${eventsDone} / ${eventsNum} Completed`}</span>
                <div className='ProgressBarWrapper'>
                    <progress className='ProgressBar' value={progressPercentage} max="100"></progress>
                    <div className='ProgressLabel'>{`${progressPercentage}%`}</div>
                </div>
            </div>
            <h1 className='StudyName'>Name of the study</h1>
        </header>
    );
}

export default HeaderComponent;