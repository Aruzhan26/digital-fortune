import os
import time
import emoji
import cv2
import telebot
from telebot import types
import random

from handDetect import HandDetector

bot = telebot.TeleBot('5210518096:AAHhjFYxST8JaHDuP5AZbv-YWPw9ptiDsfA')


def get_default_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Хиромантия")
    btn2 = types.KeyboardButton("🃏 Карты ТАРО")
    btn3 = types.KeyboardButton('🫘 ҚҰМАЛАҚ')
    markup.add(btn1).add(btn2).add(btn3)
    bot.send_message(message.from_user.id, text='Выберите способ гадания', reply_markup=markup)


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id, 'Привет!')
    get_default_buttons(message)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "👋 Хиромантия":
        bot.send_message(message.chat.id, text="Сфотографируй левую ладонь и отправь фото)")
    elif message.text == "🃏 Карты ТАРО":
        send_tarot(message)
    elif message.text == "🫘 ҚҰМАЛАҚ":
        kumalak(message)
    elif message.text == "Готов!":
        kumalak_helper(message)
    else:
        bot.send_message(message.chat.id, emoji.emojize('ШТА.. :confused: мое твое не понимать', language='alias'))
        time.sleep(1)
        bot.send_message(message.chat.id, emoji.emojize(':pray: напиши "/start"', language='alias'))


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
            r = int(random.uniform(1, 100) % 3)
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
    a = int(random.uniform(1, 100) % 3)
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


def kumalak(message):
    bot.send_message(message.chat.id, "Загадай вопрос на который можно ответить да или нет!")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Готов!")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Готов?', reply_markup=markup)


def kumalak_helper(message):
    bot.send_message(message.chat.id, "Позволь бобам решить твою судьбу!")
    bot.send_message(message.chat.id, "ПЕРСТ СУДЬБЫ!")
    bot.send_document(message.chat.id, document=open('tiadalma.gif', 'rb'))
    time.sleep(3)
    bot.send_message(message.chat.id, "Бобы говорят....")
    r = int(random.uniform(1, 100) % 3)
    if r == 0:
        msg = "ДА!"
        msg2 = "НУ ИЛИ НЕТ!"
        msg3 = "ИЛИ ДА!"
        msg4 = "СПРОСИ ЗАВТРА!"
    elif r == 1:
        msg = "НЕТ!"
        msg2 = "НУ ИЛИ ДА!"
        msg3 = "ИЛИ НЕТ!"
        msg4 = "СПРОСИ ЗАВТРА!"
    elif r == 2:
        msg = "МОЖЕТ БЫТЬ!"
        msg2 = "А МОЖЕТ И НЕ БЫТЬ!"
        msg3 = "А МОЖЕТ И БЫТЬ!"
        msg4 = "СПРОСИ ЗАВТРА!"

    bot.send_message(message.chat.id, msg)
    time.sleep(3)
    bot.send_message(message.chat.id, msg2)
    time.sleep(3)
    bot.send_message(message.chat.id, msg3)
    time.sleep(3)
    bot.send_message(message.chat.id, msg4)
    get_default_buttons(message)


bot.polling(none_stop=True, interval=0)
