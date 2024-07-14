from playwright.async_api import Browser, BrowserContext

from zomato.elements.restaurant_details_element import RestaurantDetailsElement
from zomato.models.restaurant import Restaurant
from zomato.pages.base_page import BasePage


class RestaurantDetailsPage(BasePage):
    def __init__(self, browser: Browser | BrowserContext, restaurant: Restaurant) -> None:
        super().__init__(browser, f"https://www.zomato.com{restaurant.href}")
        self.restaurant = restaurant

    async def __aenter__(self):
        await super().__aenter__()
        self.restaurant_element = RestaurantDetailsElement(self.page, self.restaurant)
        return self

    def get_offers(self):
        return self.restaurant_element.get_offers()
    
    def get_items(self, containing: str):
        return self.restaurant_element.get_all_items(containing)
    