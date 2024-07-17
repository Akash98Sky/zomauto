from pydantic import BaseModel

from zomato.models.item import Item
from zomato.models.location import Location

class Query(BaseModel):
    location: Location
    item: Item
    at_least: int = 10