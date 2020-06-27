from telebot import TeleBot
from psycopg2 import connect
from threading import Thread
from model.database import get_all_user
from TelegramBot.bot_logic import handler, mailing
from model.config import token_telegram_bot, database_connect


def main(bot, conn):
    variable = Thread(target=start_bot, args=(bot,))
    variable1 = Thread(target=handler, args=(bot, conn))
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


if __name__ == '__main__':
    bot = TeleBot(token_telegram_bot)
    print('Бот подключен')
    conn = connect(**database_connect)
    print('База данных подключена')
    main(bot, conn)
