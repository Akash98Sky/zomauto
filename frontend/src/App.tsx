import React, { Suspense, useDeferredValue, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import {
  FluentProvider,
  webLightTheme,
  Input,
  Label,
  SearchBox,
  Field,
  makeStyles,
  tokens,
  Dropdown
} from "@fluentui/react-components";

import { SearchLocations } from './components/SearchLocations';

const useStyles = makeStyles({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  fieldWrapper: {
    padding: `${tokens.spacingVerticalMNudge} ${tokens.spacingHorizontalMNudge}`,
  },
});


function App() {
  return (
    <FluentProvider theme={webLightTheme}>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
        </header>
        <div>
          <SearchLocations />
        </div>
      </div>
    </FluentProvider>
  );
}

export default App;
