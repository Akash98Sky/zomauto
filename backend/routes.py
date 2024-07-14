import logging
from fastapi import Depends, FastAPI, HTTPException

from zomato.zomato import Zomato
from .browser import instance

api_routes = FastAPI()


@api_routes.get("/locations")
async def read_locations(q: str, zomato: Zomato = Depends(instance)):
    try:
        return await zomato.search_locations(q)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400)