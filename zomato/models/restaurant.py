import re

from pydantic import BaseModel

class Restaurant(BaseModel):
    name: str
    type: str
    img: str | None
    rating: float
    href: str
    offers_available: bool
    location: str | None = None

    def __init__(self, name: str, type: str, img: str | None, rating: str, href: str, offers_available: bool, location: str | None = None) -> None:
        try:
            frating = float(rating)
        except ValueError:
            frating = 0.0
        super().__init__(
            name=name,
            type=type,
            img=img,
            rating=frating,
            href=href,
            offers_available=offers_available,
            location=location
        )

class RestaurantOffer(BaseModel):
    code: str
    discount_str1: str
    discount_str2: str
    discount_percent: int
    max_discount_amount: int
    min_order_value: int

    def __init__(self, code: str, discount_str1: str, discount_str2: str) -> None:
        disc_percent = re.match(r'Get ([0-9]*)% OFF up to ₹([0-9]*)', discount_str1)
        flat_disc = re.match(r'[\w\s]*Flat ₹([0-9]*) OFF', discount_str1)
        flat_disc_percent = re.match(r'[\w\s]*Flat ([0-9]*)% OFF', discount_str1)
        min_order = re.match(r'Valid on [\w\s]* items worth ₹([0-9]*) or more\.', discount_str2)

        if disc_percent:
            discount_percent = int(disc_percent.group(1))
            max_discount_amount = int(disc_percent.group(2))
        elif flat_disc:
            discount_percent = 100
            max_discount_amount = int(flat_disc.group(1))
        elif flat_disc_percent:
            discount_percent = int(flat_disc_percent.group(1))
            max_discount_amount = 999999 # representing infinite
        else:
            discount_percent = 0
            max_discount_amount = 0

        if min_order:
            min_order_value = int(min_order.group(1))
        else:
            min_order_value = 0

        super().__init__(
            code=code,
            discount_str1=discount_str1,
            discount_str2=discount_str2,
            discount_percent=discount_percent,
            max_discount_amount=max_discount_amount,
            min_order_value=min_order_value
        )

class RestaurantItem(BaseModel):
    name: str
    rating: float
    price: float
    discounted_price: float
    img: str | None

    def __init__(self, name: str, rating: float, price: str, img: str | None = None) -> None:
        try:
            fprice = float(price.removeprefix('₹'))
        except ValueError:
            fprice = 0.0
        super().__init__(
            name=name,
            rating=rating,
            price=fprice,
            discounted_price=fprice,
            img=img
        )
    
class RestaurantItemCategory(BaseModel):
    name: str
    items: list[RestaurantItem]

    def __init__(self, name: str, items: list[RestaurantItem]) -> None:
        super().__init__(name=name, items=items)
    

class RestaurantDetails(BaseModel):
    restaurant: Restaurant
    offers: list[RestaurantOffer]
    items: list[RestaurantItemCategory]

    def __init__(self, restaurant: Restaurant, offers: list[RestaurantOffer], items: list[RestaurantItemCategory]) -> None:
        super().__init__(restaurant=restaurant, offers=offers, items=items)
