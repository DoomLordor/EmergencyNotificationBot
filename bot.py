import telebot

bot = telebot.TeleBot('1213132925:AAE2jwkv00Xgl6AeyQj9UxgkZE5QoHpm2fU')


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    bot.send_message(message.chat.id, 'заебись')
    bot.register_next_step_handler(message, prp)


def prp(massage):
    bot.send_message(massage.chat.id, 'Вы сказали: {}'.format(massage.text))


<<<<<<< Updated upstream
bot.polling(none_stop=True, interval=0)
=======
    @bot.message_handler(content_types=['text'])
    def prp(massage):
        global i, b
        print(massage.from_user.first_name, '[',massage.from_user.id,']:', massage.text)
        response_keys = key_phrase_extraction_example(client, massage.text)
        bot.send_message(massage.chat.id, response_keys)
        i += 1
        print('Сигнал',i,'/10')
        b.append(massage.chat.id)
        print(b)
        if i == 2:
            i = 0
            bot.send_message(b[-1], 'Вы находитесь в опасности')

>>>>>>> Stashed changes
