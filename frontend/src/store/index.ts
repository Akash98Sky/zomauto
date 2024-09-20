import { configureStore } from "@reduxjs/toolkit";
import { zomautoApi } from "./reducers/zomautoApi";
import restaurantsReducer from "./reducers/restaurants";
import { useDispatch, useSelector } from "react-redux";

export const store = configureStore({
    reducer: {
        [zomautoApi.reducerPath]: zomautoApi.reducer,
        restaurants: restaurantsReducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(zomautoApi.middleware),
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch = useDispatch.withTypes<AppDispatch>()
export const useAppSelector = useSelector.withTypes<RootState>()