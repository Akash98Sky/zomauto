import logging
from typing import Any
import json
import asyncio

from zomato.models.restaurant import RestaurantItem, RestaurantOffer
from zomato.zomato import Zomato
from zomato.logger import setLogLevel, setWebDriverLogLevel

# set logging level of zomato module only
setLogLevel(logging.DEBUG)
setWebDriverLogLevel(logging.WARNING)

HEADLESS = True
config: dict[str, Any] = {}

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)
    
def discounted_price(item: RestaurantItem, offer: RestaurantOffer) -> float:
    discount = min(item.price * offer.discount_percent / 100, offer.max_discount_amount)
    return item.price - discount if item.price >= offer.min_order_value else item.price

async def automate(args: list[str]) -> None:
    # browser = await playwright.chromium.launch(executable_path="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe", headless=HEADLESS)
    async with Zomato(headless=HEADLESS, browser_args=args) as z:
        location_matchers = config["location"]["match"]
        item_matchers = config["item"]["match"]
        
        locations = await z.search_locations(config["location"]["search"])
        items = await z.search_items(config["item"]["search"])

        location = next((loc for loc in locations if all([matcher["field"] in loc.__dict__ and str(matcher["value"]).lower() in str(loc.__dict__[matcher["field"]]).lower() for matcher in location_matchers])), None)
        if not location:
            raise Exception("No location found")
        item = next((item for item in items if all([matcher["field"] in item.__dict__ and str(matcher["value"]).lower() in str(item.__dict__[matcher["field"]]).lower() for matcher in item_matchers])), None)
        if not item:
            raise Exception("No item found")
        
        json_data: list[dict[str, Any]] = []
        async for r in z.browse_restaurants(at=location, serving=item, at_least=0):
            if not r.offers_available:
                continue
            r, offers, item_categories = await z.get_restaurant_details(r, config["item"]["search"])
            for category in item_categories:
                for item in category.items:
                    for offer in offers:
                        item.discounted_price = min(item.discounted_price, discounted_price(item, offer))

            json_data.append({
                "restaurant": r.to_dict(),
                "offers": [o.to_dict() for o in offers],
                "items": [category.to_dict() for category in item_categories]
            })
        with open("restaurants.json", "w") as f:
            json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    config = load_config()
    browser_args = [
        "--guest",
    ]

    if HEADLESS:
        browser_args.append("--headless")
        browser_args.append(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    
    asyncio.run(automate(browser_args))