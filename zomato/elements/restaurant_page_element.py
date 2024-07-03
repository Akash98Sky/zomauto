import asyncio
import time
from typing import AsyncGenerator
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from zomato.elements.base_element import BaseElement
from zomato.models.restaurant import Restaurant, RestaurantItem, RestaurantItemCategory, RestaurantOffer
from zomato.logger import getLogger

logger = getLogger(__name__)

class RestaurantPageElement(BaseElement):
    def __init__(self, driver: WebDriver, restaurant: Restaurant):
        super().__init__(driver, "//div[@id='root']/div/main")
        self._restaurant = restaurant

    def __enter__(self):
        self.main_window_handle = self.driver.current_window_handle
        # Open a new tab
        self.driver.execute_script(f"window.open('{self._restaurant.href}','_blank');")
        # Switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.switch_to.window(self.main_window_handle)

    async def get_offers(self) -> AsyncGenerator[RestaurantOffer, None]:
        if not self._restaurant.offers_available:
            return

        offer_elements = self.base_element.find_elements(by=By.XPATH, value="div/section[4]/section/section[2]/div[5]/div/div")

        for offer in offer_elements:
            # open modal
            if offer.is_displayed() and offer.is_enabled():
                try:
                    offer.click()
                except:
                    self.driver.execute_script("arguments[0].click();", offer)
                
                offer_modal = None
                try:
                    offer_modal = self.driver.find_element(by=By.XPATH, value="//div[contains(@class, 'modalWrapper') and @aria-hidden='false']/div[starts-with(@id, 'id-')]")
                    code = offer_modal.find_element(by=By.XPATH, value="section[2]/div[2]/div[4]/strong").text

                    offer_line1 = offer_modal.find_element(by=By.XPATH, value="section[2]/div[2]/div[2]").text
                    offer_line2 = offer_modal.find_element(by=By.XPATH, value="section[2]/div[2]/div[3]").text

                    # print(offer_line1, ' - ', offer_line2, ' - ', code.text)
                    
                    yield RestaurantOffer(code, offer_line1, offer_line2)
                except Exception as e:
                    logger.error('Failed to scrape offer details for restaurant: %s', self._restaurant.name, exc_info=True)
                finally:
                    if offer_modal:
                        # close modal
                        offer_modal.find_element(by=By.XPATH, value="section[1]/i").click()
    
    async def _find_items_by_category(self, category: str, name_contains: str = '') -> list[RestaurantItem]:
        begin = time.time()
        implicit_wait = self.driver.timeouts.implicit_wait
        # Set implicit wait to 0 seconds
        self.driver.implicitly_wait(0)
        try:
            section = self.base_element.find_element(by=By.XPATH, value="div/section[4]/section/section[2]/section[h4=\"" + category + "\"]")
            return [
                RestaurantItem(
                    item.find_element(by=By.XPATH, value="div[2]/div[1]/div/h4").text,
                    item.find_elements(by=By.XPATH, value="div[2]/div[1]/div/div[./span[contains(text(), 'vote')]]/div/i/*[name()='svg']/*[name()='title' and text()='star-fill']").__len__().__float__(),
                    item.find_element(by=By.XPATH, value="div[2]/div[1]/div/div/span[contains(text(), '₹')]").text
                )
                for item in section.find_elements(by=By.XPATH, value=f"div[2]/div/div/div[contains(translate(., '{name_contains.upper()}', '{name_contains.lower()}'), '{name_contains.lower()}')]")
            ]
        finally:
            # Set implicit wait back to its original value
            self.driver.implicitly_wait(implicit_wait)
            end = time.time()
            logger.debug(f'Scraped item category: {category} in {end - begin} seconds')
    
    async def get_all_items(self, containing: str) -> AsyncGenerator[RestaurantItemCategory, None]:
        categories = self.base_element.find_elements(by=By.XPATH, value="div/section[4]/section/section[2]/section/h4")
        tasks_map: dict[str, asyncio.Task[list[RestaurantItem]]] = {}

        for category in categories:
            if not containing or containing.lower() in category.text.lower():
                tasks_map[category.text] = asyncio.create_task(self._find_items_by_category(category.text))
            else:
                tasks_map[category.text] = asyncio.create_task(self._find_items_by_category(category.text, containing))

        for category, items_task in tasks_map.items():
            items = await items_task
            yield RestaurantItemCategory(category, items)
    
    def close(self):
        self.driver.close()