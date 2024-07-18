// Need to use the React-specific entry point to import createApi
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { ItemSearch, LocationSearch, RestaurantDetail, RestaurantSearchQuery } from '../../models/interfaces'

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || ''

// Define a service using a base URL and expected endpoints
export const zomautoApi = createApi({
  reducerPath: 'zomautoApi',
  baseQuery: fetchBaseQuery({ baseUrl: BACKEND_URL + '/api/' }),
  endpoints: (builder) => ({
    getItemsByName: builder.query<ItemSearch[], string>({
      query: (name) => `items?q=${name}`,
    }),
    getLocationsByName: builder.query<LocationSearch[], string>({
      query: (name) => `locations?q=${name}`,
    }),
    queryRestaurantsByItem: builder.query<RestaurantDetail[], RestaurantSearchQuery>({
      query: (search) => ({ method: 'POST', url: 'query', body: search }),
    }),
  }),
})

// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const { useLazyGetItemsByNameQuery, useLazyGetLocationsByNameQuery, useQueryRestaurantsByItemQuery, useLazyQueryRestaurantsByItemQuery } = zomautoApi