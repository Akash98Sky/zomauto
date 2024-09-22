import { createSlice } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import { Filter, Restaurant, RestaurantDetail, RestaurantItem, RestaurantSearchQuery, SearchFilters } from '../../models/interfaces';

// Define a type for the slice state
interface RestautantsState {
  query?: RestaurantSearchQuery;
  restaurants: RestaurantDetail[];
  filters: SearchFilters;
  filteredRestaurants: RestaurantDetail[];
}

// Load values from session storage
const previousQuery = sessionStorage.getItem('query')
const previousRestaurantsRaw = sessionStorage.getItem('restaurants')
const previousRestaurants = previousRestaurantsRaw ? JSON.parse(previousRestaurantsRaw) : undefined

// Define the initial state using that type
const initialState: RestautantsState = {
  query: previousQuery ? JSON.parse(previousQuery!) : undefined,
  restaurants: previousRestaurants,
  filters: { restaurant: [], item: [] },
  filteredRestaurants: previousRestaurants
}

const applyFilters = <T = Restaurant | RestaurantItem>(item: T, filters: Filter<T>[]) => {
  if (!filters) {
    return true
  }
  return filters.every(f => {
    if (f.operator === 'eq') {
      return item[f.field] == f.value
    } else if (f.operator === 'gt') {
      return item[f.field] && parseFloat(item[f.field]!.toString()) > parseFloat(f.value.toString())
    } else if (f.operator === 'lt') {
      return item[f.field] && parseFloat(item[f.field]!.toString()) < parseFloat(f.value.toString())
    } else if (f.operator === 'contains') {
      return item[f.field]?.toString().toLowerCase().includes(f.value.toString().toLowerCase())
    }
  });
}

export const restaurantsSlice = createSlice({
  name: 'restaurants',
  // `createSlice` will infer the state type from the `initialState` argument
  initialState,
  reducers: {
    setQuery: (state, action: PayloadAction<RestaurantSearchQuery>) => {
      state.query = action.payload;

      sessionStorage.setItem('query', JSON.stringify(action.payload));
      sessionStorage.removeItem('restaurants');
      console.debug('set query', action.payload);
    },
    updateRestaurants: (state, action: PayloadAction<RestaurantDetail[]>) => {
      state.restaurants = action.payload;
      state.filteredRestaurants = action.payload.filter(r => applyFilters(r.restaurant, state.filters.restaurant)).map(r => ({
        restaurant: r.restaurant,
        offers: r.offers,
        items: r.items.map(cat => ({
          name: cat.name,
          items: cat.items.filter(item => applyFilters(item, state.filters.item))
        }))
      })).filter(r => r.items.some(cat => cat.items.length > 0));

      sessionStorage.setItem('restaurants', JSON.stringify(action.payload));
    },
    updateFilters: (state, action: PayloadAction<SearchFilters>) => {
      state.filters = action.payload;
      state.filteredRestaurants = state.restaurants.filter(r => applyFilters(r.restaurant, state.filters.restaurant)).map(r => ({
        restaurant: r.restaurant,
        offers: r.offers,
        items: r.items.map(cat => ({
          name: cat.name,
          items: cat.items.filter(item => applyFilters(item, state.filters.item))
        }))
      })).filter(r => r.items.some(cat => cat.items.length > 0));
    }
  },
})

export const { setQuery, updateRestaurants, updateFilters } = restaurantsSlice.actions;

export default restaurantsSlice.reducer;