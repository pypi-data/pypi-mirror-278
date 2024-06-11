import logging
import os


def init():
    '''Инициализация логера'''
    logger = logging.getLogger('dars')
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    # --- @see https://stackoverflow.com/a/44049484
    if logger.hasHandlers():
        logger.handlers.clear()
    # ---
    logger.addHandler(handler)
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
