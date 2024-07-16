from os import getenv

from backend.logger import getLogger
from zomato.zomato import Zomato

HEADLESS = False
DEVTOOLS = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
BROWSER_ARGS: list[str] = []
env = getenv("ENV")
logger = getLogger(__name__)

zomauto: Zomato

def config():
    global HEADLESS
    global DEVTOOLS
    global BROWSER_ARGS
    BROWSER_ARGS.extend([
        '--guest',
        '--disable-extensions',
        '--disable-component-extensions-with-background-pages',
        '--no-first-run',
        '--ash-no-nudges'
    ])
    if env == "production":
        HEADLESS = True
        DEVTOOLS = False

        BROWSER_ARGS.append('--no-sandbox')
        BROWSER_ARGS.append('--disable-setuid-sandbox')
        BROWSER_ARGS.append('--disable-dev-shm-usage')
        BROWSER_ARGS.append('--disable-gl-drawing-for-tests')
        BROWSER_ARGS.append('--disable-accelerated-2d-canvas')

def instance():
    global zomauto
    return zomauto

async def startup():
    config()
    global zomauto
    zomauto = await Zomato(headless=HEADLESS, devtools=DEVTOOLS, user_agent=USER_AGENT, browser_args=BROWSER_ARGS).__aenter__()

async def shutdown():
    global zomauto
    await zomauto.__aexit__(None, None, None)
