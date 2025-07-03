import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re
import requests

TOKEN = "8174885258:AAF5HEkQQq7FkzQKmWFFIDUcwrGfe0bLT5w"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені нікнейм або номер телефону, і я спробую знайти максимум інформації 🔍")

def is_phone_number(text):
    return re.match(r'^\+?[0-9]{7,15}$', text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    
    if is_phone_number(query):
        # Пошук по номеру
        url = f"https://numverify.com/validate?number={query}"
        await update.message.reply_text(f"🔢 Номер виглядає як: {query}\n(Пошук ще в розробці — буде більше)")
    else:
        # Пошук по ніку
        username = query
        await update.message.reply_text(f"🔍 Шукаю профілі з нікнеймом: {username}\nЦе займе кілька секунд...")

        try:
            response = requests.get(f"https://www.namecheckr.com/namecheckr/?username={username}")
            if response.status_code == 200:
                await update.message.reply_text("✅ Деякі сайти, де знайдено цей нік: (в розробці буде повноцінна видача)")
            else:
                await update.message.reply_text("⚠️ Не вдалося знайти дані.")
        except Exception as e:
            await update.message.reply_text(f"Сталася помилка: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
