import logging
from fastapi import Depends, FastAPI, HTTPException

from backend.cache import CacheManager
from backend.models.query import Query
from zomato.models.item import Item
from zomato.models.location import Location
from zomato.models.restaurant import Restaurant
from zomato.zomato import Zomato
from .browser import instance

api_routes = FastAPI()


@api_routes.get("/locations")
async def read_locations(q: str, zomato: Zomato = Depends(instance), cachemgr: CacheManager = Depends(lambda: CacheManager("locations"))):
    def func():
        return zomato.search_locations(q)
    try:
        if q.strip() == "":
            return list[Location]([])
        return await cachemgr.cached(q, func)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)
    
@api_routes.get("/items")
async def read_items(q: str, zomato: Zomato = Depends(instance), cachemgr: CacheManager = Depends(lambda: CacheManager("items"))):
    def func():
        return zomato.search_items(q)
    try:
        if q.strip() == "":
            return list[Item]([])
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
            try:
                details = await cachemgr.cached(key, func(restaurant), expire=28800)    # cache for 8 hours
                data.append(details)
            except TimeoutError as e:
                logging.warning('Restaurant "%s" timed out, Error: %s', restaurant.name, e, exc_info=True)

        return data
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)