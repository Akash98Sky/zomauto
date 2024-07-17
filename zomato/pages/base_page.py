import asyncio
from typing import Awaitable
from playwright.async_api import Browser, BrowserContext

class BasePage:
    def __init__(self, browser: Browser | BrowserContext, page_url: str = "https://www.zomato.com/bangalore") -> None:
        self._browser = browser
        self._page_url = page_url

    async def __aenter__(self):
        self._page = await self._browser.new_page()
        await self._page.goto(self._page_url)
        return self
    
    async def __aexit__(self, exc_type, exc, traceback):
        await self._page.close()

    @property
    def page(self):
        if self._page.url != self._page_url:
            asyncio.create_task(self.__reload())
        return self._page
    
    async def __reload(self):
        if self._page.url != self._page_url:
            await self._page.goto(self._page_url)
        else:
            await self._page.reload()
