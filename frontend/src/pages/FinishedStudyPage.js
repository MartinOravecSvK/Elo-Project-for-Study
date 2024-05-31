import React from 'react';
import { Helmet } from 'react-helmet';
import './FinishedStudyPage.css';  // Ensure your CSS is being imported here


function FinishedStudyPage() {
    // Tried to integrate the original code for the finished study page into react as best as possible
    return (
        <div className="jspsych-display-element">
            {/* Using Helmet instead of Head as you can't normally directly change head of the html page in react thus we use a  library react-helmet*/}
            <Helmet>
                <title>End Study</title>
                <meta http-equiv="refresh" content="5; url=https://app.prolific.com/submissions/complete?cc=COBF1PK2" />
                <link href="../../jspsych-6.2.0/css/jspsych.css" rel="stylesheet" type="text/css" />
            </Helmet>
            <div className="jspsych-content-wrapper">
                <div className="jspsych-content">
                    <div style={{ width: '100%' }}>
                        <img
                            style={{ display: 'block', margin: '0 auto', width: '200px', height: 'auto' }}
                            src="../UoBlogocolour.png"
                            alt="Logo"
                        />
                    </div>
                    <h2><b>THANK YOU FOR COMPLETING TODAY'S STUDY</b></h2>
                    <p>
                        Please note: If you experience any adverse effects to your mental health please seek help from your
                        usual care providers. If you require immediate help, online advice can be found at{' '}
                        <a href="https://www.samaritans.org/" target="_blank" rel="noopener noreferrer">
                            www.samaritans.org
                        </a>{' '}
                        , or alternatively you can contact a Samaritan free of charge on 116 123 (available 24 hours a day,
                        365 days a year).
                    </p>
                    <p><b>Please click the link below to submit your data and return to Prolific</b></p>
                    <p>
                        <b>
                            <a href="https://app.prolific.com/submissions/complete?cc=COBF1PK2">Click here to finish study</a>
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