import asyncio
from typing import Any
import uuid
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from backend.browser import instance
from backend.cache import CacheManager
from backend.logger import getLogger
from backend.models.query import Query
from zomato.models.restaurant import Restaurant

logger = getLogger(__name__)
worker = None


def worker_instance():
    global worker
    if worker is None:
        worker = QueryWorker()
    return worker

class Work:
    def __init__(self, id: uuid.UUID, task: asyncio.Task, data = None, completed: bool = False):
        self.id = id
        self.task = task
        self.completed = completed
        self.data = data


class QueryWorker:

    def __init__(self):
        self.cachemgr = CacheManager("restaurants")
        self.works: dict[uuid.UUID, Work] = {}
        self.zomato = instance()

    async def __query(self, q: Query, data: list[Any] = []):
        def func(restaurant: Restaurant):
            def inner_func():
                return self.zomato.get_restaurant_details(restaurant)
            return inner_func
        
        try:
            restaurants = [restaurant async for restaurant in self.zomato.browse_restaurants(q.location, q.item, q.at_least)]
            for restaurant in restaurants:
                key = restaurant.href
                try:
                    details = await self.cachemgr.cached(key, func(restaurant), expire=28800)    # cache for 8 hours
                    data.append(details)
                except PlaywrightTimeoutError as e:
                    logger.warning('Restaurant "%s" timed out, Error: %s', restaurant.name, e, exc_info=True)
        except Exception as e:
            logger.error(e, exc_info=True)

        return data

    def enqueue(self, query: Query):
        data = []
        work = Work(
            id = uuid.uuid4(),
            task = asyncio.create_task(self.__query(query, data)),
            data = data
        )
        self.works[work.id] = work

        return work

    def check_result(self, result_id: str):
        work = self.works.get(uuid.UUID(result_id))
        if work is not None and work.task.done():
            work.completed = True
        return work