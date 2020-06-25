i = 0
b = []


def main(bot):  # сюда писать только функции которые трубуют декоратора
    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        bot.send_message(message.chat.id, 'заебись')

    @bot.message_handler(content_types=['text'])
    def prp(massage):
        global i, b
        i += 1
        print(i)
        b.append(massage.chat.id)
        if i == 3:
            i = 0
            bot.send_message(b[-1], 'Сон')


def mailing(bot, text):
    v = [1011917065, 809971387]
    for val in v:
        bot.send_message(val, text)