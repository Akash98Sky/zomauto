import React, { useCallback, useState } from 'react';
import { ItemFilter, RestaurantFilter, SearchFilters } from "../../models/interfaces"
import { SingleFilter } from "./SingleFilter"
import { Button, makeStyles, Tab, TabList } from '@fluentui/react-components';

export interface RestaurantFilterProps {
    filters: SearchFilters,
    onFilterChange?: (filters: SearchFilters) => void
}

const useStyles = makeStyles({
    tab_root: {
        alignItems: "flex-start",
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-start",
        padding: "50px 20px",
        rowGap: "20px",
    },

    filter_list: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'stretch',
        justifyContent: 'center',
        gap: '5px',
    },
});


export default function RestaurantsFilter(props: RestaurantFilterProps) {
    const styles = useStyles();
    const [tab, setTab] = useState<'restaurant' | 'item'>('restaurant');
    const filterMutations = useCallback((type: 'item' | 'restaurant') => {
        return {
            add: () => {
                const filters = [...props.filters[type]];
                filters.push({ field: 'name', operator: 'contains', value: '' });
                props.onFilterChange && props.onFilterChange({ ...props.filters, [type]: filters });
            },
            remove: (index: number) => {
                const filters = [...props.filters[type]];
                filters.splice(index, 1);
                props.onFilterChange && props.onFilterChange({ ...props.filters, [type]: filters });
            },
            update: (filter: RestaurantFilter | ItemFilter, index: number) => {
                const filters = [...props.filters[type]];
                filters[index] = filter;
                props.onFilterChange && props.onFilterChange({ ...props.filters, [type]: filters });
            }
        }
    }, [tab, props.filters, props.onFilterChange]);
    const mutations = filterMutations(tab);
    const restaurantFilters = props.filters['restaurant'];
    const itemFilters = props.filters['item'];

    return (
        <div className={styles.tab_root}>
            <TabList selectedValue={tab} onTabSelect={(_, data) => setTab(data.value as any)}>
                <Tab value='restaurant'>Restaurant Filters</Tab>
                <Tab value='item'>Item Filters</Tab>
            </TabList>

            <div className={styles.filter_list}>
                {tab === 'restaurant' && restaurantFilters.map((filter, index) => (
                    <div key={index}>
                        <SingleFilter filter={filter} type='restaurant' onChange={f => mutations.update(f, index)} onDelete={() => mutations.remove(index)} />
                    </div>
                ))}

                {tab === 'item' && itemFilters.map((filter, index) => (
                    <div key={index}>
                        <SingleFilter filter={filter} type='item' onChange={f => mutations.update(f, index)} onDelete={() => mutations.remove(index)} />
                    </div>
                ))}
            </div>
            <Button size='small' onClick={mutations.add}>Add Filter</Button>
        </div>
    )
}