import Keyboards
i = 0
b = []
v = []


def main(bot):
    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        global v
        if message.from_user.id not in v:
            v.append(message.from_user.id)
        bot.send_message(message.chat.id, 'Вас приветсвует Emergency Notification bot! \n'
                                          'Введите /help для получения справки по командам',
                         reply_markup=Keyboards.markup1)

    @bot.message_handler(commands=['help', 'h'])
    def help_handler(message):
        bot.send_message(message.chat.id,   'Список команд:\n'
                                            '1) /help - получение справки\n'
                                            '2) /numbers - номера телефонов спецслужб\n'
                                            '3) /reg - регистрация в приложении\n'
                                            '4) /edit - смена адресса регистрации',
                         reply_markup=Keyboards.markup2)

    @bot.message_handler(commands=['numbers'])
    def numbers_handler(message):
        bot.send_message(message.chat.id, '101 - пожарная служба\n'
                                          '102 - полиция\n'
                                          '103 - скорая помощь\n'
                                          '104 - газовая служба\n'
                                          '112 - мобильный агрегатор МЧС',
                         reply_markup=Keyboards.markup3)

    @bot.message_handler(content_types=['text'])
    def prp(massage):
        global i, b
        print(f'{massage.from_user.first_name} [{massage.from_user.id}]: massage.text')

        if massage.from_user.id not in b:
            i += 1
            print(f'Сигнал{i}/10')
            b.append(massage.chat.id)
        if i == 3:
            i = 0
            for id in b:
                bot.send_message(id, 'Вы находитесь в опасности')
            b.clear()


def mailing(bot, text):
    for val in v:
        bot.send_message(val, text)
