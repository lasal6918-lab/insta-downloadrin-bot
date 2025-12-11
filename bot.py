import telebot
import requests
import os

BOT_TOKEN = "8583621506:AAE6DR9bNJ4OYEbEK08bEMFxxO4-PdzJKcA"  

bot = telebot.TeleBot(BOT_TOKEN)

INSTAGRAM_API = "https://saveig.app/api?url="  # Public only API

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Send any *public* Instagram link.\nPrivate account not supported ❌", parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def download(msg):
    url = msg.text.strip()

    if "instagram.com" not in url:
        bot.reply_to(msg, "❌ Please send a valid Instagram URL.")
        return

    bot.send_message(msg.chat.id, "⏳ Downloading... Please wait.")

    try:
        api_url = INSTAGRAM_API + url
        data = requests.get(api_url).json()

        if "error" in data or data.get("is_private"):
            bot.send_message(msg.chat.id, "❌ Private account এর ভিডিও ডাউনলোড করা যাবে না!")
            return

        video_url = data['medias'][0]['url']
        bot.send_video(msg.chat.id, video_url)

    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Error: {str(e)}")

bot.polling()