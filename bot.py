import telebot
import yt_dlp
import os
import time
import re

# ===== تنظیمات بات =====
BOT_NAME = "@Pintrestdownloader1bot"
TOKEN = "8804462951:AAEZUyrc8OWZ7kig8JA2MqjU36uH4H88uWc"

bot = telebot.TeleBot(TOKEN, timeout=120)


def download_media(url):
    folder = "downloads"

    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = f"{folder}/file_{int(time.time())}.%(ext)s"

    options = {
        "outtmpl": filename,
        "format": "best",
        "noplaylist": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        }
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)

    except Exception as e:
        print("DOWNLOAD ERROR:", e)
        return None


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"🤖 به {BOT_NAME} خوش اومدی!\n\n📌 لینک Pinterest رو برام بفرست تا برات دانلود کنم.")


@bot.message_handler(func=lambda m: True)
def handle(message):

    match = re.search(r"https?://\S+", message.text)

    if not match:
        bot.reply_to(message, "❌ لینک پیدا نشد")
        return

    url = match.group(0)

    if "pin.it" not in url and "pinterest.com" not in url:
        bot.reply_to(message, "❌ فقط لینک Pinterest")
        return

    msg = bot.reply_to(message, "⏳ در حال دانلود...")

    file = download_media(url)

    if not file:
        bot.edit_message_text(
            "❌ دانلود نشد",
            message.chat.id,
            msg.message_id
        )
        return

    try:
        with open(file, "rb") as f:
            bot.send_document(
                message.chat.id,
                f,
                timeout=120
            )

    except Exception as e:
        print("SEND ERROR:", e)
        bot.send_message(message.chat.id, "❌ خطا در ارسال")

    finally:
        try:
            os.remove(file)
        except:
            pass


print("🚀 BOT RUNNING")
print(f"🤖 Bot Name: {BOT_NAME}")
print(f"🔑 Token: {TOKEN[:10]}...")
print("📌 Pinterest Downloader Active")
bot.infinity_polling()
