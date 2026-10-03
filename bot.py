from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import os
import re


# ==========================================
# НАЛАШТУВАННЯ
# ==========================================

import os

TOKEN = os.environ["BOT_TOKEN"]

ALLOWED_CHAT_ID = -1002830919044


TRIGGERS = {
    "камрад": "гав!",
    "собака": "уууу?",
    "пес": "гав?",
}


# ==========================================
# ОБРОБКА ПОВІДОМЛЕНЬ
# ==========================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return

    text = update.message.text

    if not text:
        return

    text = text.lower()

    for trigger, response in TRIGGERS.items():
        pattern = rf"(?<!\w){re.escape(trigger)}(?!\w)"

        if re.search(pattern, text):
            await update.message.reply_text(response)
            return
# ==========================================
# ЗАПУСК
# ==========================================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("Бот запущений!")

    app.run_polling()


if __name__ == "__main__":
    main()
