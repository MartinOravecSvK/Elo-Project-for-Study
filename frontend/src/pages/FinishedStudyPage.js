import React, { useEffect } from 'react';
import { Helmet } from 'react-helmet';
import UoB_CMYK_24 from '../images/UoB_CMYK_24.svg';
import './FinishedStudyPage.css'; 

// TODO:
// - Double check it works as intended
// - Does the prolific_id need to be included in the return link?

function FinishedStudyPage() {
    // Change this code for each study
    // If possible add this to the backend and fetch it from there (store it inside a .env file or similar)
    const completion_code = "C8ZGRGME";

    useEffect(() => {
        const participantId = localStorage.getItem('participant_id');
        if (participantId) {
            // Redirect the participant after a delay
            // For production, change the delay to 5000 (5 seconds)
            setTimeout(() => {
                window.location.href = `https://app.prolific.com/submissions/complete?cc=${completion_code}`;
            }, 5000);
        } else {
            // If participant ID is not found, give them an option to input it manually if it makes sense
        }
    }, []);

    // Tried to integrate the original code for the finished study page into react as best as possible
    return (
        <div className="jspsych-display-element">
            <Helmet>
                <title>End Study</title>
                {/* <meta http-equiv="refresh" content="5; url=https://app.prolific.com/submissions/complete?cc=${completion_code}" /> */}

            </Helmet>
            <div className="jspsych-content-wrapper">
                <div className="jspsych-content">
                    <div style={{ width: '100%' }}>
                        <img
                            style={{ display: 'block', margin: '0 auto', width: '200px', height: 'auto' }}
                            src={UoB_CMYK_24}
                            alt="University of Bristol Logo"
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
                        Please click the link below to go to Prolific
                    </b></p>
                    <p>
                        <b>
                            <a href={`https://app.prolific.com/submissions/complete?cc=${completion_code}`} >
                                Click here to finish study
                            </a>
                        </b>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default FinishedStudyPage;