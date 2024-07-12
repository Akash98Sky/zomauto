from typing import AsyncGenerator, Callable
from selenium.webdriver.remote.webdriver import WebDriver

from zomato.elements.navbar_element import NavbarElement
from zomato.elements.restaurant_page_element import RestaurantPageElement
from zomato.elements.restaurants_element import RestaurantsElement
from zomato.elements.search_element import SearchElement
from zomato.models.item import Item
from zomato.models.location import Location
from zomato.models.restaurant import Restaurant, RestaurantItem
from zomato.logger import getLogger

logger = getLogger(__name__)

class Zomato:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        driver.get("https://www.zomato.com/bangalore/")
        driver.implicitly_wait(3)

    def login(self, ph_no: str):
        navbarElement = NavbarElement(self.driver)

        userName = navbarElement.login(ph_no)

        logger.info(userName, 'logged in')

    def logout(self):
        navbarElement = NavbarElement(self.driver)

        navbarElement.logout()

        logger.info('logged out')

    def search_locations(self, query: str, select: Callable[[Location], bool] | None = None) -> list[Location]:
        logger.info('Searching for location: %s', query)
        searchElement = SearchElement(self.driver)

        locations = searchElement.locations(query)

        if select:
            searchElement.update_location(query, [loc for loc in locations if select(loc)][0])

        return locations

    def search_items(self, query: str, select: Callable[[Item], bool] | None = None) -> list[Item]:
        logger.info('Searching for item: %s', query)
        searchElement = SearchElement(self.driver)

        items = searchElement.items(query)

        if select:
            searchElement.find_item(query, [item for item in items if select(item)][0])

        return items
    
    def browse_restaurants(self, at_least: int = 10) -> AsyncGenerator[Restaurant, None]:
        restaurantsElement = RestaurantsElement(self.driver)

        return restaurantsElement.browse_restaurants(at_least)
    
    def get_offers(self, restaurant: Restaurant):
        with RestaurantPageElement(self.driver, restaurant) as page:
            return page.get_offers()
    
    async def get_restaurant_details(self, restaurant: Restaurant, item_contains: str = ''):
        with RestaurantPageElement(self.driver, restaurant) as page:
            offers = [offer async for offer in page.get_offers()]
            items = [item async for item in page.get_all_items(item_contains)]

            return restaurant, offers, items
    
    async def get_items(self, restaurant: Restaurant, query: str) -> AsyncGenerator[RestaurantItem, None]:
        with RestaurantPageElement(self.driver, restaurant) as page:
            async for itemcat in page.get_all_items(query):
                for item in itemcat.items:
                    if query.lower() in itemcat.name.lower() or query.lower() in item.name.lower():
                        yield item