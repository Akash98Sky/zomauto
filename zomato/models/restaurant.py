import re

class Restaurant:
    def __init__(self, name: str, type: str, img: str | None, rating: str, href: str | None, offers_available: bool) -> None:
        self.name = name
        self.type = type
        self.img = img
        try:
            self.rating = float(rating)
        except ValueError:
            self.rating = 0
        self.href = href
        self.offers_available = offers_available

    def __str__(self) -> str:
        return self.to_dict().__str__()
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "img": self.img,
            "rating": self.rating,
            "href": self.href,
            "offers_available": self.offers_available
        }

class RestaurantOffer:
    def __init__(self, code: str, discount_str1: str, discount_str2: str) -> None:
        self.code = code
        self.discount_str1 = discount_str1
        self.discount_str2 = discount_str2

        disc_percent = re.match(r'Get ([0-9]*)% OFF up to ₹([0-9]*)', discount_str1)
        flat_disc = re.match(r'[\w\s]*Flat ₹([0-9]*) OFF', discount_str1)
        flat_disc_percent = re.match(r'[\w\s]*Flat ([0-9]*)% OFF', discount_str1)
        min_order = re.match(r'Valid on [\w\s]* items worth ₹([0-9]*) or more\.', discount_str2)

        if disc_percent:
            self.discount_percent = int(disc_percent.group(1))
            self.max_discount_amount = int(disc_percent.group(2))
        elif flat_disc:
            self.discount_percent = 100
            self.max_discount_amount = int(flat_disc.group(1))
        elif flat_disc_percent:
            self.discount_percent = int(flat_disc_percent.group(1))
            self.max_discount_amount = 999999 # representing infinite
        else:
            self.discount_percent = 0
            self.max_discount_amount = 0

        if min_order:
            self.min_order_value = int(min_order.group(1))
        else:
            self.min_order_value = 0

    def __str__(self) -> str:
        return self.to_dict().__str__()
    
    def to_dict(self) -> dict:
        return {
            "code": str(self.code),
            "discount_str1": str(self.discount_str1),
            "discount_str2": str(self.discount_str2),
            "discount_percent": self.discount_percent,
            "max_discount_amount": self.max_discount_amount,
            "min_order_value": self.min_order_value
        }

class RestaurantItem:
    def __init__(self, name: str, rating: float, price: str) -> None:
        self.name = name
        self.rating = rating
        self.price = float(price.removeprefix('₹'))

    def __str__(self) -> str:
        return self.to_dict().__str__()
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "rating": self.rating,
            "price": self.price
        }
    
class RestaurantItemCategory:
    def __init__(self, name: str, items: list[RestaurantItem]) -> None:
        self.name = name
        self.items = items

    def __str__(self) -> str:
        return self.to_dict().__str__()
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "items": [item.to_dict() for item in self.items]
        }