from threading import Thread
from telebot import TeleBot
import bot as t


def main(bot):
    with open('Baze.txt', 'r') as f:
        text = f.read().split('\n')
        text.pop()
        t.v = list(map(int, text))
    variable = Thread(target=start_bot, args=(bot,))
    variable1 = Thread(target=t.main, args=(bot,))
    variable.start()
    variable1.start()
    while True:
        a = input(': ')
        if a.lower() == 'пожар':
            t.mailing(bot, a)
        elif a.lower() == 'стоп':
            variable.join()
            variable1.join()
            bot.stop_polling()
        else:
            t.mailing(bot, a)
            print(a)


def start_bot(bot):
    bot.polling(none_stop=True, interval=0)




if __name__ == '__main__':
    bot = TeleBot('1213132925:AAE2jwkv00Xgl6AeyQj9UxgkZE5QoHpm2fU')

    main(bot)
