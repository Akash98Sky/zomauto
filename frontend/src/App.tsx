import React, { Suspense, useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';
import {
  FluentProvider,
  webLightTheme
} from "@fluentui/react-components";

import RestaurantSearch from './components/RestaurantSearch';
import RestaurantDisplay from './components/RestaurantDisplay';
import { ItemSearch, LocationSearch, RestaurantDetail } from './models/interfaces';
import { postData, PromiseResponse } from './utils/fetchData';

function App() {
  const [searchQuery, setSearchQuery] = useState<{ location: LocationSearch, item: ItemSearch } | undefined>(undefined);
  const [data, setData] = useState<PromiseResponse<RestaurantDetail[]>>();
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    if (!searchQuery || processing) return;

    try {
      console.log('searchQuery', searchQuery);
      setProcessing(true);
      setData(postData<RestaurantDetail[]>(`/api/query`, searchQuery));
    } catch (e) {
      console.log(e);
    }
  }, [searchQuery]);

  const restaurants = data?.read();
  if (restaurants && processing) setProcessing(false);

  return (
    <FluentProvider theme={webLightTheme}>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
        </header>
        <RestaurantSearch onSearch={(location, item) => setSearchQuery({ location, item })} />
        <Suspense fallback={processing ? <>Loading...</> : <></>}>
          {restaurants && <RestaurantDisplay restaurants={restaurants} />}
        </Suspense>
      </div>
    </FluentProvider>
  );
}

export default App;
