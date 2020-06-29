import http.client
from threading import Thread
from time import time, sleep
from model.database import get_user_full_address
from TelegramBot.bot_logic import emergency_mailing, dangerous_processing, all_users_id_danger, people_danger

danger = []
flag = [True]


def dangerous_start(message, bot, connected):

    street = input('Введите улицу проишествия: ').lower()
    num = input('Введите дом проишествия: ')

    addres = f'{street}:{num}'

    users = get_user_full_address(connected, addres)

    message = f'По адресу {street.title()} {num} произошло проишествие: {message}'

    users = emergency_mailing(bot, message, users)

    time_start = time()

    for user in users:
        all_users_id_danger[user] = addres

    danger.append([Thread(target=dangerous_processing, args=(bot,), name=f'{street}:{num}'),
                   time_start, False])

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
            flag_flow = False
            name = flow[0].getName()
            if flow[1] - time() > 100:
                flag_flow = True
                print(f'По аддресу {name} время вышло')
                # Клаву пользователю нужно вернуть на стартовую
            elif not flow[2]:
                flag_flow = True
                print(f'По аддресу {name} опрос окончен')
            elif flow[3]:
                flag_flow = True
                print(f'По аддресу {name} ситуация завершина')
            if flag_flow:
                if not len(people_danger):
                    people_danger.pop(name)
                for user in all_users_id_danger:
                    if all_users_id_danger[user] == name:
                        all_users_id_danger.pop(user)
                flows.remove(flow)
        sleep(60)


def get_ip():
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode("utf-8")
