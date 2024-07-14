from typing import AsyncGenerator
from playwright.async_api import Browser, BrowserContext

from zomato.elements.restaurants_element import RestaurantsElement
from zomato.models.restaurant import Restaurant
from zomato.pages.base_page import BasePage


class RestaurantsPage(BasePage):
    def __init__(self, browser: Browser | BrowserContext, page_url: str = "https://www.zomato.com/bangalore/restaurants") -> None:
        super().__init__(browser, page_url)

    async def __aenter__(self):
        await super().__aenter__()
        self.restaurants = RestaurantsElement(self.page)
        return self

    def browse_restaurants(self, load_atleast: int = 50) -> AsyncGenerator[Restaurant, None]:
        return self.restaurants.browse_restaurants(load_atleast)