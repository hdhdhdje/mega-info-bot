import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import re
import aiohttp  # Асинхронний HTTP клієнт

TOKEN = "тут_твій_токен"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Надішли мені нікнейм або номер телефону, і я спробую знайти максимум інформації 🔍")

def is_phone_number(text):
    # Допускаємо + і від 7 до 15 цифр
    return re.fullmatch(r'\+?\d{7,15}', text) is not None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()

    if is_phone_number(query):
        # Пошук по номеру телефону (поки заглушка)
        await update.message.reply_text(f"🔢 Номер виглядає як: {query}\n(Пошук ще в розробці — буде більше)")
    else:
        # Пошук по ніку
        username = query
        await update.message.reply_text(f"🔍 Шукаю профілі з нікнеймом: {username}\nЦе займе кілька секунд...")

        url = f"https://www.namecheckr.com/namecheckr/?username={username}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        # Тут можна парсити html resp.text(), але поки просто повідомлення
                        await update.message.reply_text("✅ Деякі сайти, де знайдено цей нік: (в розробці буде повноцінна видача)")
                    else:
                        await update.message.reply_text("⚠️ Не вдалося знайти дані.")
        except Exception as e:
            await update.message.reply_text(f"Сталася помилка при пошуку: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
