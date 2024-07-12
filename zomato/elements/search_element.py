from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from zomato.elements.base_element import BaseElement
from zomato.models.item import Item
from zomato.models.location import Location

class SearchElement(BaseElement):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, "//div[@id='root']//ul[starts-with(@id, 'navigation')]/li[1]/div/div")

    def locations(self, query: str):
        locSearchElement = self.base_element.find_element(by=By.XPATH, value="div[1]")
        
        locSearchElement.find_element(by=By.TAG_NAME, value="input").clear()
        locSearchElement.find_element(by=By.TAG_NAME, value="input").send_keys(query)

        # wait for drop down element to be present
        dropElement = locSearchElement.find_element(by=By.XPATH, value="div/div/p[2]")

        if (not dropElement.is_displayed()):
            locSearchElement.find_element(by=By.XPATH, value="i[2]").click()
            locSearchElement.find_element(by=By.XPATH, value="div/div/p[2]")

        return [Location(
                    loc.find_elements(by=By.TAG_NAME, value="p")[0].text,
                    loc.find_elements(by=By.TAG_NAME, value="p")[1].text
                ) for loc in locSearchElement.find_elements(by=By.XPATH, value="div/div")]
    
    def update_location(self, query: str, location: Location):
        locSearchElement = self.base_element.find_element(by=By.XPATH, value="div[1]")

        if (locSearchElement.find_element(by=By.TAG_NAME, value="input").get_attribute("value") != query):
            locSearchElement.find_element(by=By.TAG_NAME, value="input").clear()
            locSearchElement.find_element(by=By.TAG_NAME, value="input").send_keys(query)
        
        # wait for drop down element to be present
        dropElement = locSearchElement.find_element(by=By.XPATH, value="div/div/p[2]")

        if (not dropElement.is_displayed()):
            locSearchElement.find_element(by=By.XPATH, value="i[2]").click()
            locSearchElement.find_element(by=By.XPATH, value="div/div/p[2]")

        for loc in locSearchElement.find_elements(by=By.XPATH, value="div/div"):
            if loc.find_element(by=By.XPATH, value="p[1]").text == location.line1 and loc.find_element(by=By.XPATH, value="p[2]").text == location.line2:
                loc.click()
                break

    def items(self, query: str):
        itemSearchElement = self.base_element.find_element(by=By.XPATH, value="div[3]")

        if (itemSearchElement.find_element(by=By.TAG_NAME, value="input").get_attribute("value") != query):
            itemSearchElement.find_element(by=By.TAG_NAME, value="input").send_keys(query)
            itemSearchElement.find_element(by=By.TAG_NAME, value="input").click()

        # wait for drop down element to be present
        itemSearchElement.find_element(by=By.XPATH, value="div/div/div[1]/img")
        itemSearchElement.find_element(by=By.XPATH, value="div/div/div[2]/p[1]")

        return [Item(
                    item.find_element(by=By.XPATH, value="div[2]/p[1]").text,
                    item.find_element(by=By.XPATH, value="div[2]/p[2]").text,
                    item.find_element(by=By.XPATH, value="div[1]/img").get_attribute("src")
                ) for item in itemSearchElement.find_elements(by=By.XPATH, value="div/div") if item.find_element(by=By.XPATH, value="div[1]/div").get_attribute("alt") == 'Dish']
    
    def find_item(self, query: str, item: Item):
        itemSearchElement = self.base_element.find_element(by=By.XPATH, value="div[3]")

        if (itemSearchElement.find_element(by=By.TAG_NAME, value="input").get_attribute("value") != query):
            itemSearchElement.find_element(by=By.TAG_NAME, value="input").clear()
            itemSearchElement.find_element(by=By.TAG_NAME, value="input").send_keys(query)
            itemSearchElement.find_element(by=By.TAG_NAME, value="input").click()

        # wait for drop down element to be present
        itemSearchElement.find_element(by=By.XPATH, value="div/div/div[1]/img")
        itemSearchElement.find_element(by=By.XPATH, value="div/div/div[2]/p[1]")

        for itemElement in itemSearchElement.find_elements(by=By.XPATH, value="div/div"):
            if itemElement.find_element(by=By.XPATH, value="div[2]/p[1]").text == item.name and itemElement.find_element(by=By.XPATH, value="div[2]/p[2]").text == item.type:
                itemElement.click()
                break