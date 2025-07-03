import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re
import aiohttp

TOKEN = "ТУТ_ТВОЙ_ТОКЕН"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені нікнейм або номер телефону 🔍")

def is_phone_number(text: str) -> bool:
    return re.match(r"^\+?[0-9]{7,15}$", text)

async def search_by_username(username: str) -> str:
    async with aiohttp.ClientSession() as session:
        url = f"https://www.namecheckr.com/namecheckr/?username={username}"
        async with session.get(url) as resp:
            if resp.status == 200:
                return f"✅ Можливо, такий нік існує. (Деталі в розробці)"
            else:
                return "⚠️ Не вдалося знайти інформацію."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    if is_phone_number(query):
        await update.message.reply_text(f"🔢 Виявлено номер: {query}\n(Пошук по телефону — в розробці)")
    else:
        await update.message.reply_text(f"🔍 Шукаю профілі з нікнеймом: {query}")
        result = await search_by_username(query)
        await update.message.reply_text(result)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
