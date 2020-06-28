def new_user(connect, user_id):
    cursor = connect.cursor()
    cursor.execute("INSERT INTO client(telegram_id, home_place, stud_place, work_place, "
                   "home_place_num, stud_place_num, work_place_num) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (user_id, '', '', '', '', '', ''))
    connect.commit()
    cursor.close()


def set_address(connect, user_id, type_address, address):
    address = address.split(':')
    cursor = connect.cursor()
    request = f"UPDATE client SET {type_address}_place = %s, {type_address}_place_num = %s WHERE telegram_id = %s"
    if type(user_id) is int:
        user_id = str(user_id)
    cursor.execute(request, (address[0], address[1],user_id))
    connect.commit()
    cursor.close()


def get_user_full_address(connect, address):
    address = address.split(':')
    cursor = connect.cursor()
    cursor.execute("SELECT telegram_id FROM client WHERE (home_place = %s and home_place_num = %s) "
                   "or (stud_place = %s and stud_place_num = %s) or (work_place = %s and work_place_num = %s)",
                   (address[0], address[1], address[0], address[1], address[0], address[1]))
    rows = cursor.fetchall()
    cursor.close()
    return [r[0] for r in rows]


def get_all_user(connect):
    cursor = connect.cursor()
    cursor.execute("SELECT telegram_id FROM client")
    rows = cursor.fetchall()
    cursor.close()
    return [r[0] for r in rows]
