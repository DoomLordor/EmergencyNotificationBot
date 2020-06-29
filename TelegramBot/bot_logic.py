import os
import requests
import speech_recognition as sr
from pydub import AudioSegment
import TelegramBot.Keyboards as KB
from model.database import set_address, new_user, get_all_user
from model.config import token_telegram_bot
from model.key_phrase_extraction import key_phrase_extraction
from model.config import Disasters

song = {}
reg = {}
address = {}
pattern = {'street': '', 'type_place': '', 'save_address': True, 'address': ''}
all_users_id_danger = {}
people_danger = {}


def emergency_mailing(bot, text, users):
    danger_user_id = users.copy()
    for id in users:
        if type(id) is str:
            id = int(id)
        bot.send_message(id, f'{text}\n Вы сейчас находитесть по данному адресу?', reply_markup=KB.EmergencyMailingMenu)
    return danger_user_id


def handler(bot, connect, client):

    def check_exit(func):
        def wrapper(message, *arg, **keyword):
            if message.text == '/exit':
                exit_handler(message)
            else:
                func(message, *arg, **keyword)
        return wrapper

    @bot.message_handler(commands=['admin'])
    def admin_handler(message):
        if message.from_user.id == 809971387:

            bot.send_message(message.chat.id, 'Привет Хозяин',
                             reply_markup=KB.AdminMenu)
            bot.send_message(message.chat.id, 'Сообщение пользователям:')
            bot.register_next_step_handler(message, Consol)

    @check_exit
    def Consol(message):
        message = message.text
        from model.logic import dangerous_stop, dangerous_start
        if message.lower() in Disasters:
            dangerous_start(message, bot, connect)
        elif message.lower() == 'проишествие стоп':
            dangerous_stop()
        else:
            mailing(bot, message, get_all_user(connect))
            print(message)

    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        if str(message.from_user.id) not in get_all_user(connect):
            new_user(connect, message.from_user.id)
            bot.send_message(message.chat.id,
                             'Вас приветсвует Emergency Notification bot! \n'
                             'Вы ещё не зарегестрированы в нашем приложении.\n'
                             'Пройти Регистрацию?', reply_markup=KB.FirstConnectMenu)

        else:
            bot.send_message(message.chat.id,
                             'Вас приветсвует Emergency Notification bot! \n'
                             'Введите /help для получения справки по командам',
                             reply_markup=KB.StartMenu)

    @bot.message_handler(commands=['exit'])
    def exit_handler(message):
        global reg

        if reg.get(message.from_user.id):
            reg.pop(message.from_user.id)
            address.pop(message.from_user.id)
        bot.send_message(message.chat.id, f'Всего доброго, {message.from_user.first_name}', reply_markup=KB.ExitMenu)

    @bot.message_handler(commands=['help', 'h'])
    def help_handler(message):
        bot.send_message(message.chat.id,
                         'Список команд:\n'
                         '1) /help - получение справки\n'
                         '2) /numbers - номера телефонов спецслужб\n'
                         '3) /update - смена адресса регистрации\n'
                         '4) /description - Перейсти к описанию ЧС\n'
                         '5) /exit - Выход из системы',
                         reply_markup=KB.HelpMenu)

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
                         reply_markup=KB.NumbersMenu)

    @bot.message_handler(commands=['reg'])
    def registration(message):
        global reg
        reg[message.from_user.id] = pattern.copy()
        bot.send_message(message.chat.id, 'Отправте тип регистрации:', reply_markup=KB.RegistrationMenu)
        bot.register_next_step_handler(message, get_type_place)

    @check_exit
    def get_type_place(message):
        global reg

        text = message.text

        if text.lower() == 'место проживания':
            reg[message.from_user.id]['type_place'] = 'home'

        elif text.lower() == 'место учёбы':
            reg[message.from_user.id]['type_place'] = 'stud'

        elif text.lower() == 'место работы':
            reg[message.from_user.id]['type_place'] = 'work'

        else:
            bot.send_message(message.chat.id, 'Отправте тип регистрации:', reply_markup=KB.RegistrationMenu)
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
            reg[message.from_user.id]['street'] = message.text.lower()
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
            bot.send_message(message.chat.id, 'Адрес добавлен.', reply_markup=KB.StartMenu)
            reg.pop(message.from_user.id)

        else:
            street = reg[message.from_user.id]['street']
            address[message.from_user.id] = f'{street}:{message.text}'

    def recogn(message):  # для когнитивки
        file_info = bot.get_file(message.voice.file_id)
        name = f'{message.chat.id}.ogg'
        name = os.path.join('audio', name)
        file = requests.get('https://api.telegram.org/file/bot{}/{}'.format(token_telegram_bot, file_info.file_path))
        f = open(name, "wb")
        f.write(file.content)
        f.close()
        path = os.path.join(os.getcwd(), name)

        song[message.chat.id] = AudioSegment.from_file(path, 'ogg')
        os.remove(path)
        song[message.chat.id].export(path.replace('.ogg', '.wav'), format="wav")
        path = path.replace('.ogg', '.wav')

        f = sr.AudioFile(path)
        r = sr.Recognizer()
        with f as audio_file:
            audio_content = r.record(audio_file)

        text = r.recognize_google(audio_content, language='Ru-r')
        os.remove(path)
        return text

    @bot.message_handler(commands=['description', 'd'])
    def description_key(message):
        bot.send_message(message.chat.id, 'Опишите ситуацию: ')
        bot.register_next_step_handler(message, main_description)

    def main_description(message):
        if not message.text:
            message.text = recogn(message)
            bot.send_message(message.chat.id, f'Вы сказали:\n{message.text}')
        print(f'{message.from_user.first_name} [{message.from_user.id}]: {message.text}\n{keyPhrases(message)}')
        bot.send_message(message.chat.id, f'{message.from_user.first_name}, спасибо за предоставленную информацию',
                         reply_markup=KB.StartMenu)

    def keyPhrases(message):  # для когнитивки
        return ', '.join(key_phrase_extraction(message))


def dangerous_processing(bot):
    @bot.message_handler(content_types=['text'])
    def check_danger_user(message):
        if str(message.from_user.id) in all_users_id_danger:
            if message.text.lower() == 'да':
                address = all_users_id_danger[str(message.from_user.id)]
                all_users_id_danger.pop(str(message.from_user.id))
                bot.send_message(message.from_user.id, 'Следйте дальнейшим инструкциям')
                people_danger[str(message.from_user.id)] = ["user", message.from_user.id, address]

            elif message.text.lower() == 'нет':
                bot.send_message(message.from_user.id, 'Находились ли ваши близкие по указанному адресу в тот момет?\n'
                                                       'Если да, то укажите их количество.')
                bot.register_next_step_handler(message, check_danger_user_close)

            else:
                bot.send_message(message.from_user.id, 'Не верный ответ.')
                bot.register_next_step_handler(message, check_danger_user)

    def check_danger_user_close(message):
        if message.text.lower() == 'нет':
            all_users_id_danger.pop(str(message.from_user.id))
            bot.send_message(message.from_user.id, 'Хорошо. Удачного вам дня.')

        elif message.text.isdigit():
            address = all_users_id_danger[str(message.from_user.id)]
            all_users_id_danger.pop(str(message.from_user.id))
            people_danger[str(message.from_user.id)] = ["not_user", message.text, address]
            bot.send_message(message.from_user.id, 'Данные были переданы спец службам')

        else:
            bot.send_message(message.from_user.id, 'Не верный ответ.')
            bot.register_next_step_handler(message, check_danger_user)


def mailing(bot, text, users):
    for id in users:
        if type(id) is str:
            id = int(id)
        bot.send_message(id, text)
