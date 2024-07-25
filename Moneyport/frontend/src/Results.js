import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import './Results.css';

function Results() {
  const location = useLocation();
  const result = location.state?.result;

  const openYFinance = (symbol) => {
    window.open(`https://finance.yahoo.com/quote/${symbol}`, '_blank');
  };

  if (!result) {
    return <div>No results to display. Please complete the questionnaire.</div>;
  }

  return (
    <div className="results-container">
      <h2>Your Investment Profile</h2>
      <h3>Risk Profile: <span className="risk-level">{result.risk_level}</span></h3>
      <h4>Recommended Stocks:</h4>
      <ul className="stock-list">
        {result.recommended_stocks.map((stock, index) => (
          <li key={index} className="stock-item">
            <div className="stock-info">
              <span className="stock-name">{stock.name}</span>
              <span className="stock-symbol">({stock.symbol})</span>
              <span className="stock-price">Current Price: ${stock.current_price}</span>
            </div>
            <button className="yfinance-button" onClick={() => openYFinance(stock.symbol)}>
              View on Yahoo Finance
            </button>
          </li>
        ))}
      </ul>
      <Link to="/" className="back-button">Back to Questionnaire</Link>
    </div>
  );
}

export default Results;