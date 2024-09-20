export interface ItemSearch {
    name: string;
    type: string;
    img: string;
}

export interface LocationSearch {
    line1: string;
    line2: string;
}

export interface RestaurantSearchQuery {
    location: LocationSearch;
    item: ItemSearch;
    at_least?: number;
}

export interface QueryResult<T> {
    result_id: string;
    completed: boolean;
    data: T;
}

export interface RestaurantDetail {
    restaurant: Restaurant;
    offers: RestaurantOffer[];
    items: RestaurantItemCategory[];
}

export interface RestaurantItemCategory {
    name: string;
    items: RestaurantItem[];
}

export interface RestaurantItem {
    name: string;
    rating: number;
    price: number;
    discounted_price: number;
    img?: string;
}

export interface RestaurantOffer {
    code: string;
    discount_str1: string;
    discount_str2: string;
    discount_percent: number;
    max_discount_amount: number;
    min_order_value: number;
}

export interface Restaurant {
    name: string;
    type: string;
    img: string;
    rating: number;
    href: string;
    offers_available: boolean;
}

export interface SearchFilters {
    restaurant: RestaurantFilter[];
    item: ItemFilter[];
}

export type FilterOperator = 'eq' | 'gt' | 'lt' | 'contains';

export interface Filter<T> {
    field: keyof T;
    operator: FilterOperator;
    value: string | number;
}

export type RestaurantFilter = Filter<Restaurant>;

export type ItemFilter = Filter<RestaurantItem>;
