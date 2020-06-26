from key_phrase_extraction_example import *
i = 0
b = []
key = "50eb5695624243b59cc69f3c87a5289b"
endpoint = "https://emergencynotification.cognitiveservices.azure.com/"
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

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


    @bot.message_handler(content_types=['text'])
    def prp(massage):
        global i, b
        print(massage.from_user.first_name, '[',massage.from_user.id,']:', massage.text)
        i += 1
        print('Сигнал',i,'/10')
        b.append(massage.chat.id)
        print(b)
        if i == 2:
            i = 0
            bot.send_message(b[-1], 'Вы находитесь в опасности')

    @bot.message_handler(commands=['Notify about incident', 'h'])
    def Notify_center(message):
        bot.send_message(message.chat.id, "Расскажите о происшествии")
        bot.register_next_step_handler(message)
        response_keys=key_phrase_extraction_example(client, message)
        bot.send_message(message.chat.id, response_keys)