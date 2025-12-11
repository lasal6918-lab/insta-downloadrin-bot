
import telebot
import requests
import os

BOT_TOKEN = os.getenv("8583621506:AAE6DR9bNJ4OYEbEK08bEMFxxO4-PdzJKcA")  # Secure: read token from environment
bot = telebot.TeleBot(BOT_TOKEN)

# Working public Instagram downloader API
INSTAGRAM_API = "https://igram.world/api/instagram?url="  


@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(
        msg,
        "Send any *public* Instagram link.\nPrivate accounts are not supported ❌",
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda m: True)
def download(msg):
    url = msg.text.strip()

    if "instagram.com" not in url:
        bot.reply_to(msg, "❌ Please send a valid Instagram URL.")
        return

    bot.send_message(msg.chat.id, "⏳ Downloading... Please wait.")

    try:
        api_url = INSTAGRAM_API + url
        response = requests.get(api_url).json()

        # Check for errors or private profile
        if "error" in response or response.get("is_private"):
            bot.send_message(msg.chat.id, "❌ Unable to download. Private accounts are not supported.")
            return

        video_url = response['medias'][0]['url']
        bot.send_video(msg.chat.id, video_url)

    except Exception as e:
        bot.send_message(msg.chat.id, f"❌ Error: {str(e)}")


bot.polling()