import React, { useEffect, useState } from 'react';
import { Button, makeStyles } from "@fluentui/react-components";

import { SearchItems } from "./SearchItem";
import { SearchLocations } from "./SearchLocations";
import { ItemSearch, LocationSearch } from '../models/interfaces';

const useStyle = makeStyles({
    searchControl: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
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
    onSearch?: (location: LocationSearch, item: ItemSearch) => void;
}

export default function RestaurantSearch(props: RestaurantSearchProps) {
    const [searchData, setSearchData] = useState<{ location: LocationSearch | undefined, item: ItemSearch | undefined }>({ location: undefined, item: undefined });
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
                <SearchLocations onChange={(location) => {setSearchData(data => ({ ...data, location })); console.log('location', location)}} />
                <SearchItems onChange={(item) => {setSearchData(data => ({ ...data, item })); console.log('item', item)}} />
                <Button 
                    appearance="primary"
                    onClick={() => props.onSearch && props.onSearch(searchData.location!, searchData.item!)}
                    disabled={!searchData.location || !searchData.item}>
                        Search
                </Button>
            </div>
        </div>
    );
}