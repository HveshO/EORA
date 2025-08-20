from pathlib import Path
import logging
from config import settings, embeddings
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)


def retrieve(
    question: str,
    top_k: int = settings.TOP_K,
    index_path: Path = settings.PATH_STORAGE_INDEX,
) -> list[dict]:
    """
    Searches relevant documents in a local FAISS index.

    :param question: search query
    :param top_k: number of top results
    :param index_path: path to the saved index
    :return: list of Document objects
    """
    try:
        logger.info("Searching for query: %s (top_k=%s)", question, top_k)
        if not Path(index_path).exists():
            logger.error("Index not found: %s", index_path)
            return []
        vectorstore = FAISS.load_local(
            index_path, embeddings, allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        results = retriever.get_relevant_documents(question)

        logger.info("Number of documents found: %s", len(results))
        return results

    except Exception as e:
        logger.exception("Error while searching the index: %s", e)
        raise
