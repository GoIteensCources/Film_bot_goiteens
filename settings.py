import os

from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("BOT_TOKEN")
DATABASE = "./data.json"
PAGE_SIZE = 3

