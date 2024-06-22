import logging

logging.basicConfig(level=logging.INFO)
zomauto_logger = logging.getLogger('zomauto')
selenium_logger = logging.getLogger('selenium')

def getLogger(name: str):
    child = zomauto_logger.getChild(name)
    child.setLevel(zomauto_logger.level)
    return child

def setLogLevel(level: int | str) -> None:
    zomauto_logger.setLevel(level)

def setWebDriverLogLevel(level: int | str) -> None:
    selenium_logger.setLevel(level)