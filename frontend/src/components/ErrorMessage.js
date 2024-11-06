import React from 'react';
import { useSelector } from 'react-redux';
import '../styles/components/ErrorMessage.css';

const ErrorMessage = () => {
  const errorMessage = useSelector((state) => state.error.message);

  return errorMessage ? (
    <div className="error-message">
      <span className="error-icon">⚠️</span>
      {errorMessage}
    </div>
  ) : null;
};

export default ErrorMessage;
