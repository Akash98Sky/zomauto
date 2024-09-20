import React, { useEffect } from 'react';

import { ItemSearch, LocationSearch } from '../../models/interfaces';
import { useGetResultByIdQuery, useLazyQueryRestaurantsByItemQuery } from '../../store/reducers/zomautoApi';
import RestaurantSearch from './RestaurantSearch';
import { useAppDispatch } from '../../store';
import { updateRestaurants } from '../../store/reducers/restaurants';
import { ProgressBar } from '@fluentui/react-components';

interface RestaurantSearchDisplayProps {
    onComplete?: () => void;
}

type RestaurantSearchDisplayState = 'initial' | 'search' | 'search_initiated' | 'waiting' | 'completed' | 'error';

export default function RestaurantSearchDisplay(props: RestaurantSearchDisplayProps) {
    const dispatch = useAppDispatch();
    const [state, setState] = React.useState<RestaurantSearchDisplayState>('initial');
    const [queryRestaurantById, searchQueryResult] = useLazyQueryRestaurantsByItemQuery();
    const { isFetching, isError, isSuccess, data: result } = useGetResultByIdQuery(searchQueryResult?.currentData?.result_id!, { skip: state !== 'search_initiated' && state !== 'waiting', pollingInterval: 10000 });

    useEffect(() => {
        if (searchQueryResult.isSuccess) {
            setState('search_initiated');
        } else if (searchQueryResult.isError) {
            setState('error');
        }
    }, [searchQueryResult.isSuccess, searchQueryResult.isFetching]);

    useEffect(() => {
        if (isFetching) {
            setState('waiting');
        } else if (isError) {
            setState('error');
        } else if (isSuccess && result?.completed) {
            setState('completed');
            props.onComplete && props.onComplete();
        }
    }, [isFetching, isError, isSuccess]);

    useEffect(() => {
        if (result?.data)
            dispatch(updateRestaurants(result.data));
    }, [result]);

    const restaurants = result?.data;
    const onSearch = (location: LocationSearch, item: ItemSearch, atLeast: number) => {
        setState('search');
        queryRestaurantById({ location, item, at_least: atLeast });
    }

    return (
        <div>
            <RestaurantSearch onSearch={onSearch} disableSearch={state === 'search' || state === 'search_initiated' || state === 'waiting'} />
            <h1>Restaurant Display</h1>
            {state === 'waiting' ? <ProgressBar />: <ProgressBar value={1} /> }
            {state === 'error' && <p>Failed to load!</p>}
        </div>
    );
}