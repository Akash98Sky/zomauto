class Item:
    def __init__(self, name: str, type: str, img: str | None, query: str) -> None:
        self.name = name
        self.type = type
        self.img = img
        self.query = query