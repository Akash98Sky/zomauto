import logging

zomauto_logger = logging.getLogger('zomauto.backend')

def getLogger(name: str):
    child = zomauto_logger.getChild(name)
    child.setLevel(zomauto_logger.level)
    return child
