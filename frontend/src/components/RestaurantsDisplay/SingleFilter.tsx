import React from 'react';
import { Button, Input, makeStyles, Select } from "@fluentui/react-components";
import { ItemFilter, RestaurantFilter, Filter, Restaurant, RestaurantItem } from "../../models/interfaces";

export interface SingleFilterProps<T> {
    filter: T;
    onChange: (filter: T) => void;
    onDelete: () => void;
}

const useStyles = makeStyles({
    filter: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '10px',
    },
    item: {
        flexGrow: 1,
    }
});

export function SingleFilter<T = RestaurantFilter | ItemFilter>(props: SingleFilterProps<T>) {
    const styles = useStyles();
    const [filter, setFilter] = React.useState(props.filter as Filter<Restaurant> | Filter<RestaurantItem>);
    const [lastTimeout, setLastTimeout] = React.useState<NodeJS.Timeout | undefined>();

    const filterOperatorMap: { [key: string]: string[] } = {
        name: ['eq', 'contains'],
        rating: ['gt', 'lt', 'eq']
    }
    const handleChange = (change: { field?: keyof Restaurant | keyof RestaurantItem, op?: 'eq' | 'gt' | 'lt' | 'contains', value?: any }, debounce = false) => {
        const { field, op, value } = change;
        setFilter(filter => ({ ...filter, field: field || filter.field, operator: op || filter.operator, value: value || filter.value }));
        if (debounce) {
            lastTimeout && clearTimeout(lastTimeout);
            setLastTimeout(setTimeout(() => props.onChange(filter as T), 300));
        } else {
            props.onChange(filter as T);
        }
    }

    return (
        <div className={styles.filter}>
            <Select className={styles.item} id='field' size="small" value={filter.field as string} onChange={e => handleChange({ field: e.target.value as any })}>
                {Object.keys(filterOperatorMap).map(field => <option key={field}>{field}</option>)}
            </Select>
            <Select className={styles.item} id='operator' size="small" value={filter.operator} onChange={e => handleChange({ op: e.target.value as any })}>
                {filterOperatorMap[filter.field as string].map(op => <option key={op}>{op}</option>)}
            </Select>
            <Input className={styles.item} id='value' size='small' value={filter.value.toString()} onChange={e => setFilter(f => ({ ...f, value: e.target.value }))} onBlur={e => handleChange({ value: filter.value })} />
            <Button appearance="primary" size="small" onClick={_ => props.onDelete()}>Remove</Button>
        </div>
    );
}