import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")  # Render environment variables-dan götür
bot = telebot.TeleBot(TOKEN)

CHANNEL_ID = "@sənin_kanal_adın"  # məsələn: @mytestchannel

def send_test_message():
    bot.send_message(CHANNEL_ID, "✅ Botdan test mesajı göndərildi!")
    print("Mesaj kanala göndərildi.")

if __name__ == "__main__":
    send_test_message()
