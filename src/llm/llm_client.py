import os
from typing import Optional

from torch import float16
from config import settings
from llm.prompts import ANSWER_PROMPT, SYSTEM_PROMPT
from utils.logger import logger
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM, pipeline
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

model_name = "mistralai/Mistral-7B-Instruct-v0.2"
# Загружаем конфиг и токенизатор
config = AutoConfig.from_pretrained(model_name, use_auth_token=settings.API_KEY)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=settings.API_KEY)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    offload_folder="offload",
    token=settings.API_KEY,
    torch_dtype=float16,
)


# Создаём pipeline
chat_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=False,
    max_new_tokens=settings.ANSWER_MAX_TOKENS,
    temperature=settings.ANSWER_TEMPERATURE,
)


def chat_complete(
    question: str,
    context: str,
    max_tokens: Optional[int] = settings.ANSWER_MAX_TOKENS,
    temperature: Optional[float] = settings.ANSWER_TEMPERATURE,
) -> str:
    """
    Выполняет генерацию ответа через локальный pipeline transformers.
    """
    logger.debug("Generate answer locally with Mistral-7B")

    prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + ANSWER_PROMPT.format(question=question, context=context)
    )

    outputs = chat_pipeline(
        prompt,
        max_new_tokens=max_tokens,
        temperature=temperature,
    )
    answer = outputs[0]["generated_text"].strip()

    return answer


# {"role": "system", "content": SYSTEM_PROMPT},
#     question: str,
#     context: str,
#     model: Optional[str] = settings.OPENAI_MODEL,
#     max_tokens: Optional[int] = settings.ANSWER_MAX_TOKENS,
#     temperature: Optional[float] = settings.ANSWER_TEMPERATURE,
# ) -> str:
#     """
#     Выполняет синхронную (или асинхронную, если библиотека поддерживает) ChatCompletion.
#     Возвращает текст ответа или вызывает исключение.
#     """
#     logger.debug("Send request to OpenAI %s", model)

#     resp = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {
#                 "role": "user",
#                 "content": ANSWER_PROMPT.format(question=question, context=context),
#             },
#         ],
#         max_tokens=max_tokens,
#         temperature=temperature,
#     )
#     return resp.choices[0].message.content.strip()
