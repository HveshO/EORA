from src.core.search import SearchEngine
from src.core.llm_engine import generate_answer


def main():
    search_engine = SearchEngine()
    print("Введите вопрос. Для выхода - Ctrl+C.")
    while True:
        question = input("\nВопрос: ")
        docs = search_engine.search(question)
        answer = generate_answer(question, docs)
        print("\nОтвет:\n", answer)
        print("\nИсточники:")
        for idx, doc in enumerate(docs, 1):
            print(f"[{idx}] {doc['title']}: {doc['url']}")


if __name__ == "__main__":
    main()
