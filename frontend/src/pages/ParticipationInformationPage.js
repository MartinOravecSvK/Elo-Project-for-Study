import React from 'react';
import './ParticipantInformationPage.css';
import UoB_CMYK_24 from '../images/UoB_CMYK_24.svg';

const ParticipantInformationPage = ({ nextPage }) => {
  const consent = () => {
    nextPage();
  }

  return (
    <div className="container">
        <img
            style={{ display: 'block', margin: '0 auto', width: '300px', height: 'auto' }}
            src={UoB_CMYK_24}
            alt="University of Bristol Logo"
        />
        <header>
            <h1>Participant Information Sheet</h1>
        </header>

        <section>
            <h2>Comparing Life Experiences</h2>
            <p>
                You are invited to take part in a research study to compare statements about life experiences. 
                Before you decide whether to participate, please read the following study information carefully 
                so you understand what will be required in this research study. If anything is unclear or you 
                have any questions, please contact us for more information (contact details provided below). 
                Take your time to decide whether you would like to take part and please remember your 
                participation is entirely voluntary.
            </p>

            <h3>What is this study about?</h3>
            <p>
                The purpose of this study is to better understand judgements of life experiences. The life 
                experience statements used in this study vary widely. Some statements may refer to everyday 
                occurrences e.g. losing an item; other statements may refer to more impactful life events e.g. 
                loss of a loved one. By asking you to compare these differing types of statements we aim to 
                understand how the general public ranks various life experiences.
            </p>

            <h3>What will you have to do?</h3>
            <p>
                10 minutes for £1.91<br/>
                You will be asked to compare multiple pairs of statements that refer to life experiences. 
                You will have to decide which of the statements is comparatively better or worse than the 
                other depending on the phrasing of the question when these statements are presented to you. 
                You will answer by clicking a button referring to the statement you have chosen.<br/>
                Each session should take around 10 minutes to complete. When completing the study make sure 
                to have the webpage in full-screen mode and ensure that you will not be distracted during the 
                time taken to complete the assessment.
            </p>

            <p>To take part in the study you will need to confirm that you:</p>
            <ul>
                <li>are between 18-30 years of age</li>
                <li>are currently living in the UK</li>
                <li>are a fluent English speaker</li>
                <li>are currently not taking any medication for a mental health condition</li>
            </ul>

            <h3>What is your reward?</h3>
            <p>You will be paid £1.91 for successful completion.</p>

            <h3>Do I have to take part?</h3>
            <p>
                Participation in this study is entirely voluntary. If you decide you would like to go ahead 
                with the study and take part, we will ask you to provide electronic consent. You are free to 
                withdraw at any time without giving a reason. You can withdraw by simply closing the browser 
                and not continuing with the study. However, you will only be reimbursed for a fully completed assessment.
            </p>

            <h3>Ethics</h3>
            <p>
                This study has been given ethical approval by the Research Ethics Committee of the University of
                Bristol (School of Psychology, Ethics approval code 21823). No risks or adverse effects have been
                identified, and no personal identifying information will be available to researchers unless you choose
                to provide it. By taking part in this University of Bristol research there will be no identifiable health
                benefits to you. It is important to understand that the research team will not be monitoring
                responses in real-time for any urgent or distressing content. Therefore, if you have an immediate
                need for support or are in a crisis, we strongly advise you to seek appropriate help from a qualified
                professional or contact helpline services available in your area (<a href="http://www.samaritans.org" target="_blank" rel="noopener noreferrer">www.samaritans.org</a> are available 24/7, 365 days a year).
                If you have any questions about the research, feel free to contact us before starting the study.
            </p>

            <p>
                If you have any questions about the research, feel free to contact us before starting the study.
            </p>

            <h3>What would happen to the results of the research study?</h3>
            <p>
                When the study has been completed, we will analyse the study data we have collected and report
                the findings. This may be reported in an appropriate scientific journal or presented at a scientific
                meeting. As your study data are anonymised, it will not be possible to identify you by name from any
                aspect of documentation or reporting for this research study. Your participation in the study is
                completely anonymous, we do not store your name or identity and your name will not be in any way
                linked to the data.
            </p>
            <p>
                You will not have access to any individual data collected during the study and at the end of the study
                your data would become “open data”
            </p>
            <p>
                Open data means that the data will be stored in an online database that is publicly available to
                anyone interested in the research. We will therefore have no control over how these data are used.
                However, all data will be anonymised and Prolific IDs will be removed before the data are made
                available. There will be no way to identify you from the research data.
            </p>
            <p>
                If you consent, you agree to the University of Bristol keeping and processing the information that
                you have provided during the study. Your consent is conditional on the University complying with its
                duties and obligations under the Data Protection Act
            </p>

            <h3>Can I withdraw my study data after I have participated in the study?</h3>
            <p>
                It is not possible to withdraw any responses you have given up to the point you either finish the
                study or discontinue with the study. Each response you give within this study is added into a live
                "score" which adjusts based on all participants' data. This score will change over the study as it goes
                along; in short, the questions are chosen based on the previous answers and so it is not possible to
                retract any answer after it is submitted. If you no longer wish to participate you can leave the study,
                this will mean that no further data is collected but will not withdraw the data you have already
                provided.
                All data collected from you is anonymised and initially identified by your Prolific ID. At completion of
                the study your Prolific ID is replaced by a numeric identifier. At this point links between your identity
                and your anonymised data set will be destroyed.
            </p>

            <p>
                If you have any questions about the study, please contact us using Prolific Messenger or 
                at <a href="mailto:xo20940@bristol.ac.uk">xo20940@bristol.ac.uk</a>. Thank you!
            </p>
        </section>

      <section className="consent-section">
        <h2>Participant Consent Form</h2>
        <h3>Comparing Life Experiences</h3>
        <p>By clicking the ‘I consent’ button below you agree to the following:</p>
        <ul>
          <li>I have received information about the tasks involved in this research study and been given the opportunity to ask questions.</li>
          <li>I have received enough information about the study to make an informed decision to participate and I understand my participation is completely voluntary.</li>
          <li>I understand that after the study the data will be made “open data”. I understand that this means the anonymised data will be publicly available and may be used for purposes not related to this study. I understand my participation is anonymous and my name will not be recorded when the data are collected and when released publicly it will be labelled only by a numerical identifier.</li>
          <li>I am aware I am free to withdraw from the study at any time without giving a reason for doing so.</li>
        </ul>
        <p>If you are happy to proceed with the study please press the consent button below. Otherwise please close this browser window.</p>

        <button onClick={consent} className="consent-button">I Consent</button>
      </section>
    </div>
  );
};

export default ParticipantInformationPage;
