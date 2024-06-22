import logging
from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Edge, EdgeOptions
import json
import asyncio

from zomato.zomato import Zomato
from zomato.logger import setLogLevel, setWebDriverLogLevel

# set logging level of zomato module only
setLogLevel(logging.DEBUG)
setWebDriverLogLevel(logging.WARNING)

HEADLESS = False
config: dict[str, Any] = {}

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

async def automate(browser: WebDriver):
    z = Zomato(browser)
    
    location_matchers = config["location"]["match"]
    item_matchers = config["item"]["match"]
    
    z.search_locations(config["location"]["search"], lambda loc: all([matcher["field"] in loc.__dict__ and str(matcher["value"]).lower() in str(loc.__dict__[matcher["field"]]).lower() for matcher in location_matchers]))
    z.search_items(config["item"]["search"], lambda item: all([matcher["field"] in item.__dict__ and str(matcher["value"]).lower() in str(item.__dict__[matcher["field"]]).lower() for matcher in item_matchers]))
    
    json_data: list[dict[str, Any]] = []
    async for r in z.browse_restaurants():
        r, offers, items = await z.get_restaurant_details(r)
        
        json_data.append({
            "restaurant": r.to_dict(),
            "offers": [o.to_dict() for o in offers],
            "items": [i.to_dict() for i in items]
        })
    with open("restaurants.json", "w") as f:
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    config = load_config()
    options = EdgeOptions()
    options.add_argument("--guest")

    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    browser = Edge(options)
    try:
        asyncio.run(automate(browser))
    finally:
        browser.close()
        browser.quit()