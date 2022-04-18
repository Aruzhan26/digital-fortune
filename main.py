import telebot
from telebot import types

bot = telebot.TeleBot('5210518096:AAHhjFYxST8JaHDuP5AZbv-YWPw9ptiDsfA')


@bot.message_handler(commands=['start'])
def get_text_messages(message):
    bot.send_message(message.chat.id, 'Привет!')
    keyboard = types.InlineKeyboardMarkup()
    # По очереди готовим текст и обработчик для каждого знака зодиака
    key_kumalak = types.InlineKeyboardButton(text='ҚҰМАЛАҚ', callback_data='kumalak')
    # И добавляем кнопку на экран
    keyboard.add(key_kumalak)
    key_cards_taro = types.InlineKeyboardButton(text='Карты ТАРО', callback_data='cards_taro')
    keyboard.add(key_cards_taro)
    key_chiromancy = types.InlineKeyboardButton(text='Хиромантия', callback_data='chiromancy')
    keyboard.add(key_chiromancy)
    bot.send_message(message.from_user.id, text='Способ гадание', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    msg = ''
    if call.data == "chiromancy":
        msg = 'Сфотографируй левую ладонь и отправь фото'
    elif call.data == "cards_taro":
        msg = 'this is message for cards_taro'
    elif call.data == "kumalak":
        msg = 'this is message for kumalak'
    bot.send_message(call.message.chat.id, msg)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=["photo"])
def send_text(message):
    percent = userFace.verify(message.photo, config.photoToCompare)
    bot.send_message(message.chat.id, "Percentage: " + str(percent))


bot.polling(none_stop=True, interval=0)
