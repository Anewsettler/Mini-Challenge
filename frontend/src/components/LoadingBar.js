import React from 'react';
import { useSelector } from 'react-redux';
import '../styles/components/LoadingBar.css';

const LoadingBar = () => {
  const isLoading = useSelector((state) => state.loading.isLoading);

  return isLoading ? (
    <div className="loading-container">
      <div className="spinner"></div>
      <p className="loading-text">Loading</p>
    </div>
  ) : null;
};

export default LoadingBar;
