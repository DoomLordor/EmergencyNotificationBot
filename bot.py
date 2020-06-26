import Keyboards
import key_phrase_extraction_example

i = 0
b = []
v = []
dict_adress={}
dict_baze={}
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
        global v
        if message.from_user.id not in v:
            v.append(message.from_user.id)
            save_data(message.from_user.id)
            with open('GlobalBaze.txt', 'a') as f:
                f.write(f'{message.from_user.id} {message.from_user.first_name}\n')
            bot.send_message(message.chat.id, 'Вас приветсвует Emergency Notification bot! \n'
                                              'Вы ещё не зарегестрированы в нашем приложении.\n'
                                              'Пройти Регистрацию?', reply_markup=Keyboards.markup4)
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
    def consAdr(message):
        bot.send_message(message.chat.id, 'Вы ещё не зарегистрированы. Для регистрации '
                                          'предоставьте нам свой адрес постоянного проживания \n Улица: ')
        bot.register_next_step_handler(message, homeHouse)

    def homeHouse(message):
        global HomeStreet
        HomeStreet = message.text
        bot.send_message(message.chat.id, 'Дом: ')
        bot.register_next_step_handler(message, workAdr)

    def workAdr(message):
        global HomeHouse
        HomeHouse = message.text
        bot.send_message(message.chat.id, 'Предоставьте нам свой адрес работы \n Улица:')
        bot.register_next_step_handler(message, workHouse)

    def workHouse(message):
        global WorkStreet
        WorkStreet = message.text
        bot.send_message(message.chat.id, 'Дом: ')
        bot.register_next_step_handler(message, studAdr)

    def studAdr(message):
        global WorkHouse
        WorkHouse = message.text
        bot.send_message(message.chat.id, 'Предоставьте нам свой адрес учебы \n Улица: ')
        bot.register_next_step_handler(message, studHouse)

    def studHouse(message):
        global StudStreet
        StudStreet = message.text
        bot.send_message(message.chat.id, 'Дом: ')
        bot.register_next_step_handler(message, out)

    def out(message):
        global StudHouse
        StudHouse = message.text
        bot.send_message(message.chat.id, 'Спасибо за предоставленную информацию',
                                            reply_markup=Keyboards.markup6)
        dict_adress = {1: HomeStreet, 2: HomeHouse, 3: WorkStreet, 4: WorkHouse, 5: StudStreet, 6: StudHouse}
        print(dict_adress)
        dict_baze = {1: message.from_user.id, 2: dict_adress}
        with open('Adress.txt', 'a') as f:
            f.write(f'{dict_baze}\n')

    #@bot.message_handler(content_types=['text'])
    #def prp(message):
    #    global i, b
    #    if message.text == 'Код МЧС 112':
     #       i = 49
     #   else:
      #      print(f'{message.from_user.first_name} [{message.from_user.id}]: {message.text}')
     #   if message.from_user.id not in b:
      #      i += 1
      #      print(f'Сигнал {i}/10')
      #      b.append(message.chat.id)
      #  if i > 9 and message.text!='Код МЧС 112':
      #      i = 0
       #     for id in b:
       #         bot.send_message(id, 'Вы находитесь в опасности')
       #     b.clear()
       # elif i == 50:
       #     i = 0
       #     for id in b:
       #         bot.send_message(id, 'МЧС ПРЕДУПРЕЖДАЕТ! \nВы находитесь в опасности')


def mailing(bot, text):
    for val in v:
        bot.send_message(val, text)


def save_data(val):
    with open('Baze.txt', 'a') as f:
        f.write(f'{val}\n')
