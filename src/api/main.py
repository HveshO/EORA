from fastapi import FastAPI
from pydantic import BaseModel
from src.core.search import SearchEngine
from src.core.llm_engine import generate_answer

# поднимает HTTP сервер (FastAPI), получает вопросы, отвечает с подложкой (ссылки в ответе)
app = FastAPI()
search_engine = SearchEngine()


class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(req: QuestionRequest):
    docs = search_engine.search(req.question)
    answer = generate_answer(req.question, docs)
    sources = [{"title": d["title"], "url": d["url"]} for d in docs]
    return {"answer": answer, "sources": sources}
