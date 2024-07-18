import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import {
  FluentProvider,
  webLightTheme
} from "@fluentui/react-components";

import RestaurantSearch from './components/RestaurantSearch';
import RestaurantDisplay from './components/RestaurantDisplay';
import { ItemSearch, LocationSearch, RestaurantSearchQuery } from './models/interfaces';
import { Provider } from 'react-redux';
import { store } from './store';

function App() {
  const [searchQuery, setSearchQuery] = useState<RestaurantSearchQuery | undefined>(undefined);
  const [searching, setSearching] = useState(false);

  const onSearch = (location: LocationSearch, item: ItemSearch, atLeast: number) => {
    setSearching(true);
    setSearchQuery({ location, item, at_least: atLeast });
  }

  return (
    <FluentProvider theme={webLightTheme}>
      <Provider store={store}>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
          </header>
          <RestaurantSearch onSearch={onSearch} disableSearch={searching} />
          {searchQuery && <RestaurantDisplay query={searchQuery} onComplete={() => setSearching(false)} />}
        </div>
      </Provider>
    </FluentProvider>
  );
}

export default App;
