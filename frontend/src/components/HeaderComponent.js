import React from 'react';
import './HeaderComponent.css';

function HeaderComponent() {
    return (
        <header className='HeaderWrapper'>
            <img
                className='Logo'
                src="/UoBLogo.svg"
            />
            <h1 className='StudyName'>Name of the study</h1>
        </header>
    );
}

export default HeaderComponent;