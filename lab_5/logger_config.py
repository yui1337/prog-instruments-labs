import os

import logging


def setup_logging() -> None:
    """
    Создаёт объект логгера
    :return: None
    """

    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    all_handler = logging.FileHandler('logs/all.log', encoding='utf-8')
    all_handler.setLevel(logging.DEBUG)

    info_handler = logging.FileHandler('logs/info.log', encoding='utf-8')
    info_handler.setLevel(logging.INFO)

    error_handler = logging.FileHandler('logs/error.log', encoding='utf-8')
    error_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    all_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.addHandler(all_handler)
    root.addHandler(info_handler)
    root.addHandler(error_handler)
