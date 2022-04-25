import os
import time

import cv2
import telebot
from telebot import types
import random

from handDetect import HandDetector

bot = telebot.TeleBot('5210518096:AAHhjFYxST8JaHDuP5AZbv-YWPw9ptiDsfA')


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id, 'Привет!')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Хиромантия")
    btn2 = types.KeyboardButton("❓ Карты ТАРО")
    btn3 = types.KeyboardButton("❓ ҚҰМАЛАҚ")
    markup.add(btn1).add(btn2).add(btn3)
    # keyboard = types.InlineKeyboardMarkup()
    # # По очереди готовим текст и обработчик для каждого знака зодиака
    # key_kumalak = types.InlineKeyboardButton(text='ҚҰМАЛАҚ', callback_data='kumalak')
    # # И добавляем кнопку на экран
    # keyboard.add(key_kumalak)
    # key_cards_taro = types.InlineKeyboardButton(text='Карты ТАРО', callback_data='cards_taro')
    # keyboard.add(key_cards_taro)
    # key_chiromancy = types.InlineKeyboardButton(text='Хиромантия', callback_data='chiromancy')
    # keyboard.add(key_chiromancy)
    bot.send_message(message.from_user.id, text='Способ гадание', reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     msg = ''
#     if call.data == "chiromancy":
#         msg = 'Сфотографируй левую ладонь и отправь фото'
#     elif call.data == "cards_taro":
#         msg = 'this is message for cards_taro'
#     elif call.data == "kumalak":
#         msg = 'this is message for kumalak'
#     bot.send_message(call.message.chat.id, msg)
#     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "👋 Хиромантия"):
        bot.send_message(message.chat.id, text="Сфотографируй левую ладонь и отправь фото)")
    elif (message.text == "❓ Карты ТАРО"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    elif (message.text == "❓ ҚҰМАЛАҚ"):
        bot.send_message(message.chat.id, "У меня нет имени..")


@bot.message_handler(content_types=["photo"])
def send_text(message):
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = message.chat.username + "/" + file_info.file_unique_id + ".jpg"
    isExist = os.path.exists(message.chat.username)
    if not isExist:
        os.makedirs(message.chat.username)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    image = cv2.imread('./'+file_path)
    try:
        hand_detector = HandDetector(min_detection_confidence=0.7)
        handLandmarks = hand_detector.find_hand_land_marks(image=image, draw=True)

        if (len(handLandmarks) != 0):
            rand = random.uniform(1, 100)

            r = int(rand % 3)
            msg = ""
            msg2 = ""

            if r == 0:
                msg = "Ойбай! Линия жизни короткая!!!"
                msg2 = "А, не. Просто руку помыть надо!"
            elif r == 1:
                msg = "Линия сердца просто Супер! Сразу видно, что человек Хороший!"
                msg2 = "А, не. Показалось!"
            elif r == 2:
                msg = "Линия ума глубокая как Океан! Тебе бы пойти в Науку!"
                msg2 = "А, не. В Науке мало платят!"

            bot.send_message(message.chat.id, msg)
            time.sleep(5)
            bot.send_message(message.chat.id, msg2)
        else:
            bot.send_message(message.chat.id, "Что с рукой? Мозоли?! ;)")
    except Exception as ex:
        print(ex)


bot.polling(none_stop=True, interval=0)
