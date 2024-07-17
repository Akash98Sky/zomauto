import asyncio
from typing import AsyncGenerator
from playwright.async_api import Page

from zomato.elements.base_element import BaseElement
from zomato.models.restaurant import Restaurant

class RestaurantsElement(BaseElement):
    def __init__(self, page: Page):
        super().__init__(page, "//div[@id='root']/div")
    
    async def browse_restaurants(self, load_atleast: int = 50) -> AsyncGenerator[Restaurant, None]:
        restaurants = await self.base_element.locator("//div[@class='jumbo-tracker']/div").all()

        while (len(restaurants) < load_atleast):
            await restaurants[-1].scroll_into_view_if_needed()
            await self.page.evaluate("() => window.scrollBy(0, 50)")
            # wait for a new restaurant to be loaded
            await self.base_element.locator("//div[contains(@class, 'jumbo-tracker')]").nth(len(restaurants)).wait_for()
            restaurants = await self.base_element.locator("//div[contains(@class, 'jumbo-tracker')]/div").all()

        for restaurant in restaurants:
            offer_available = False
            try:
                if await restaurant.locator("//a[1]/div[3]/p").is_visible():
                    discount_text = await restaurant.locator("//a[1]/div[3]/p").text_content()
                    if discount_text and "OFF" in discount_text:
                        offer_available = True
            except Exception:
                pass
            
            yield Restaurant(
                await restaurant.locator("//a[2]/div[1]/h4").text_content() or "",
                await restaurant.locator("//a[2]/div[2]/p[1]").text_content() or "",
                await restaurant.locator("//a[1]/div[2]/img").get_attribute("src"),
                await restaurant.locator("//a[2]/div[1]/div/div/div/div/div/div[1]").text_content() or "",
                await restaurant.locator("//a[1]").get_attribute("href") or "",
                offer_available
            )
