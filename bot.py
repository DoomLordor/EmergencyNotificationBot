import Keyboards
i = 0
b = []
v = []
x = []
dict_adress={}
baze={}


def main(bot):
    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        global v
        if message.from_user.id not in v:
            v.append(message.from_user.id)
            save_data(message.from_user.id)
            with open('GlobalBaze.txt', 'a') as f:
                f.write(f'{message.from_user.id} {message.from_user.first_name}\n')
            bot.send_message(message.chat.id, 'Вас приветсвует Emergency Notification bot! \n'
                                              'Вы ещё не зарегестрированы в нашем приложении.\n'
                                              'Пройти Регистрацию?',
                                              reply_markup=Keyboards.markup4)
        else:
            bot.send_message(message.chat.id,    'Вас приветсвует Emergency Notification bot! \n'
                                                 'Введите /help для получения справки по командам',
                                                 reply_markup=Keyboards.markup1)

    @bot.message_handler(commands=['EXIT'])
    def exit_handler(message):
            bot.send_message(message.chat.id, 'Всего доброго', reply_markup=Keyboards.markup5)

    @bot.message_handler(commands=['help', 'h'])
    def help_handler(message):
        bot.send_message(message.chat.id,    'Список команд:\n'
                                             '1) /help - получение справки\n'
                                             '2) /numbers - номера телефонов спецслужб\n'
                                             '3) /reg - регистрация в приложении\n'
                                             '4) /edit - смена адресса регистрации\n'
                                             '5) "/EXIT" - Выход из системы',
                                             reply_markup=Keyboards.markup2)

    @bot.message_handler(commands=['numbers'])
    def numbers_handler(message):
        bot.send_message(message.chat.id,    '101 - пожарная служба\n'
                                             '102 - полиция\n'
                                             '103 - скорая помощь\n'
                                             '104 - газовая служба\n'
                                             '112 - мобильный агрегатор МЧС',
                                             reply_markup=Keyboards.markup3)


    def prp(message):
        global i, b
        print(f'{message.from_user.first_name} [{message.from_user.id}]: {message.text}')

        if message.from_user.id not in b:
            i += 1
            print(f'Сигнал{i}/10')
            b.append(message.chat.id)
        if i == 3:
            i = 0
            for id in b:
                bot.send_message(id, 'Вы находитесь в опасности')
            b.clear()


def mailing(bot, text):
    for val in v:
        bot.send_message(val, text)


def save_data(val):
    with open('Baze.txt', 'a') as f:
        f.write(f'{val}\n')
