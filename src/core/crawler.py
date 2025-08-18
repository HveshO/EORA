# скачивает и парсит страницы по списку ссылок, сохраняет тексты в JSON


import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from core.config import URLS_FILEPATH
from utils.helpers import load_urls

URLS = [
    "https://eora.ru/cases/promyshlennaya-bezopasnost",
    "https://eora.ru/cases/lamoda-systema-segmentacii-i-poiska-po-pohozhey-odezhde",
    "https://eora.ru/cases/navyki-dlya-golosovyh-assistentov/karas-golosovoy-assistent",
    # ... остальные ссылки из списка
]


def fetch_page(url: str) -> Dict[str, str]:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator=" ", strip=True)
        title = soup.title.string if soup.title else url
        return {"url": url, "title": title, "content": text[:8000]}
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")
        return {}


def crawl_all(urls: List[str]) -> List[Dict[str, str]]:
    docs = []
    for url in urls:
        doc = fetch_page(url)
        if doc:
            docs.append(doc)
    return docs


def save_docs(docs: List[Dict[str, str]], filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)


def main():
    urls = load_urls(URLS_FILEPATH)
    docs = crawl_all(urls)
    save_docs(docs, "data/docs.json")


if __name__ == "__main__":
    main()
