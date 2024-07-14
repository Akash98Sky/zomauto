import asyncio
from os import getenv

from backend.logger import getLogger
from zomato.zomato import Zomato

HEADLESS = False
DEVTOOLS = False
env = getenv("ENV")
logger = getLogger(__name__)

zomauto: Zomato

def config(headless: bool):
    global HEADLESS
    global DEVTOOLS
    HEADLESS = headless
    DEVTOOLS = env != "production"

def instance():
    global zomauto
    return zomauto

async def startup():
    global zomauto
    zomauto = await Zomato(headless=HEADLESS, devtools=DEVTOOLS).__aenter__()

async def shutdown():
    global zomauto
    await zomauto.__aexit__(None, None, None)
