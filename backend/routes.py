import logging
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from zomato.models.item import Item
from zomato.models.location import Location
from zomato.zomato import Zomato
from .browser import instance

api_routes = FastAPI()

class Query(BaseModel):
    location: Location
    item: Item
    at_least: int = 10


@api_routes.get("/locations")
async def read_locations(q: str, zomato: Zomato = Depends(instance)):
    try:
        return await zomato.search_locations(q)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)
    
@api_routes.get("/items")
async def read_items(q: str, zomato: Zomato = Depends(instance)):
    try:
        return await zomato.search_items(q)
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)
    
@api_routes.post("/query")
async def query(query: Query, zomato: Zomato = Depends(instance)):
    data = []
    try:
        restaurants = [restaurant async for restaurant in zomato.browse_restaurants(query.location, query.item, query.at_least)]
        for restaurant in restaurants:
            restaurant, offers, items = await zomato.get_restaurant_details(restaurant)
            data.append({
                "restaurant": restaurant.to_dict(),
                "offers": [o.to_dict() for o in offers],
                "items": [category.to_dict() for category in items]
            })

        return data
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)