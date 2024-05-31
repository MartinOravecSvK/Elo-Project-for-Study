import React from 'react';
import './HeaderComponent.css';

function HeaderComponent({ eventsNum, eventsDone }) {

    const progressPercentage = (eventsDone / eventsNum) * 100;

    return (
        <header className='HeaderWrapper'>
            <img
                className='Logo'
                src="/UoBLogo.svg"
                alt="University of Bristol Logo"
            />
            <div className='ProgressContainer'>
                <progress className='ProgressBar' value={progressPercentage} max="100"></progress>
                <span>{`${eventsDone} / ${eventsNum} completed`}</span>
            </div>
            <h1 className='StudyName'>Name of the study</h1>
        </header>
    );
}

export default HeaderComponent;