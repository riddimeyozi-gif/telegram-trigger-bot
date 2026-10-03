import os
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters


TOKEN = os.environ["BOT_TOKEN"]

TRIGGERS = {
    "Камрад": "Гав!",
    "собака": "у?",
    "пес": "Гав?",
}


async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    if update.effective_chat.type not in ("group", "supergroup"):
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


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

    def log_message(self, format, *args):
        pass


def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()


def main():
    health_thread = threading.Thread(
        target=run_health_server,
        daemon=True
    )
    health_thread.start()

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
