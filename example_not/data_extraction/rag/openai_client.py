# Настройка клиента
from openai import AsyncOpenAI

from setup import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
