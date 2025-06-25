
import telebot
from flask import Flask, request
import openai

TOKEN = "7527902782:AAGIvqAiL2EksXHFRAvHbK4-xrirMYSzo9s"
bot = telebot.TeleBot(TOKEN)

openai.api_key = "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"

app = Flask(__name__)

@app.route('/')
def index():
    return "Бот працює!"

@app.route(f"/{TOKEN}", methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                { "role": "user", "content": message.text }
            ]
        )
        reply = response['choices'][0]['message']['content']
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Виникла помилка при зверненні до OpenAI API.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://oleo.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=10000)
