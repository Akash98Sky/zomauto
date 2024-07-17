import logging
from fastapi import Depends, FastAPI, HTTPException
from fastapi_cache.decorator import cache

from backend.cache import CacheManager
from backend.models.query import Query
from zomato.models.restaurant import Restaurant
from zomato.zomato import Zomato
from .browser import instance

api_routes = FastAPI()


@api_routes.get("/locations")
async def read_locations(q: str, zomato: Zomato = Depends(instance), cachemgr: CacheManager = Depends(lambda: CacheManager("locations"))):
    try:
        def func():
            return zomato.search_locations(q)
        return await cachemgr.cached(q, func)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)
    
@api_routes.get("/items")
async def read_items(q: str, zomato: Zomato = Depends(instance), cachemgr: CacheManager = Depends(lambda: CacheManager("items"))):
    try:
        def func():
            return zomato.search_items(q)
        return await cachemgr.cached(q, func)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)
    
@api_routes.post("/query")
async def query(query: Query, zomato: Zomato = Depends(instance), cachemgr: CacheManager = Depends(lambda: CacheManager("restaurants"))):
    data = []
    def func(restaurant: Restaurant):
        def inner_func():
            return zomato.get_restaurant_details(restaurant)
        return inner_func
    try:
        restaurants = [restaurant async for restaurant in zomato.browse_restaurants(query.location, query.item, query.at_least)]
        for restaurant in restaurants:
            key = restaurant.href
            details = await cachemgr.cached(key, func(restaurant), expire=28800)    # cache for 8 hours
            data.append(details)

        return data
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)