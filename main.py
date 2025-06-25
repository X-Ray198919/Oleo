import telebot
import openai
from flask import Flask, request

# 🔑 ВСТАВ СЮДИ СВІЙ OpenAI API-КЛЮЧ
openai.api_key = "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"

# 🔧 Твій Telegram Bot Token
bot = telebot.TeleBot("7527902782:AAGIvqAiL2EksXHFRAvHbK4-xrirMYSzo9s")

# 🌐 Flask-сервер
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Бот активний!'

@app.route('/', methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return ''

# 🤖 Обробка повідомлень
@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # gpt-4 не підключено
            messages=[
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response['choices'][0]['message']['content'])
    except Exception as e:
        bot.reply_to(message, f"Помилка: {str(e)}")

# 🚀 Запуск сервера
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


