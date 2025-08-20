from pathlib import Path

from bs4 import BeautifulSoup
from config import settings, embeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.logger import logger

import requests
from langchain.schema import Document


def load_url_content(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; EORA Bot/1.0)"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    return Document(page_content=text, metadata={"source": url})


def load_documents(urls):
    docs = []
    for url in urls:
        try:
            doc = load_url_content(url)
            docs.append(doc)
        except Exception as e:
            logger.warning(f"Failed to load {url}: {e}")
    return docs


def build_faiss_index(
    urls_path: Path = settings.PATH_FILE_URLS,
    index_path: Path = settings.PATH_STORAGE_INDEX,
):
    try:
        with open(urls_path, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        logger.info("Start load urls %s", len(urls))
        docs = load_documents(urls)

        logger.info("Get docs %s", len(docs))
        if docs != 0:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=100
            )
            docs_split = splitter.split_documents(docs)
            logger.info("Get docs_split %s", len(docs_split))

            vectorstore = FAISS.from_documents(docs_split, embeddings)
            logger.info("Get vector store")
            vectorstore.save_local(index_path)
            logger.info(
                "[build_faiss_index] success save to %s", settings.PATH_STORAGE_INDEX
            )
    except Exception as e:
        logger.error("[build_faiss_index] failed: %s", e)
        raise
