import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { setUrl } from '../redux/slices/urlSlice';
import { clearError } from '../redux/slices/errorSlice';
import { setQuestion } from '../redux/slices/questionSlice';
import '../styles/components/URLInput.css';

const URLInput = ({ onSubmit }) => {
  const dispatch = useDispatch();
  const [inputUrl, setInputUrl] = useState('');
  const [isValid, setIsValid] = useState(true);

  const validateUrl = (url) => {
    const urlPattern = /^(https?:\/\/)?([\w-]+(\.[\w-]+)+)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?$/;
    return urlPattern.test(url);
  };  

  const handleSubmit = () => {
    if (!validateUrl(inputUrl)) {
      setIsValid(false);
      return;
    }
    setIsValid(true);
    dispatch(setUrl(inputUrl));
    dispatch(clearError());
    dispatch(setQuestion({}));
    onSubmit(inputUrl);
  };

  return (
    <div className="url-input-container">
      <input
        type="text"
        value={inputUrl}
        placeholder="Enter a valid URL"
        onChange={(e) => setInputUrl(e.target.value)}
        className={isValid ? 'input-valid' : 'input-invalid'}
      />
      <button onClick={handleSubmit}>Start Scrape</button>
      {!isValid && <p className="error-text">Please enter a valid URL</p>}
    </div>
  );
};

export default URLInput;
