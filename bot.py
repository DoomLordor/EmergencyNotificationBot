from key_phrase_extraction_example import *
i = 0
b = []


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
        bot.send_message(massage.chat.id, 'Предоставьте нам свой адрес работы ')

        bot.register_next_step_handler(massage, studAdr)

    def studAdr(massage):
        global work
        work =massage.text
        bot.send_message(massage.chat.id, 'Предоставьте нам свой адрес учебы ')

        bot.register_next_step_handler(massage, out)

    def out(massage):
        global stud
        stud =massage.text
        #  global home, work, stud
        bot.send_message(massage.chat.id, 'Спасибо за предоставленную информацию')
        dict_adress = {1:home, 2:work, 3:stud}
        print(dict_adress)

    @bot.message_handler(content_types=['text'])
    def prp(massage):
        response_keys = key_phrase_extraction_example(client, massage.text)
        responses = ''
        for phrase in response_keys:
            responses = responses + phrase + ','
        bot.send_message(massage.chat.id, responses)
        b.append(massage.chat.id)
