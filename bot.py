
from key_phrase_extraction_example import *

import Keyboards

i = 0
b = []
v = []
x = []
dict_adress={}
baze={}



def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def main(bot):
    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        bot.send_message(message.chat.id, 'Вас приветсвует Emergency Notification bot! \n'
                                          'Введите /help для получения справки по командам')

    @bot.message_handler(commands=['help', 'h'])
    def help_handler(message):
        bot.send_message(message.chat.id,  'Список команд:\n1) /help - получение справки'
                                          '\n2) /numbers - номера телефонов спецслужб'
                                          '\n3) /reg - регистрация в приложении'
                                           '\n4) /edit - смена адресса регистрации')

    @bot.message_handler(commands=['numbers', 'h'])
    def numbers_handler(message):
        bot.send_message(message.chat.id, '101 - пожарная служба'
                                          '\n102 - полиция'
                                          '\n103 - скорая помощь'
                                          '\n104 - газовая служба'
                                          '\n112 - мобильный агрегатор МЧС')




    @bot.message_handler(commands = ['reg', 'h'])
    def consAdr(massage):
        bot.send_message(massage.chat.id, 'Вы ещё не зарегистрированы. Для регистрации предоставьте нам свой адрес постоянного проживания ')
        bot.register_next_step_handler(massage, workAdr)


    def workAdr(massage):
        global home
        home =massage.text

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
                                             '3) /edit - смена адресса регистрации\n'
                                             '4) /EXIT - Выход из системы',
                                             reply_markup=Keyboards.markup2)



    @bot.message_handler(commands=['numbers'])
    def numbers_handler(message):
        bot.send_message(message.chat.id,    '101 - пожарная служба\n'
                                             '102 - полиция\n'
                                             '103 - скорая помощь\n'
                                             '104 - газовая служба\n'
                                             '112 - мобильный агрегатор МЧС',
                                             reply_markup=Keyboards.markup3)

    @bot.message_handler(commands=['reg', 'h'])
    def consAdr(massage):
        bot.send_message(massage.chat.id,
                         'Вы ещё не зарегистрированы. Для регистрации предоставьте нам свой адрес постоянного проживания \n Улица: ')
        bot.register_next_step_handler(massage, homeHouse)

    def homeHouse(massage):
        global HomeStreet
        HomeStreet = massage.text
        bot.send_message(massage.chat.id, 'Дом: ')
        bot.register_next_step_handler(massage, workAdr)

    def workAdr(massage):
        global HomeHouse
        HomeHouse = massage.text
        bot.send_message(massage.chat.id, 'Предоставьте нам свой адрес работы \n Улица:')
        bot.register_next_step_handler(massage, workHouse)

    def workHouse(massage):
        global WorkStreet
        WorkStreet = massage.text
        bot.send_message(massage.chat.id, 'Дом: ')
        bot.register_next_step_handler(massage, studAdr)

    def studAdr(massage):
        global WorkHouse
        WorkHouse = massage.text
        bot.send_message(massage.chat.id, 'Предоставьте нам свой адрес учебы \n Улица: ')
        bot.register_next_step_handler(massage, studHouse)

    def studHouse(massage):
        global StudStreet
        StudStreet = massage.text
        bot.send_message(massage.chat.id, 'Дом: ')
        bot.register_next_step_handler(massage, out)

    def out(massage):
        global StudHouse
        StudHouse = massage.text
        bot.send_message(massage.chat.id, 'Спасибо за предоставленную информацию')
        dict_adress = {1: HomeStreet, 2: HomeHouse, 3: WorkStreet, 4: WorkHouse, 5: StudStreet, 6: StudHouse}
        print(dict_adress)

    @bot.message_handler(content_types=['text'])
    def keyPhrases(massage):
        response_keys = key_phrase_extraction_example(client, massage.text)
        responses = ''
        for phrase in response_keys:
            responses = responses + phrase + ','
        bot.send_message(massage.chat.id, responses)
        b.append(massage.chat.id)


def mailing(bot, text):
    for val in v:
        bot.send_message(val, text)


def save_data(val):
    with open('Baze.txt', 'a') as f:
        f.write(f'{val}\n')

