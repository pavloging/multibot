from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = [
    [KeyboardButton(text="Да")],
    [KeyboardButton(text="Нет")]
]
kb_answer_yes_no = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


kb = [
    [KeyboardButton(text="Нет")]
]
kb_answer_no = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


kb = [
    [KeyboardButton(text="1")],
    [KeyboardButton(text="2")],
    [KeyboardButton(text="3")],
    [KeyboardButton(text="4")],
    [KeyboardButton(text="5")]
]
kb_answer_value = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


kb = [
    [KeyboardButton(text="Завершить")],
    [KeyboardButton(text="Вернуться к списку")]
]
kb_complete_or_replay = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


kb = [
    [KeyboardButton(text="Дневники сопровождения")],
    [KeyboardButton(text="Информация о клинике")]
]
kb_main = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


kb = [
    [KeyboardButton(text="Запись на прием")]
]
kb_make_appointment = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


kb = [
    [KeyboardButton(text="Вернуться в главное меню")]
]
kb_back_main = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


# b1 = KeyboardButton("Да")
# b2 = KeyboardButton("Нет")
# kb_answer_yes_no = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Ваш ответ:")
# kb_answer_yes_no.row(b1, b2)

# b1 = KeyboardButton("Нет")
# kb_answer_no = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Ваш ответ:")
# kb_answer_no.row(b1)

# b1 = KeyboardButton("1")
# b2 = KeyboardButton("2")
# b3 = KeyboardButton("3")
# b4 = KeyboardButton("4")
# b5 = KeyboardButton("5")
# kb_answer_value = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Ваш ответ:")
# kb_answer_value.row(b1, b2, b3, b4, b5)


# b1 = KeyboardButton('Завершить')
# b2 = KeyboardButton('Вернуться к списку')
# kb_complete_or_replay = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Что делаем?")
# kb_complete_or_replay.row(b1, b2)

# b1 = KeyboardButton('Дневники сопровождения')
# b2 = KeyboardButton('Информация о клинике')
# kb_main = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Куда направимся?")
# kb_main.row(b1, b2)

# b1 = KeyboardButton('Запись на прием')
# kb_make_appointment = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Назначить встречу?")
# kb_make_appointment.row(b1)

# b1 = KeyboardButton('Вернуться в главное меню')
# kb_back_main = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Возвращаемся?")
# kb_back_main.row(b1)
