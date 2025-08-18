# здесь получаем параметры
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DATA_PATH = os.getenv("DATA_PATH", "data/data.json")
URLS_FILEPATH = os.getenv("URLS_FILEPATH", "data/urls.txt")
