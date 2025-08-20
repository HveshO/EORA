# src/bot/handlers.py
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from telegram import ReplyKeyboardRemove

from utils.logger import logger
from rag.generator import generate_answer
from bot.keyboards import main_kb
from bot.constants import (
    START_ANSWER,
    HELP_ANSWER,
    EMPTY_INPUT_ANSWER,
    ERROR_ANSWER,
)

router = Router()


@router.message(CommandStart())
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    logger.info("[start_cmd] User ID=%s", user_id)
    await message.answer(START_ANSWER, reply_markup=main_kb)


@router.message(Command("help"))
async def help_cmd(message: types.Message):
    user_id = message.from_user.id
    logger.info("[help_cmd] User ID=%s", user_id)
    await message.answer(HELP_ANSWER, reply_markup=main_kb)


@router.message()
async def handle_message(message: types.Message):
    user_id = str(message.from_user.id)
    text = (message.text or "").strip()

    logger.info("[handle_message] Incoming message from User ID=%s", user_id)

    if not text:
        logger.debug("[handle_message] Empty text from User ID=%s", user_id)
        return await message.answer(EMPTY_INPUT_ANSWER)

    try:
        answer_html = await generate_answer(user_id, text)
        logger.debug(
            "[handle_message] Generated answer length=%s for User ID=%s",
            len(answer_html),
            user_id,
        )
    except Exception as e:
        logger.error(
            "[handle_message] generate_answer failed for User ID=%s: %s",
            user_id,
            e,
            exc_info=False,
        )
        return await message.answer(ERROR_ANSWER)

    logger.debug("[handle_message] Sending answer to User ID=%s", user_id)
    await message.answer(
        answer_html,
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=ReplyKeyboardRemove(),
    )
