import logging

Logger = logging.getLogger()
Logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
Logger.addHandler(console_handler)
