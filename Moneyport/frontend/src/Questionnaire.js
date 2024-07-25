
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';  
import axios from 'axios';
import './Questionnaire.css';

const questions = [
  {
    question: "What is your primary investment goal?",
    options: ["Preserve capital", "Generate income", "Balanced growth and income", "Maximize long-term growth"]
  },
  {
    question: "How long do you plan to hold your investments?",
    options: ["Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"]
  },
  {
    question: "How would you describe your risk tolerance when it comes to investing?",
    options: ["Very low- I am not comfortable with any risk", "Low- I prefer safer investments, even if returns are lower", "Moderate-I am willing to accept some risk for potentially higher return", "High- I am comfortable with significant risk for the potential of high returns"]
  },
  {
    question: "What is your annual income range?",
    options: ["Less than $30,000", "$30,000-$60,000", "$60,000-$100,000", "Greater than $100,000"]
  },
  {
    question: "How would you rate your investment experience?",
    options: ["No experience", "Some experience with basic investments like saving account", "Moderate experience with stocks, bonds and mutual funds", "Extensive experience with various investment types"]
  },
  {
    question: "If your investment suddenly dropped 20% in value, how would you react?",
    options: ["Sell all my investments immediately", "Sell some of my investments", "Hold onto my investments and wait for recovery", "Buy more investments at the lower price"]
  },
  {
    question: "What is your age group?",
    options: ["Over 60", "45-60", "30-45", "Under 30"]
  }
];

function Questionnaire() {
  const [answers, setAnswers] = useState(Array(questions.length).fill(null));
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleOptionSelect = (questionIndex, optionIndex) => {
    const newAnswers = [...answers];
    newAnswers[questionIndex] = optionIndex;
    setAnswers(newAnswers);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (answers.some(answer => answer === null)) {
      setError("Please answer all questions before submitting.");
      return;
    }
    setError(null);
    try {
      const formattedAnswers = {
        investmentGoal: answers[0] + 1,
        timeHorizon: answers[1] + 1,
        riskTolerance: answers[2] + 1,
        income: answers[3] + 1,
        investmentExperience: answers[4] + 1,
        lossReaction: answers[5] + 1,
        age: answers[6] + 1
      };

      console.log('Sending formatted answers:', JSON.stringify(formattedAnswers));

      const response = await axios.post('http://localhost:8080/predict_and_recommend', formattedAnswers);
      navigate('/results', { state: { result: response.data } });
    } catch (error) {
      console.error('Error:', error);
      setError("An error occurred while submitting your answers. Please try again.");
    }
  };

  return (
    <div className="questionnaire-container">
      <h2>Investment Risk Assessment Questionnaire</h2>
      <form onSubmit={handleSubmit}>
        {questions.map((q, qIndex) => (
          <div key={qIndex} className="question-container">
            <h3>Question {qIndex + 1}</h3>
            <p>{q.question}</p>
            {q.options.map((option, oIndex) => (
              <div key={oIndex} className="option-container">
                <input
                  type="radio"
                  id={`q${qIndex}o${oIndex}`}
                  name={`question${qIndex}`}
                  checked={answers[qIndex] === oIndex}
                  onChange={() => handleOptionSelect(qIndex, oIndex)}
                />
                <label htmlFor={`q${qIndex}o${oIndex}`}>{option}</label>
              </div>
            ))}
          </div>
        ))}
        <button type="submit" className="submit-button">Submit</button>
      </form>

      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

export default Questionnaire;