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
                        Sorry! Your answers to question 2 and 4 do not suggest you have paid attention to the instructions required for completing this task.
                    </p>
                    <p>
                        Please do not attempt to continue with this task as you will not be reimbursed for this study as per Prolific valid reasons for rejection:
                        The participant objectively demonstrated clear low-effort.
                    </p>
                    <p><b>
                        Please follow the link below to return your submission without penalty.
                    </b></p>
                    <p>
                        <b>
                            {/* Change this link of course */}
                            <a href={`https://app.prolific.com/`} >
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