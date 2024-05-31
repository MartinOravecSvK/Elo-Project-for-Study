import React, { useEffect } from 'react';
import { Helmet } from 'react-helmet';
import './FinishedStudyPage.css';  // Ensure your CSS is being imported here

// TODO:
// - Fix broken Logo image path (there is none that is valid)
// - Double check it works as intended
// - Use <img> with script fallbacks to png version (for older IE and android < 3). One clean and simple way to do that: <img src="your.svg" onerror="this.src='your.png'">


function FinishedStudyPage() {

    useEffect(() => {
        const participantId = localStorage.getItem('participant_id');
        if (participantId) {
            // Redirect the participant after a delay
            // For production, change the delay to 5000 (5 seconds)
            setTimeout(() => {
                window.location.href = `https://app.prolific.com/submissions/complete?cc=COBF1PK2&participant_id=${participantId}`;
            }, 500000);
        } else {
            // If participant ID is not found, give them an option to input it manually if it makes sense
        }
    }, []);

    // Tried to integrate the original code for the finished study page into react as best as possible
    return (
        <div className="jspsych-display-element">
            {/* Using Helmet instead of Head as you can't normally directly change head of the html page in react thus we use a  library react-helmet*/}
            <Helmet>
                <title>End Study</title>
                {/* <meta http-equiv="refresh" content="5; url=https://app.prolific.com/submissions/complete?cc=COBF1PK2" /> */}

            </Helmet>
            <div className="jspsych-content-wrapper">
                <div className="jspsych-content">
                    <div style={{ width: '100%' }}>
                        <img
                            style={{ display: 'block', margin: '0 auto', width: '200px', height: 'auto' }}
                            src="/UoBLogo.svg"
                        />
                    </div>
                    <h2><b>
                        THANK YOU FOR COMPLETING TODAY'S STUDY
                    </b></h2>
                    <p>
                        Please note: If you experience any adverse effects to your mental health please seek help from your
                        usual care providers. If you require immediate help, online advice can be found at{' '}
                        <a href="https://www.samaritans.org/" target="_blank" rel="noopener noreferrer">
                            www.samaritans.org
                        </a>{' '}
                        , or alternatively you can contact a Samaritan free of charge on 116 123 (available 24 hours a day,
                        365 days a year).
                    </p>
                    <p><b>
                        Please click the link below to submit your data and return to Prolific
                    </b></p>
                    <p>
                        <b>
                            <a href={`https://app.prolific.com/submissions/complete?cc=COBF1PK2&participant_id=${localStorage.getItem('participant_id')}`} >
                                Click here to finish study
                            </a>
                        </b>
                    </p>
                    <p>
                        If you no longer wish to submit your data to this research study you must close this browser window
                        and withdraw your submission from Prolific.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default FinishedStudyPage;