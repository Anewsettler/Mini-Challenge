import React from 'react';
import { Provider } from 'react-redux';
import store from './redux/store';
import './App.css';
import MainPage from './pages/MainPage';

function App() {
  return (
    <Provider store={store}>
      <div className="App">
        <MainPage />
      </div>
    </Provider>
  );
}

export default App;
