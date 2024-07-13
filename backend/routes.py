import logging
from fastapi import Depends, FastAPI, HTTPException
from selenium.webdriver.remote.webdriver import WebDriver

from zomato.zomato import Zomato
from .browser import instance as browser

api_routes = FastAPI()


@api_routes.get("/locations")
def read_locations(q: str, browser: WebDriver = Depends(browser)):
    try:
        z = Zomato(browser)
        return z.search_locations(q)
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=400)