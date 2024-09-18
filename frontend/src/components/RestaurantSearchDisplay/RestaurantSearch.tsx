import React, { useEffect, useState } from 'react';
import { Button, Input, makeStyles } from "@fluentui/react-components";

import { SearchItems } from "./SearchItem";
import { SearchLocations } from "./SearchLocations";
import { ItemSearch, LocationSearch } from '../../models/interfaces';

const useStyle = makeStyles({
    searchControl: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '10px',
    },
    row: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'stretch',
        gap: '10px',
    }
})

const useStyleMd = makeStyles({
    searchControl: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'end',
        justifyContent: 'center',
        gap: '10px',
    }
})

interface RestaurantSearchProps {
    onSearch?: (location: LocationSearch, item: ItemSearch, atLeast: number) => void;
    disableSearch?: boolean;
}

export default function RestaurantSearch(props: RestaurantSearchProps) {
    const [searchData, setSearchData] = useState<{ location: LocationSearch | undefined, item: ItemSearch | undefined }>({ location: undefined, item: undefined });
    const [atLeast, setAtLeast] = useState(10);

    const [width, setWidth] = useState(window.innerWidth);
    const style = useStyle();

    const styleMd = useStyleMd();
    const isMd = width >= 768;

    useEffect(() => {
        const handleResize = () => setWidth(window.innerWidth);
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <div>
            <h1>Restaurant Search</h1>
            <div className={isMd ? styleMd.searchControl : style.searchControl}>
                <SearchLocations onChange={(location) => { setSearchData(data => ({ ...data, location })); console.log('location', location) }} />
                <SearchItems onChange={(item) => { setSearchData(data => ({ ...data, item })); console.log('item', item) }} />
                <div className={style.row}>
                    <Input placeholder="No of restaurants to search" type='number' min={1} max={50} value={atLeast.toString()} onChange={(e) => setAtLeast(parseInt(e.target.value))} />
                    <Button
                        appearance="primary"
                        onClick={() => props.onSearch && props.onSearch(searchData.location!, searchData.item!, atLeast)}
                        disabled={props.disableSearch || !searchData.location || !searchData.item}>
                        Search
                    </Button>
                </div>
            </div>
        </div>
    );
}