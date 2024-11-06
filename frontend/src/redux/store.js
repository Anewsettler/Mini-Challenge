import { configureStore } from '@reduxjs/toolkit';
import loadingReducer from './slices/loadingSlice';
import urlReducer from './slices/urlSlice';
import questionReducer from './slices/questionSlice';
import errorReducer from './slices/errorSlice';

const store = configureStore({
  reducer: {
    loading: loadingReducer,
    url: urlReducer,
    question: questionReducer,
    error: errorReducer
  }
});

export default store; // Default export here
