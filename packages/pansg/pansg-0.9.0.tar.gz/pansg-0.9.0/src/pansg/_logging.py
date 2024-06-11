import logging
from logging import (CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET)


def set_logging_level(level='ERROR'):
    level = level.upper()
    dt_level = {
        k: v for k, v in zip(
            ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'],
            [CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET]
        )
    }
    logging.basicConfig(level=dt_level[level])

    logging.info(f'set logging level to {level}')


if __name__ == '__main__':
    set_logging_level('NOTSET')

    logging.debug('Python debug')
    logging.info('Python info')
    logging.warning('Python warning')
    logging.error('Python error')
    logging.critical('Python critical')
