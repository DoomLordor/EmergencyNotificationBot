import Keyboards
i = 0
b = []
v = []


def main(bot):
    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        v.append(message.from_user.id)
        bot.send_message(message.chat.id, 'Вас приветсвует Emergency Notification bot! \n'
                                          'Введите /help для получения справки по командам',
                         reply_markup=Keyboards.markup1)

    @bot.message_handler(commands=['help', 'h'])
    def help_handler(message):
        bot.send_message(message.chat.id,  'Список команд:\n1) /help - получение справки'
                                          '\n2) /numbers - номера телефонов спецслужб'
                                          '\n3) /reg - регистрация в приложении'
                                           '\n4) /edit - смена адресса регистрации',
                         reply_markup=Keyboards.markup2)


    @bot.message_handler(commands=['numbers'])
    def numbers_handler(message):
        bot.send_message(message.chat.id, '101 - пожарная служба'
                                          '\n102 - полиция'
                                          '\n103 - скорая помощь'
                                          '\n104 - газовая служба'
                                          '\n112 - мобильный агрегатор МЧС',
                         reply_markup=Keyboards.markup3)


    @bot.message_handler(content_types=['text'])
    def prp(massage):
        global i, b
        print(massage.from_user.first_name, '[',massage.from_user.id,']:', massage.text)
                                                                                                ##СДЕЛАТЬ ПРОВЕРКУ НА УНИКАЛЬНОСТЬ
        i += 1
        print('Сигнал',i,'/10')
        b.append(massage.chat.id)
        print(b)
        if i == 10:
            i = 0
            bot.send_message(b[-1], 'Вы находитесь в опасности')