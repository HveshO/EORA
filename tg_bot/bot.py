import os
import logging
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from core.search import SearchEngine
from core.llm_engine import answer_with_context

load_dotenv()
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

logging.basicConfig(level=logging.INFO)
se = SearchEngine()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Отправьте свой вопрос по проектам EORA!")


async def handle_q(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.message.text
    docs = se.search(q)
    answer = answer_with_context(q, docs)
    answer += "\n\nМатериалы:"
    for idx, d in enumerate(docs, 1):
        answer += f"\n[{idx}] {d['title']}: {d['url']}"
    await update.message.reply_text(answer)


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_q))
    application.run_polling()


if __name__ == "__main__":
    main()
