import React, { useState, useEffect } from 'react';
import '../styles/components/Question.css';

const Question = ({ question, options, onSubmit }) => {
    const [selectedOption, setSelectedOption] = useState('');

    useEffect(() => {
        console.log("Received question and options in Question component:", { question, options });
    }, [question, options]);

    const handleSubmit = () => {
        if (selectedOption) {
            onSubmit(selectedOption);
        }
    };

    return (
        <div className="question-container">
            <h3 className="question-title">{question || 'No question available'}</h3>
            <ul className="question-options">
                {options && options.length > 0 ? (
                    options.map((option, index) => (
                        <li key={index} className="option-item">
                            <label>
                                <input
                                    type="radio"
                                    value={option}
                                    checked={selectedOption === option}
                                    onChange={() => setSelectedOption(option)}
                                />
                                {option}
                            </label>
                        </li>
                    ))
                ) : (
                    <p className="no-options">No options available</p>
                )}
            </ul>
            <button onClick={handleSubmit} disabled={!selectedOption} className="submit-button">
                Submit
            </button>
        </div>
    );
};

export default Question;
