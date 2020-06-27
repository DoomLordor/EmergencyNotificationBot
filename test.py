import http.client
from telebot import TeleBot
from psycopg2 import connect
from threading import Thread
from model.database import get_all_user, get_user
from TelegramBot.bot_logic import handler, mailing, important_mailing, danger_user
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from model.config import token_telegram_bot, database_connect, key, endpoint, Disasters


def main(bot, conn, client):
    people_danger = {}
    variable = Thread(target=start_bot, args=(bot,))
    variable1 = Thread(target=handler, args=(bot, conn, client))
    variable.start()
    variable1.start()
    ip = get_ip()
    mailing(bot, f'Бот запущен на сервере у {ip}', [1011917065, 809971387, 453207183, 283130759])
    while True:
        message = input('Сообщение: ')
        if message.lower() in Disasters:
            street = input('Введите улицу проишествия: ').lower()
            num = input('Введите дом проишествия: ')
            users = get_user(conn, f'{street}:{num}')
            message = f'По аддресу {street.title()} {num} произошло проишествие: {message}'
            important_mailing(bot, message, users)
            danger_user(users, f'{street.title()} {num}')
        elif message.lower() == 'стоп':
            bot.stop_polling()
            variable.join()
            variable1.join()
            mailing(bot, 'Бот остановлен', [1011917065, 809971387, 453207183, 283130759])
            break
        else:
            mailing(bot, message,  get_all_user(conn))
            print(message)


def start_bot(bot):
    bot.polling(none_stop=True, interval=1)


def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client


def get_ip():
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode("utf-8")


if __name__ == '__main__':
    bot = TeleBot(token_telegram_bot)
    print('Бот подключен')
    conn = connect(**database_connect)
    print('База данных подключена')
    client = authenticate_client()
    print('Когнетивный сервис подключен')
    main(bot, conn, client)
