from src.core.llm_engine import answer_with_context
from src.core.search import SearchEngine


def main():
    se = SearchEngine()
    while True:
        question = input("\nВопрос: ")
        docs = se.search(question)
        print("\nОтвет:")
        print(answer_with_context(question, docs))
        print("Материалы:")
        for idx, d in enumerate(docs, 1):
            print(f"[{idx}] {d['title']}: {d['url']}")


if __name__ == "__main__":
    main()
