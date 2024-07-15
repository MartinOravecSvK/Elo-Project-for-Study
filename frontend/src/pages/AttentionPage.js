import React from 'react';
import './AttentionPage.css';

const AttentionPage = ({ word, onContinue }) => {
  const displayWord = word.toUpperCase();

  if (displayWord === 'BETTER') {
    word = <span className="highlight-better">BETTER</span>;
  } else {
    word = <span className="highlight-worse">WORSE</span>;
  }

  return (
    <div className="attention-page">
      <h1>ATTENTION: Change of Question Wording</h1>
      <p>
        From this point forward, we would like to understand which of the two scenarios presented you think is {word}.
        The questions in the following section of the task will all be phrased as follows:
      </p>
      <p className="question">
        “IN YOUR OPINION, WHICH OF THESE SCENARIOS IS {word}?”
      </p>
      <button className="continue-button" onClick={onContinue}>Continue</button>
    </div>
  );
}

export default AttentionPage;