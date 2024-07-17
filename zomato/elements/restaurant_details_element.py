import asyncio
import time
from typing import AsyncGenerator
from playwright.async_api import Page

from zomato.elements.base_element import BaseElement
from zomato.models.restaurant import Restaurant, RestaurantItem, RestaurantItemCategory, RestaurantOffer
from zomato.logger import getLogger

logger = getLogger(__name__)

class RestaurantDetailsElement(BaseElement):
    def __init__(self, page: Page, restaurant: Restaurant):
        super().__init__(page, "//div[@id='root']/div/main")
        self._restaurant = restaurant

    async def get_offers(self) -> AsyncGenerator[RestaurantOffer, None]:
        if not self._restaurant.offers_available:
            return

        offer_elements = await self.base_element.locator("//div/section[4]/section/section[2]/div[5]/div/div", has_text="OFF").all()

        for offer in offer_elements:
            # open modal
            if (await offer.is_visible()) and (await offer.is_enabled()):
                await offer.click()
                
                offer_modal = None
                try:
                    offer_modal = self.page.locator("//div[contains(@class, 'modalWrapper') and @aria-hidden='false']/div[starts-with(@id, 'id-')]")
                    if offer_modal:
                        code_locator = offer_modal.locator("//section[2]/div[2]/div[4]/strong")
                        code = ""
                        if await code_locator.is_visible():
                            code = await code_locator.text_content() or ""

                        if await offer_modal.locator("//section[2]/div[2]/div[1]/img").is_visible():
                            offer_line1 = await offer_modal.locator("//section[2]/div[2]/div[2]").text_content() or ""
                            offer_line2 = await offer_modal.locator("//section[2]/div[2]/div[3]").text_content() or ""
                        else:
                            offer_line1 = await offer_modal.locator("//section[2]/div[2]/div[1]").text_content() or ""
                            offer_line2 = await offer_modal.locator("//section[2]/div[2]/div[2]").text_content() or ""

                        yield RestaurantOffer(code, offer_line1, offer_line2)
                except Exception as e:
                    logger.error('Failed to scrape offer details for restaurant: %s', self._restaurant.name, exc_info=True)
                finally:
                    if offer_modal:
                        # close modal
                        await offer_modal.locator("//section[1]/i").first.click() # type: ignore
    
    async def _find_items_by_category(self, category: str, name_contains: str = '') -> list[RestaurantItem]:
        begin = time.time()
        try:
            section = self.base_element.locator("//div/section[4]/section/section[2]/section[h4=\"" + category + "\"]")

            try:
                items_locator = section.locator(f"//div[2]/div/div/div[./div[2]/div[1]/div/h4 and contains(translate(., '{name_contains.upper()}', '{name_contains.lower()}'), '{name_contains.lower()}')]")
                if await items_locator.count() > 0:
                    await items_locator.last.scroll_into_view_if_needed()
                    await items_locator.last.wait_for(state="visible", timeout=1000)
            except:
                # this is just a workaround to load all the item images
                pass
            
            return [
                RestaurantItem(
                    await item.locator("//div[2]/div[1]/div/h4").text_content() or "",
                    len(await item.locator("//div[2]/div[1]/div/div[./span[contains(text(), 'vote')]]/div/i/*[name()='svg']/*[name()='title' and text()='star-fill']").all()),
                    await item.locator("//div[2]/div[1]/div/div/span[contains(text(), '₹')]").first.text_content() or "",
                    await item.locator("//div[1]/div[1]/img").get_attribute("src") if await item.locator("//div[1]/div[1]/img").count() > 0 else None,
                )
                for item in await items_locator.all()
            ]
        finally:
            end = time.time()
            logger.debug(f'Scraped item category: {category} in {end - begin} seconds')
    
    async def get_all_items(self, containing: str) -> AsyncGenerator[RestaurantItemCategory, None]:
        categories = await self.base_element.locator("//div/section[4]/section/section[2]/section/h4").all()
        tasks_map: dict[str, asyncio.Task[list[RestaurantItem]]] = {}

        for category in categories:
            category_name = await category.text_content() or ""
            if not containing or containing.lower() in category_name.lower():
                tasks_map[category_name] = asyncio.create_task(self._find_items_by_category(category_name))
            else:
                tasks_map[category_name] = asyncio.create_task(self._find_items_by_category(category_name, containing))

        for category, items_task in tasks_map.items():
            items = await items_task
            yield RestaurantItemCategory(category, items)
