import os
from dotenv import load_dotenv
from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from src.core.search import SearchEngine
from src.core.llm_engine import generate_answer

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

search_engine = SearchEngine()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь вопрос по проектам EORA.")


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    docs = search_engine.search(question)
    response = generate_answer(question, docs)
    message = response + "\n\nИсточники:\n"
    message += "\n".join(
        f"[{i+1}] {d['title']}: {d['url']}" for i, d in enumerate(docs)
    )
    await update.message.reply_text(message)


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    app.run_polling()


if __name__ == "__main__":
    main()
