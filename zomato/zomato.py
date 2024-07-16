from typing import AsyncGenerator, Callable, Literal
from playwright.async_api import async_playwright
import platform
from os import path
import shutil

from zomato.models.item import Item
from zomato.models.location import Location
from zomato.models.restaurant import Restaurant, RestaurantItem
from zomato.logger import getLogger
from zomato.pages.home_page import HomePage
from zomato.pages.restaurant_details_page import RestaurantDetailsPage

logger = getLogger(__name__)

class Zomato:
    def __init__(
        self,
        browser_type: Literal["msedge", "chrome"] = "msedge",
        browser_args: list[str] = [],
        headless: bool = False,
        devtools: bool = False,
        user_agent: str | None = None,
    ) -> None:
        self.headless = headless
        self.devtools = devtools
        self.browser_type = browser_type
        self.browser_args = browser_args
        self.user_agent = user_agent

    def browser_executable_path(self, browser_type: str) -> str | None:
        exec_path = None
        
        # check if os is windows
        if platform.system().lower() == "windows":
            if browser_type == "msedge":
                exec_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            elif browser_type == "chrome":
                if path.exists("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"):
                    exec_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                elif path.exists("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"):
                    exec_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        else:
            exec_path = shutil.which(f"{browser_type}")

        if not exec_path:
            raise Exception(f"Could not find {browser_type} executable path")

        return exec_path

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            executable_path=self.browser_executable_path(browser_type=self.browser_type),
            headless=self.headless,
            devtools=self.devtools,
            args=self.browser_args
        )
        self.browser = await self.browser.new_context(
            user_agent=self.user_agent,
        )
        return self
    
    async def __aexit__(self, exc_type, exc, traceback):
        await self.browser.close()
        await self.playwright.stop()

    async def login(self, ph_no: str):
        async with HomePage(self.browser) as home:
            userName = await home.login(ph_no)

            logger.info(userName, 'logged in')

    async def logout(self):
        async with HomePage(self.browser) as home:
            await home.logout()

            logger.info('logged out')

    async def search_locations(self, query: str, select: Callable[[Location], bool] | None = None) -> list[Location]:
        logger.info('Searching for location: %s', query)
        async with HomePage(self.browser) as home:
            locations = await home.locations(query)

            if select:
                await home.update_location(query, [loc for loc in locations if select(loc)][0])

            return locations

    async def search_items(self, query: str) -> list[Item]:
        logger.info('Searching for item: %s', query)
        async with HomePage(self.browser) as home:
            items = await home.items(query)

            return items
    
    async def browse_restaurants(self, at: Location, serving: Item, at_least: int = 10) -> AsyncGenerator[Restaurant, None]:
        async with HomePage(self.browser) as home:
            restaurants_page = await home.goto_restaurants_page(at, serving)
            async for restaurant in restaurants_page.browse_restaurants(at_least):
                yield restaurant
    
    async def get_offers(self, restaurant: Restaurant):
        async with RestaurantDetailsPage(self.browser, restaurant) as restaurant_page:
            return restaurant_page.get_offers()
    
    async def get_restaurant_details(self, restaurant: Restaurant, item_contains: str = ''):
        async with RestaurantDetailsPage(self.browser, restaurant) as restaurant_page:
            offers = [offer async for offer in restaurant_page.get_offers()]
            items = [item async for item in restaurant_page.get_items(item_contains)]

            return restaurant, offers, items
    
    async def get_items(self, restaurant: Restaurant, query: str) -> AsyncGenerator[RestaurantItem, None]:
        async with RestaurantDetailsPage(self.browser, restaurant) as restaurant_page:
            async for itemcat in restaurant_page.get_items(query):
                for item in itemcat.items:
                    if query.lower() in itemcat.name.lower() or query.lower() in item.name.lower():
                        yield item