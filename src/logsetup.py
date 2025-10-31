import logging
from logging.handlers import RotatingFileHandler
from constants import LOG_DIR, LOG_PATH, LOG_MAX_SIZE, LOG_BACKUP_COUNT, LOG_DATE_FORMAT

def setup_logging():
    '''Настраивает логирование'''
    logger = logging.getLogger('shell')
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(LOG_PATH, LOG_MAX_SIZE, LOG_BACKUP_COUNT, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt='[%(asctime)s] %(levelname)s %(message)s', datefmt=LOG_DATE_FORMAT)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False
    return logger