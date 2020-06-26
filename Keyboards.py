from telebot import types

markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("/help")
item2 = types.KeyboardButton("/EXIT")
markup1.add(item1, item2)

markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("/help")
item2 = types.KeyboardButton("/numbers")
item3 = types.KeyboardButton("/edit")
item4 = types.KeyboardButton("/EXIT")
markup2.add(item1, item2, item3, item4)

markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("101")
item2 = types.KeyboardButton("102")
item3 = types.KeyboardButton("103")
item4 = types.KeyboardButton("104")
item5 = types.KeyboardButton("112")
item6 = types.KeyboardButton("/help")
markup3.add(item1, item2, item3, item4, item5, item6)

markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("/reg")
item2 = types.KeyboardButton("/EXIT")
markup4.add(item1, item2)

markup5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("/help")
item2 = types.KeyboardButton("/start")
markup5.add(item1, item2)

markup6 = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("/help")
item2 = types.KeyboardButton("/EXIT")
markup6.add(item1, item2)