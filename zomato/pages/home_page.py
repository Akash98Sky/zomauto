from playwright.async_api import Browser, BrowserContext

from zomato.elements.navbar_element import NavbarElement
from zomato.elements.restaurants_element import RestaurantsElement
from zomato.models.item import Item
from zomato.models.location import Location
from zomato.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, browser: Browser | BrowserContext, page_url: str = "https://www.zomato.com/bangalore") -> None:
        super().__init__(browser, page_url)

    async def __aenter__(self):
        await super().__aenter__()
        self.navbar = NavbarElement(self.page)
        return self

    def login(self, ph_no: str):
        return self.navbar.login(ph_no)
    
    def logout(self):
        return self.navbar.logout()

    def locations(self, query: str):
        return self.navbar.locations(query)
    
    def update_location(self, query: str, location: Location):
        return self.navbar.update_location(query, location)

    def items(self, query: str):
        return self.navbar.items(query)
    
    async def goto_restaurants_page(self, at: Location, serving: Item):
        await self.navbar.update_location(at.query, at)
        await self.navbar.find_item(serving.query, serving)
        await self._page.wait_for_load_state("networkidle")

        return RestaurantsElement(self._page)