import React from 'react';
import { Button, Input, makeStyles, Select } from "@fluentui/react-components";
import { ItemFilter, RestaurantFilter, Filter, Restaurant, RestaurantItem, FilterOperator } from "../../models/interfaces";

export interface SingleFilterProps<T> {
    filter: T;
    type: 'restaurant' | 'item';
    onChange: (filter: T) => void;
    onDelete: () => void;
}

const restaurantFields = ['name', 'rating'];
const itemFields = ['name', 'rating', 'price', 'discounted_price'];
const filterOperatorMap: { [key: string]: FilterOperator[] } = {
    name: ['eq', 'contains'],
    rating: ['gt', 'lt', 'eq'],
    price: ['gt', 'lt', 'eq'],
    discounted_price: ['gt', 'lt', 'eq'],
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

    const fieldList = props.type === 'restaurant' ? restaurantFields : itemFields;
    const handleChange = (change: { field?: keyof Restaurant | keyof RestaurantItem, op?: FilterOperator, value?: any }) => {
        const { field, op, value } = change;
        const updatedFilter = { ...filter, field: field || filter.field, operator: op || filter.operator, value: value || filter.value };
        setFilter(updatedFilter);
        props.onChange(updatedFilter as T);
    }

    return (
        <div className={styles.filter}>
            <Select className={styles.item} id='field' size="small" value={filter.field as string} onChange={e => handleChange({ field: e.target.value as any, op: filterOperatorMap[filter.field as string][0] })}>
                {fieldList.map(field => <option key={field}>{field}</option>)}
            </Select>
            <Select className={styles.item} id='operator' size="small" value={filter.operator} onChange={e => handleChange({ op: e.target.value as any })}>
                {filterOperatorMap[filter.field as string].map(op => <option key={op} value={op}>{op}</option>)}
            </Select>
            <Input className={styles.item} id='value' size='small' value={filter.value.toString()} onChange={e => setFilter(f => ({ ...f, value: e.target.value }))} onBlur={e => handleChange({ value: filter.value })} />
            <Button appearance="primary" size="small" onClick={_ => props.onDelete()}>Remove</Button>
        </div>
    );
}