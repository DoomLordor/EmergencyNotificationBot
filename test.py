from telebot import TeleBot
from psycopg2 import connect
from threading import Thread
from model.logic import dangerous_start, dangerous_stop, timer, get_ip, danger, flag
from model.database import get_all_user
from TelegramBot.bot_logic import handler, mailing
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from model.config import token_telegram_bot, database_connect, key, endpoint, Disasters


def main(bot, conn, client):
    bot_work = Thread(target=start_bot, args=(bot,))
    bot_logic = Thread(target=handler, args=(bot, conn, client))
    timer_danger = Thread(target=timer, args=(danger,))
    bot_work.start()
    bot_logic.start()
    timer_danger.start()
    ip = get_ip()

    mailing(bot, f'Бот запущен на сервере у {ip}', [1011917065, 809971387, 453207183, 283130759])

    while True:
        message = input('Сообщение: ')
        if message.lower() in Disasters:
            dangerous_start(message, bot, conn)
        elif message.lower() == 'проишествие стоп':
            dangerous_stop()
        elif message.lower() == 'стоп':
            bot_stop(bot, bot_work, bot_logic, timer_danger)
            conn.close()
            mailing(bot, 'Бот остановлен', [1011917065, 809971387, 453207183])
            break
        else:
            mailing(bot, message,  get_all_user(conn))
            print(message)


def start_bot(bot):
    bot.polling(none_stop=True, interval=1)


def bot_stop(bot, *flows):
    bot.stop_polling()
    flag[0] = False
    for flow in flows:
        flow.join()


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
