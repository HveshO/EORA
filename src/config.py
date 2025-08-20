from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    API_KEY: str
    DEBUG: bool = True
    BUILD_FAISS: bool = True
    TOP_K: Optional[int] = 8
    ANSWER_MAX_TOKENS: Optional[int] = 700
    ANSWER_TEMPERATURE: Optional[float] = 0.3
    PATH_FILE_URLS: Path = Path("../data/urls.txt").resolve()
    PATH_STORAGE_INDEX: Path = Path("../data/faiss_index").resolve()

    class Config:
        env_file = "../.env"


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

settings = Settings()
