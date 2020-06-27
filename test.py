from telebot import TeleBot
from psycopg2 import connect
from threading import Thread
from model.database import get_all_user
from TelegramBot.bot_logic import handler, mailing
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from model.config import token_telegram_bot, database_connect, key, endpoint


def main(bot, conn, client):
    variable = Thread(target=start_bot, args=(bot,))
    variable1 = Thread(target=handler, args=(bot, conn, client))
    variable.start()
    variable1.start()
    while True:
        a = input('Сообщение: ')
        if a.lower() == 'пожар':
            mailing(bot, a, get_all_user(conn))
        elif a.lower() == 'стоп':
            variable.join()
            variable1.join()
            bot.stop_polling()
        else:
            mailing(bot, a, connect)
            print(a)


def start_bot(bot):
    bot.polling(none_stop=True, interval=1)


def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=ta_credential)
    return text_analytics_client


if __name__ == '__main__':
    bot = TeleBot(token_telegram_bot)
    print('Бот подключен')
    conn = connect(**database_connect)
    print('База данных подключена')
    client = authenticate_client()
    print('Когнетивный сервис подключен')
    main(bot, conn, client)
