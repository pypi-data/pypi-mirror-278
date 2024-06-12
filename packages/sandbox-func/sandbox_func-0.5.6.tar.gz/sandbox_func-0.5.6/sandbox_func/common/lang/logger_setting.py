import logging


def init():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d [%(levelname)s] %(name)s:%(filename)s:%(lineno)s - %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S',
    )
