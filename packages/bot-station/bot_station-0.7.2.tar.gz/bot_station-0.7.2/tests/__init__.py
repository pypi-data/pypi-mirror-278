import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)06f %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%d-%m-%Y:%H:%M:%S",
    level=logging.DEBUG,
)
