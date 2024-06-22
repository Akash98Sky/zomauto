from typing import AsyncGenerator
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from contextlib import suppress
from selenium.common.exceptions import NoSuchElementException

from zomato.elements.base_element import BaseElement
from zomato.models.restaurant import Restaurant

class RestaurantsElement(BaseElement):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, "//div[@id='root']/div")
    
    async def browse_restaurants(self, load_atleast: int = 50) -> AsyncGenerator[Restaurant, None]:
        restaurants = self.base_element.find_elements(by=By.XPATH, value="//div[@class='jumbo-tracker']/div")

        while (restaurants.__len__() < load_atleast):
            action = ActionChains(self.driver).scroll_to_element(restaurants[-1]).scroll_by_amount(0, 50).pause(1)
            action.perform()
            restaurants = self.base_element.find_elements(by=By.XPATH, value="//div[@class='jumbo-tracker']/div")

        for index, restaurant in enumerate(restaurants):
            offer_available = False
            with suppress(NoSuchElementException):
                discount_text = self.driver.execute_script(f"""
                return document
                    .querySelector('div[id="root"] > div')
                    .querySelectorAll('div[class="jumbo-tracker"] > div')[{index}]
                    .querySelector('a:nth-of-type(1) > div:nth-of-type(3) > p')?.innerText;
                """)
                if discount_text and "OFF" in discount_text:
                    offer_available = True
            
            yield Restaurant(
                restaurant.find_element(by=By.XPATH, value="a[2]/div[1]/h4").text,
                restaurant.find_element(by=By.XPATH, value="a[2]/div[2]/p[1]").text,
                restaurant.find_element(by=By.XPATH, value="a[1]/div[2]/img[@alt='Restaurant Card']").get_attribute("src"),
                restaurant.find_element(by=By.XPATH, value="a[2]/div[1]/div/div/div/div/div/div[1]").text,
                restaurant.find_element(by=By.XPATH, value="a[1]").get_attribute("href"),
                offer_available
            )