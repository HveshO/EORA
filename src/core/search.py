import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict

#  индексирует тексты, на входе — вопрос, выдаёт 2-3 наиболее релевантных документа


class SearchEngine:
    def __init__(self, docs_path: str = "data/docs.json"):
        with open(docs_path, encoding="utf-8") as f:
            self.docs = json.load(f)
        self.contents = [doc["content"] for doc in self.docs]
        self.vectorizer = TfidfVectorizer(stop_words="russian")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.contents)

    def search(self, query: str, top_n: int = 3) -> List[Dict]:
        q_vec = self.vectorizer.transform([query])
        scores = np.dot(self.tfidf_matrix, q_vec.T).toarray().ravel()
        best_indices = np.argsort(scores)[::-1][:top_n]
        return [self.docs[i] for i in best_indices]
