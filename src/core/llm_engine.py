import os
import openai
from dotenv import load_dotenv

# формирует prompt с вопросом и выдержками, вызывает LLM API (OpenAI/GigaChat)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
Используйте следующие материалы для ответа. Вставляйте ссылки как [[1]], [[9]] к соответствующим документам.

Вопрос: {question}

Материалы:
{context}

Ответ:
"""


def build_context(docs):
    parts = []
    for idx, doc in enumerate(docs, 1):
        snippet = doc["content"][:700].replace("\n", " ")
        parts.append(f"[[{idx}]] {doc['title']} ({doc['url']}): {snippet}...")
    return "\n".join(parts)


def generate_answer(question, docs):
    context = build_context(docs)
    prompt = PROMPT_TEMPLATE.format(question=question, context=context)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content
