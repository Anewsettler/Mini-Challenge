import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import URLInput from '../components/URLInput';
import LoadingBar from '../components/LoadingBar';
import Question from '../components/Question';
import ErrorMessage from '../components/ErrorMessage';
import { fetchInitialQuestion, submitAnswer } from '../services/api';
import { startLoading, stopLoading } from '../redux/slices/loadingSlice';
import { setError, clearError } from '../redux/slices/errorSlice';
import { setQuestion, setClassification, reset, incrementAttemptCount } from '../redux/slices/questionSlice';
import '../styles/pages/MainPage.css';

const MainPage = () => {
  const dispatch = useDispatch();
  const question = useSelector((state) => state.question.question);
  const options = useSelector((state) => state.question.options);
  const classification = useSelector((state) => state.question.classification);
  const attemptCount = useSelector((state) => state.question.attemptCount);
  const isLoading = useSelector((state) => state.loading.isLoading);

  const handleUrlSubmit = async (url) => {
    dispatch(reset());
    dispatch(startLoading());
    dispatch(clearError());

    try {
      const responseData = await fetchInitialQuestion(url);
      if (responseData.initial_question && responseData.initial_question.question && responseData.initial_question.options) {
        dispatch(setQuestion(responseData.initial_question));
      } else {
        console.error("Unexpected format in initial_question:", responseData.initial_question);
        dispatch(setError("Failed to retrieve valid question data."));
      }
    } catch (error) {
      console.error("Error in handleUrlSubmit:", error);
      dispatch(setError('Failed to retrieve question. Please try again.'));
    } finally {
      dispatch(stopLoading());
    }
  };

  const handleAnswerSubmit = async (selectedOption) => {
    dispatch(startLoading());
    dispatch(clearError());

    try {
      const result = await submitAnswer({
        user_selection: selectedOption,
        initial_question: { question, options },
        attempt_count: attemptCount 
      });

      if (result.classification) {
        dispatch(setClassification(result.classification));
      } else if (result.initial_question) {
        dispatch(setQuestion(result.initial_question));
        dispatch(incrementAttemptCount()); 
      }
    } catch (error) {
      dispatch(setError('Failed to classify. Please try again.'));
    } finally {
      dispatch(stopLoading());
    }
  };

  return (
    <div>
      <URLInput onSubmit={handleUrlSubmit} />
      <LoadingBar />
      <ErrorMessage />
      {!isLoading && !classification && question && options.length > 0 && (
        <Question question={question} options={options} onSubmit={handleAnswerSubmit} />
      )}
      {classification && <div>Classification Result: {classification}</div>}
    </div>
  );
};

export default MainPage;
