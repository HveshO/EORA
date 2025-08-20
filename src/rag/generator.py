from llm.llm_client import chat_complete
from utils.logger import logger
from config import settings
from rag.retriever import retrieve
from bot.constants import (
    EMPTY_INPUT_ANSWER,
    NO_CONTEXT_ANSWER,
    GENERATION_ERROR_ANSWER,
    RETRIEVE_ERROR_ANSWER,
)


class GeneratorError(Exception): ...


async def generate_answer(user_id: str, question: str) -> str:
    logger.info("[generate_answer] Start for user_id=%s", user_id)

    if not question or not question.strip():
        logger.warning("[generate_answer] Empty question for user_id=%s", user_id)
        raise ValueError(EMPTY_INPUT_ANSWER)

    try:
        docs = retrieve(question, top_k=settings.TOP_K)
        logger.debug("[generate_answer] Retrieved %s docs", len(docs))
    except Exception as e:
        logger.exception("[generate_answer] Retrieve failed: %s", e)
        raise GeneratorError(RETRIEVE_ERROR_ANSWER)

    if not docs:
        logger.info("[generate_answer] No context found")
        raise GeneratorError(NO_CONTEXT_ANSWER)

    try:
        context = "\n".join(
            f"[{i+1}] {doc.metadata.get('title', 'Без названия')} — "
            f"{doc.metadata.get('description', doc.page_content[:200])}"
            for i, doc in enumerate(docs)
        )

        answer = chat_complete(question, context)

        logger.debug("[generate_answer] Output length=%s", len(answer))
        return answer

    except Exception as e:
        logger.exception("[generate_answer] LLM call failed: %s", e)
        raise GeneratorError(GENERATION_ERROR_ANSWER)
