import telebot

bot = telebot.TeleBot('1213132925:AAE2jwkv00Xgl6AeyQj9UxgkZE5QoHpm2fU')


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'заебись')


bot.polling(none_stop=True, interval=0)
