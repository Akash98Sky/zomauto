import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import {
  FluentProvider,
  webLightTheme
} from "@fluentui/react-components";

import RestaurantSearch from './components/RestaurantSearch';
import RestaurantDisplay from './components/RestaurantDisplay';
import { RestaurantSearchQuery } from './models/interfaces';
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  const [searchQuery, setSearchQuery] = useState<RestaurantSearchQuery | undefined>(undefined);

  return (
    <FluentProvider theme={webLightTheme}>
      <Provider store={store}>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
          </header>
          <RestaurantSearch onSearch={(location, item) => setSearchQuery({ location, item })} />
          {searchQuery && <RestaurantDisplay query={searchQuery} />}
        </div>
      </Provider>
    </FluentProvider>
  );
}

export default App;
