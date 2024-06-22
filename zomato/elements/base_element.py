from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class BaseElement:
    def __init__(self, driver: WebDriver, xpath: str | None = None) -> None:
        self._driver = driver
        self._xpath = xpath

    @property
    def driver(self):
        return self._driver
    
    @property
    def base_element(self):
        return self.driver.find_element(By.XPATH, self._xpath)