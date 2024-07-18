from zomato.logger import getLogger

zomauto_logger = getLogger('backend')

def getLogger(name: str):
    child = zomauto_logger.getChild(name)
    child.setLevel(zomauto_logger.level)
    return child
