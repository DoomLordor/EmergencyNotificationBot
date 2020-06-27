def new_user(connect, user_id):
    cursor = connect.cursor()
    cursor.execute("INSERT INTO client(telegram_id, home_place, stud_place, work_place) VALUES (%s, %s, %s, %s)",
                   (user_id, '', '', ''))
    connect.commit()
    cursor.close()


def set_address(connect, user_id, type_address, address):
    cursor = connect.cursor()
    request = f"UPDATE client SET {type_address}_place = %s WHERE telegram_id = %s"
    if type(user_id) is int:
        user_id = str(user_id)
    cursor.execute(request, (address, user_id))
    connect.commit()
    cursor.close()


def get_user(connect, address):
    cursor = connect.cursor()
    cursor.execute("SELECT telegram_id FROM client WHERE home_place = %s or stud_place = %s or work_place = %s",
                   (address, address, address))
    rows = cursor.fetchall()
    cursor.close()
    return [r[0] for r in rows]


def get_all_user(connect):
    cursor = connect.cursor()
    cursor.execute("SELECT telegram_id FROM client")
    rows = cursor.fetchall()
    cursor.close()
    return [r[0] for r in rows]
