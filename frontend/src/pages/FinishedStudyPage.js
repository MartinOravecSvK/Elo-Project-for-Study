import React from 'react';

function FinishedStudyPage() {
    // Tried to integrate the original code for the finished study page into react
    return (
        <div className="jspsych-display-element">
            <head>
                <title>End Study</title>
                {/* <meta http-equiv="refresh" content="5; url=https://app.prolific.com/submissions/complete?cc=COBF1PK2" />
                <link href="../../jspsych-6.2.0/css/jspsych.css" rel="stylesheet" type="text/css" /> */}
            </head>
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