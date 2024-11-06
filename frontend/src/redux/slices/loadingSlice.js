import { createSlice } from '@reduxjs/toolkit';

const loadingSlice = createSlice({
  name: 'loading',
  initialState: { isLoading: false, progress: 0 },
  reducers: {
    startLoading: (state) => { 
      state.isLoading = true; 
      state.progress = 0; 
    },
    stopLoading: (state) => { 
      state.isLoading = false; 
      state.progress = 0; 
    },
    setProgress: (state, action) => {
      state.progress = action.payload;
    }
  }
});

export const { startLoading, stopLoading, setProgress } = loadingSlice.actions;
export default loadingSlice.reducer;
