
import logging

def set_logging(name):
    """
    Set basic logging config and name a logger
    """
    logging.basicConfig(filename="test.log",level=logging.DEBUG,
        filemode="w",format='[%(asctime)s:%(funcName)s:%(name)s:%(levelname)s] %(message)s'
        )

    logger = logging.getLogger(name)
    return logger

logger = set_logging('test')

if __name__ == "__main__":
    logger.info("Let\'s do something!")
    logger.warning("This is a Warning!")
    logger.error("Something goes wrong...")
