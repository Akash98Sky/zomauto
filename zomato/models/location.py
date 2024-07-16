from pydantic import BaseModel

class Location(BaseModel):
    line1: str
    line2: str
    query: str

    def __init__(self, line1: str, line2: str, query: str) -> None:
        super().__init__(
            line1=line1,
            line2=line2,
            query=query
        )