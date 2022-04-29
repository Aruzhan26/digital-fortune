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
    btn4 = types.KeyboardButton("🃏 Карты ТАРО v2")
    markup.add(btn1).add(btn2).add(btn3).add(btn4)
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
    if message.text == "👋 Хиромантия":
        bot.send_message(message.chat.id, text="Сфотографируй левую ладонь и отправь фото)")
    elif message.text == "❓ Карты ТАРО":
        send_tarot(message)
    elif message.text == "❓ ҚҰМАЛАҚ":
        bot.send_message(message.chat.id, "У меня нет имени..")
    elif message.text == "🃏 Карты ТАРО v2":
        send_tarot_v2(message)


@bot.message_handler(content_types=["photo"])
def send_text(message):
    print('message.photo =', message.photo)
    file_id = message.photo[-1].file_id
    print('fileID =', file_id)
    file_info = bot.get_file(file_id)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    file_path = message.chat.username + "/" + file_info.file_unique_id + ".jpg"
    is_exist = os.path.exists(message.chat.username)
    if not is_exist:
        os.makedirs(message.chat.username)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    image = cv2.imread('./' + file_path)
    try:
        hand_detector = HandDetector(min_detection_confidence=0.7)
        hand_landmarks = hand_detector.find_hand_land_marks(image=image, draw=True)

        if len(hand_landmarks) != 0:
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


def send_tarot(message):
    a = random.randint(0, 2)
    if a == 0:
        img = 'https://www.conjunction-tarot.com/ct/wp-content/uploads/2020/10/XV_the-devil-2-998x1536.jpg'
        msg = "Дьявол предупреждает вас: будьте начеку"
        msg2 = "Пить лучше мало, но долго :)"
    elif a == 1:
        img = 'https://www.conjunction-tarot.com/ct/wp-content/uploads/2020/10/XIX_the-sun-1-998x1536.jpg'
        msg = "Солнечные лучи ярко освещают вашу тропинку: споткнуться просто не удастся!"
        msg2 = "Но, по-любому, смотри под ноги!"
    else:
        img = 'https://www.conjunction-tarot.com/ct/wp-content/uploads/2020/10/XVII_the-star-2-998x1536.jpg'
        msg = "Тебя наградят тем, что ты заслужил..."
        msg2 = "Косяков же нет?"
    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, msg)
    time.sleep(3)
    bot.send_message(message.chat.id, msg2)


def send_tarot_v2(message):
    a = random.randint(0, 2)
    if a == 0:
        img = 'https://avatars.mds.yandex.net/get-zen_doc/3418917/pub_5f0de499514fc2519cfb1933_5f0de4b70fad611164c0cd2b/scale_1200'
        img2 = 'https://s.felomena.com/wp-content/images/taro/karty/starshie/smert.jpg'
        msg = "Дьявол предупреждает вас: будьте начеку"
        msg2 = "Пить лучше мало, но долго :)"
    elif a == 1:
        img = 'https://www.oculus.ru/image/blogs/18/docs/4879_9.jpg'
        img2 = 'https://avatars.mds.yandex.net/get-zen_doc/2851998/pub_5f0df2700afa571885de17da_5f0df2806235522a11f4ecf5/scale_1200'
        msg = "Солнечные лучи ярко освещают вашу тропинку: споткнуться просто не удастся!"
        msg2 = "Но, по-любому, смотри под ноги!"
    else:
        img = 'https://avatars.mds.yandex.net/get-zen_doc/3179652/pub_5f0deca641987d594723cdf0_5f0decda34a56c6326a8dba7/scale_1200'
        img2 = 'https://avatars.mds.yandex.net/get-zen_doc/2851998/pub_5f0df2700afa571885de17da_5f0df2806235522a11f4ecf5/scale_1200'
        msg = "Тебя наградят тем, что ты заслужил..."
        msg2 = "Косяков же нет?"
    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, msg)
    time.sleep(3)
    bot.send_photo(message.chat.id, img2)
    bot.send_message(message.chat.id, msg2)


bot.polling(none_stop=True, interval=0)
