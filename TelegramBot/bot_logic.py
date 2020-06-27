import TelegramBot.Keyboards as KB
from model.database import set_address, new_user, get_all_user
reg = {}
address = {}
pattern = {'street': '', 'type_place': '', 'save_address': True, 'address': ''}


def handler(bot, connect):

    def check_exit(func):
        def wrapper(message, *arg, **keyword):
            if message.text == '/exit':
                exit_handler(message)
            else:
                func(message, *arg, **keyword)
        return wrapper

    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):

        if str(message.from_user.id) not in get_all_user(connect):
            new_user(connect, message.from_user.id)
            bot.send_message(message.chat.id,
                             'Вас приветсвует Emergency Notification bot! \n'
                             'Вы ещё не зарегестрированы в нашем приложении.\n'
                             'Пройти Регистрацию?', reply_markup=KB.markup4)
        else:
            bot.send_message(message.chat.id,
                             'Вас приветсвует Emergency Notification bot! \n'
                             'Введите /help для получения справки по командам',
                             reply_markup=KB.markup1)

    @bot.message_handler(commands=['exit'])
    def exit_handler(message):
        global reg
        if reg.get(message.from_user.id):
            reg.pop(message.from_user.id)
        address.pop(message.from_user.id)
        bot.send_message(message.chat.id, f'Всего доброго, {message.from_user.first_name}', reply_markup=KB.markup5)

    @bot.message_handler(commands=['help', 'h'])
    def help_handler(message):
        bot.send_message(message.chat.id,
                         'Список команд:\n'
                         '1) /help - получение справки\n'
                         '2) /numbers - номера телефонов спецслужб\n'
                         '3) /update - смена адресса регистрации\n'
                         '4) /exit - Выход из системы\n'
                         '5) /description - Перейсти к описанию ЧС',
                         reply_markup=KB.markup2)

    @bot.message_handler(commands=['update'])
    def update_place(message):
        registration(message)

    @bot.message_handler(commands=['numbers'])
    def numbers_handler(message):
        bot.send_message(message.chat.id,
                         '101 - пожарная служба\n'
                         '102 - полиция\n'
                         '103 - скорая помощь\n'
                         '104 - газовая служба\n'
                         '112 - мобильный агрегатор МЧС',
                         reply_markup=KB.markup3)

    @bot.message_handler(commands=['reg'])
    def registration(message):
        global reg
        reg[message.from_user.id] = pattern.copy()
        bot.send_message(message.chat.id, 'Отправте тип регистрации:', reply_markup=KB.markup7)
        bot.register_next_step_handler(message, get_type_place)

    @check_exit
    def get_type_place(message):
        global reg
        text = message.text
        if text == 'Место проживания':
            reg[message.from_user.id]['type_place'] = 'home'
        elif text == 'Место учёбы':
            reg[message.from_user.id]['type_place'] = 'stud'
        elif text == 'Место работы':
            reg[message.from_user.id]['type_place'] = 'work'
        else:
            bot.send_message(message.chat.id, 'Отправте тип регистрации:', reply_markup=KB.markup7)
            bot.register_next_step_handler(message, get_type_place)
        if reg[message.from_user.id]['type_place']:
            bot.send_message(message.chat.id, 'Отправте название улицы:')
            bot.register_next_step_handler(message, get_street)

    @check_exit
    def get_street(message):
        global reg
        if message.text.isdigit():
            bot.send_message(message.chat.id, 'Название улицы не может состоять из цифр.')
            bot.send_message(message.chat.id, 'Отправте название улицы:')
            bot.register_next_step_handler(message, get_street)
        else:
            reg[message.from_user.id]['street'] = message.text
            bot.send_message(message.chat.id, 'Отправте номер дома:')
            bot.register_next_step_handler(message, get_home_number)

    @check_exit
    def get_home_number(message):
        global reg, address
        if message.text.isalpha():
            bot.send_message(message.chat.id, 'Номер дома не может состоять из букв.')
            bot.send_message(message.chat.id, 'Отправте номер дома:')
            bot.register_next_step_handler(message, get_street)
        elif reg[message.from_user.id]['save_address']:
            street = reg[message.from_user.id]['street']
            addr = f'{street}:{message.text}'
            set_address(connect, message.from_user.id, reg[message.from_user.id]['type_place'], addr)
            bot.send_message(message.chat.id, 'Адрес добавлен.', reply_markup=KB.markup1)
            reg.pop(message.from_user.id)
        else:
            street = reg[message.from_user.id]['street']
            address[message.from_user.id] = f'{street}:{message.text}'

    # @bot.message_handler(commands=['description', 'd'])
    # def description_key(message):
    #     bot.send_message(message.chat.id, 'Опишите ситуацию: ')
    #     bot.register_next_step_handler(message, main_description)
    #
    # def main_descriptiont(message):
    #         global i, b
    #         print(f'{message.from_user.first_name} [{message.from_user.id}]: {message.text}')
    #         ## Проверять адресс и ссумировать только схожие
    #         if message.from_user.id not in b:
    #             i += 1
    #             print(f'Сигнал {i}/10')
    #             b.append(message.chat.id)
    #         if i > 9:
    #             i = 0
    #             ## Добавить в b Id с улицы и дома где всё произошло
    #             for id in b:
    #                 bot.send_message(id, 'Вы находитесь в опасности')
    #             b.clear()
    #         bot.send_message(message.chat.id, f'{message.from_user.first_name} Спасибо за предоставленную информацию',
    #                          reply_markup=KB.markup1)


def mailing(bot, text, users):
    for id in users:
        bot.send_message(id, text)
