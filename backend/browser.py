from selenium.webdriver import Edge, EdgeOptions, EdgeService
import shutil
from os import getenv

from backend.logger import getLogger

HEADLESS = False
env = getenv("ENV")
browser: Edge

logger = getLogger(__name__)

def config(headless: bool):
    global HEADLESS
    HEADLESS = headless

def instance():
    global browser
    return browser

def startup():
    options = EdgeOptions()
    options.add_argument("--guest")
    options.add_argument("--disable-extensions"); # disabling extensions

    if env == "production":
        options.add_argument("--disable-gpu"); # applicable to windows os only
        options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
        options.add_argument("--no-sandbox"); # Bypass OS security model

    if HEADLESS:
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

    global browser
    driver_path = shutil.which("msedgedriver")
    if driver_path:
        logger.info(f"Using msedgedriver at {driver_path}")
        service = EdgeService(executable_path=driver_path, port=4444)
        browser = Edge(options, service)
    else:
        browser = Edge(options)

def shutdown():
    global browser
    if browser.service.is_connectable():
        browser.quit()
