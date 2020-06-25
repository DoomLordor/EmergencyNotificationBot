import telebot

bot = telebot.TeleBot('1213132925:AAE2jwkv00Xgl6AeyQj9UxgkZE5QoHpm2fU')


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'заебись')
    bot.register_next_step_handler(message, prp)


def prp(massage):
    bot.send_message(massage.chat.id, 'Вы сказали: {}'.format(massage.text))


bot.polling(none_stop=True, interval=0)
