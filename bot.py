i = 0
b = []


def main(bot):  # сюда писать только функции которые трубуют декоратора
    @bot.message_handler(commands=['start', 'go'])
    def start_handler(message):
        bot.send_message(message.chat.id, 'заебись')

    @bot.message_handler(content_types=['text'])
    def prp(massage):
        global i, b
        i += 1
        print(i)
        b.append(massage.chat.id)
        if i == 3:
            i = 0
            bot.send_message(b[-1], 'Сон')


def mailing(bot, text):
    v = [1011917065, 809971387]
    for val in v:
        bot.send_message(val, text)


def new_user(connect, user_id):
    cursor = connect.cursor()
    cursor.execute("INSERT INTO client(telegram_id, home_place, stud_place, work_place) VALUES (%s, %s, %s, %s)",
                   (user_id, '', '', ''))
    connect.commit()
    cursor.close()


def set_address(connect, user_id, type_address, address):
    cursor = connect.cursor()
    cursor.execute("UPDATE client SET %s_place = %s WHERE telegram_id==%s", (type_address, address, user_id))
    connect.commit()
    cursor.close()


def get_user(connect, address):
    cursor = connect.cursor()
    cursor.execute("SELECT telegram_id FROM client WHERE home_place=%s or stud_place=%s or work_place=%s",
                   (address, address, address))
    rows = cursor.fetchall()
    cursor.close()
    return rows
