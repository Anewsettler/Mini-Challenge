import { createSlice } from '@reduxjs/toolkit';

const urlSlice = createSlice({
  name: 'url',
  initialState: { url: '' },
  reducers: {
    setUrl: (state, action) => { state.url = action.payload; }
  }
});

export const { setUrl } = urlSlice.actions;
export default urlSlice.reducer;
