import React, { useEffect } from 'react';
import { Helmet } from 'react-helmet';
import UoB_CMYK_24 from '../images/UoB_CMYK_24.svg';
import './FailedPage.css';

function FailedPage() {
    return (
        <div className="jspsych-display-element">
            <Helmet>
                <title>End Study</title>
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
                    <p>
                        Sorry! Your answers to question 2 and question 4 do not suggest that you understand the terms “better” and “worse”. This also suggests that you might not have read the questions carefully or that you are not fluent in English, both of which are required for this study.
                    </p>
                    <p><b>
                        Please return your submission within 7 days.
                    </b></p>
                    <p>
                        If the link below is not working you can return the submission from your 'Submissions page', by selecting the red circular arrow to 'Return + cancel reward'.
                    </p>
                    <p><b>
                        Please follow the link below to return your submission without penalty.
                    </b></p>
                    <p>
                        <b>
                            {/* Change this link of course */}
                            <a href={`https://app.prolific.com/submissions/complete?cc=C19Z7RII`} >
                                CLICK HERE TO RETURN TO PROLIFIC
                            </a>
                        </b>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default FailedPage;