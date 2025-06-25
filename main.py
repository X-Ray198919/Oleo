
import telebot
import openai
import flask
import os
import requests

TOKEN = "7527902782:AAGIvqAiL2EksXHFRAvHbK4-xrirMYSzo9s"
bot = telebot.TeleBot(TOKEN)
app = flask.Flask(__name__)

openai.api_key = "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"

@app.route(f"/{TOKEN}", methods=["POST"])
def receive_message():
    json_string = flask.request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response.choices[0].message["content"])
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@app.route("/", methods=["GET"])
def index():
    return "Бот працює 🟢"

# Встановлення webhook при кожному запуску
WEBHOOK_URL = f"https://oleo.onrender.com/{TOKEN}"
set_hook_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"
requests.get(set_hook_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
