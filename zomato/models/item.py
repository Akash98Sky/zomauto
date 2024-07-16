from pydantic import BaseModel

class Item(BaseModel):
    name: str
    type: str
    img: str | None
    query: str
    
    def __init__(self, name: str, type: str, img: str | None, query: str) -> None:
        super().__init__(
            name=name,
            type=type,
            img=img,
            query=query
        )