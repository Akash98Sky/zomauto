import logging
from fastapi import Depends, FastAPI, HTTPException

from backend.cache import CacheManager
from backend.models.query import Query
from backend.worker import QueryWorker, worker_instance
from zomato.models.item import Item
from zomato.models.location import Location
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
async def query(query: Query, worker: QueryWorker = Depends(worker_instance)):
    try:
        work = worker.enqueue(query)
        return { "result_id": work.id, "completed": work.completed }
    except Exception as e:
        logging.error(e, exc_info=True)
        raise HTTPException(status_code=400)
    
@api_routes.get("/result")
async def read_result(id: str, worker: QueryWorker = Depends(worker_instance)):
    result = worker.check_result(id)

    if result is None:
        raise HTTPException(status_code=404, detail="Result not found")

    return {
        "result_id": result.id,
        "completed": result.completed,
        "data": result.task.result() if result.completed else result.data
    }