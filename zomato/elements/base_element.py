from playwright.async_api import Page, Browser

class BaseElement:
    def __init__(self, page: Page, xpath: str | None = None) -> None:
        self._page = page
        self._xpath = xpath

    @property
    def page(self):
        return self._page
    
    @property
    def base_element(self):
        return self.page.locator(self._xpath or '').first