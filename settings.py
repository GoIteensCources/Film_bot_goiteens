import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")
DATABASE = "./data.json"
PAGE_SIZE = 3

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="[%(asctime)s] %(levelname)s:%(filename)s(%(lineno)d) -- %(message)s",
)
