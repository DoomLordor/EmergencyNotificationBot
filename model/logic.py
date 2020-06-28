import http.client
from threading import Thread
from time import time, sleep
from model.database import get_user
from TelegramBot.bot_logic import emergency_mailing, dangerous_processing

danger = []
flag = [True]


def dangerous_start(message, bot, connected):

    street = input('Введите улицу проишествия: ').lower()
    num = input('Введите дом проишествия: ')

    users = get_user(connected, f'{street}:{num}')

    message = f'По аддресу {street.title()} {num} произошло проишествие: {message}'

    users_id = emergency_mailing(bot, message, users)

    time_start = time()

    people_danger = {}

    flag = False

    danger.append([Thread(target=dangerous_processing, args=(bot, users_id, people_danger), name=f'{street}:{num}'),
                   time_start, users_id, flag])
    danger[-1][0].start()


def dangerous_stop():
    street = input('Введите улицу проишествия: ').lower()
    num = input('Введите дом проишествия: ')
    address = f'{street}:{num}'
    flag = True
    for flow in danger:
        if flow.getName() == address:
            flow[3] = False
            flag = False
    if flag:
        print('Проишествия по такому адресу нет')


def timer(flows):
    while flag[0]:
        for flow in flows:
            if flow[1] - time() > 100:
                flow[0].join()
                print(f'По аддресу {flow[0].getName()} время вышло')
                # Клаву пользователю нужно вернуть на стартовую
                flows.remove(flow)
            elif not flow[2]:
                flow[0].join()
                print(f'По аддресу {flow[0].getName()} опрос окончен')
                flows.remove(flow)
            elif flow[3]:
                flow[0].join()
                print(f'По аддресу {flow[0].getName()} ситуация завершина')
                flows.remove(flow)
        print('timer')
        sleep(60)


def get_ip():
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode("utf-8")