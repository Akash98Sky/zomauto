import asyncio
from playwright.async_api import Page

from zomato.elements.base_element import BaseElement
from zomato.models.item import Item
from zomato.models.location import Location

class NavbarElement(BaseElement):
    def __init__(self, page: Page) -> None:
        super().__init__(page, "//nav/ul[starts-with(@id, 'navigation_')]")

    async def locations(self, query: str):
        locSearchElement = self.base_element.locator("//li[1]/div/div/div").nth(0).first

        # wait for drop down element to be present
        gpsElement = locSearchElement.locator("//div/div[1]/div/p[@text='Detect current location']")

        if (not await gpsElement.is_visible()):
            await locSearchElement.locator("i").nth(1).click()
        
        await locSearchElement.locator("input").clear()
        await locSearchElement.locator("input").fill(query)

        await asyncio.sleep(1)
        # wait for location search to complete
        await locSearchElement.locator("//div/div[1]/div/p[@text='Detect current location']").wait_for(state="hidden", timeout=5000)

        return [Location(
                    await loc.locator("p").nth(0).text_content() or "",
                    await loc.locator("p").nth(1).text_content() or "",
                    query
                ) for loc in await locSearchElement.locator("div div").all()]
    
    async def update_location(self, query: str, location: Location):
        locSearchElement = self.base_element.locator("//li[1]/div/div/div").nth(0).first

        # wait for drop down element to be present
        dropDownElement = locSearchElement.locator("//div/div[1]/p").first

        if (not await dropDownElement.is_visible()):
            await locSearchElement.locator("i").nth(1).click()

        if (await locSearchElement.locator("input").input_value() != query):
            await locSearchElement.locator("input").fill(query)

        await asyncio.sleep(1)
        # wait for location search to complete
        await locSearchElement.locator("//div/div[1]/div/p[@text='Detect current location']").wait_for(state="hidden", timeout=5000)

        for loc in await locSearchElement.locator("div div").all():
            if (await loc.locator("p").nth(0).text_content() == location.line1 and await loc.locator("p").nth(1).text_content() == location.line2):
                await loc.click()
                break

    async def items(self, query: str):
        itemSearchElement = self.base_element.locator("//li[1]/div/div/div[./input[@placeholder='Search for restaurant, cuisine or a dish']]").first

        if (await itemSearchElement.locator("input").input_value() != query):
            await itemSearchElement.locator("input").fill(query)
            await itemSearchElement.locator("input").click()

        # wait for drop down element to be present
        await itemSearchElement.locator("//div/div/div[1]/img").first.wait_for()

        return [Item(
                    await item.locator("//div[2]/p[1]").text_content() or "",
                    await item.locator("//div[2]/p[2]").text_content() or "",
                    await item.locator("//div[1]/img").get_attribute("src"),
                    query
                ) for item in await itemSearchElement.locator("//div[2]/div[./div/img[@alt='Dish']]").all() if await item.locator("//div[1]/img").get_attribute("alt") == 'Dish']
    
    async def find_item(self, query: str, item: Item):
        itemSearchElement = self.base_element.locator("//li[1]/div/div/div[./input[@placeholder='Search for restaurant, cuisine or a dish']]").first

        if (await itemSearchElement.locator("input").input_value() != query):
            await itemSearchElement.locator("input").fill(query)
            await itemSearchElement.locator("input").click()

        # wait for drop down element to be present
        await itemSearchElement.locator("//div/div/div[1]/img").first.wait_for()

        for itemElement in await itemSearchElement.locator("//div[2]/div[./div/img[@alt='Dish']]").all():
            if (await itemElement.locator("//div[2]/p[1]").text_content() == item.name) and (await itemElement.locator("//div[2]/p[2]").text_content() == item.type):
                await itemElement.click()
                break

    async def login(self, ph_no: str):
        await self.base_element.locator("li[4]/a").click()

        frame_name = await self.page.locator("auth-login-ui").get_attribute("name")
        frame = self.page.frame(frame_name)
        
        if frame:
            login_section = frame.locator("//div[@aria-hidden='false' and @role='dialog']/div[starts-with(@id, 'id-') and @type='default']/section[2]/section")

            await login_section.locator("//input[@type='number']").fill(ph_no)
            await login_section.locator("//button[@role='button']").click()

            loginName = ''
            while (loginName == None or loginName == ''):
                try:
                    loginName = await self.base_element.locator("li[4]/div/div/div[1]/span").text_content()
                except:
                    pass

            return loginName

    async def logout(self):
        logoutElement = self.base_element.locator("li[4]/div/div/div[2]/div[8]")

        if (not logoutElement.is_disabled()):
            await self.base_element.locator("li[4]/div/div/div[1]/i").click()

        await logoutElement.click()
