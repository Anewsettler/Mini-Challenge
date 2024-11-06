import { createSlice } from '@reduxjs/toolkit';

const questionSlice = createSlice({
  name: 'question',
  initialState: {
    question: null,
    options: [],
    classification: null,
    attemptCount: 1, 
  },
  reducers: {
    setQuestion: (state, action) => {
      state.question = action.payload.question;
      state.options = action.payload.options;
    },
    setClassification: (state, action) => {
      state.classification = action.payload;
    },
    reset: (state) => {
      state.question = null;
      state.options = [];
      state.classification = null;
      state.attemptCount = 1;
    },
    incrementAttemptCount: (state) => {
      state.attemptCount += 1;
    },
    setAttemptCount: (state, action) => {
      state.attemptCount = action.payload;
    }
  }
});

export const { setQuestion, setClassification, reset, incrementAttemptCount, setAttemptCount } = questionSlice.actions;
export default questionSlice.reducer;
