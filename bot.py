i = 0
b = []


def main(bot):
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
