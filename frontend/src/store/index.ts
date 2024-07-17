import { configureStore } from "@reduxjs/toolkit"
import { zomautoApi } from "./reducers/zomautoApi"

export const store = configureStore({
    reducer: {
        [zomautoApi.reducerPath]: zomautoApi.reducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(zomautoApi.middleware),
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch