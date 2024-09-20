import React from 'react';
import logo from './logo.svg';
import './App.css';
import {
  FluentProvider,
  webLightTheme
} from "@fluentui/react-components";

import { Provider } from 'react-redux';
import { store } from './store';
import RestaurantSearchDisplay from './components/RestaurantSearchDisplay';
import RestaurantsDisplay from './components/RestaurantsDisplay';

function App() {
  return (
    <FluentProvider theme={webLightTheme}>
      <Provider store={store}>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
          </header>
          
          <RestaurantSearchDisplay />
          <RestaurantsDisplay />
        </div>
      </Provider>
    </FluentProvider>
  );
}

export default App;
