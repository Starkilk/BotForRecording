import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('KEY')
name = ""
dataUser = ""

@bot.message_handler(commands=['start'])
def startBot(message):

    markup = types.ReplyKeyboardMarkup()
    bAboutMe = types.KeyboardButton('Обо мне 😊')
    bContacts = types.KeyboardButton('Контакты 📱')
    markup.row(bAboutMe, bContacts)
    bPriceList = types.KeyboardButton('Прайс-лист 📋')
    bWorkExamples = types.KeyboardButton('Акции 📈')
    markup.row(bPriceList, bWorkExamples)
    bEnroll = types.KeyboardButton('Записаться ✅')
    markup.row(bEnroll)
    bot.register_next_step_handler(message, onClick)
    textHello = ("Здравствуйте! Через этого бота вы можете записаться на\nнаращивание ресниц в удобное для вас время!🙃\n\nПроцедура будет проводиться в микрорайоне 'Горбатка'\nЯ(Имя)  встречу вас по адресу 'адрес'\n"
                 "Ориентир - магазин 'название'.\nАвтобусная остановка - название.🚌")
    imageTitle = open('./template.jpg', 'rb')
    bot.send_photo(message.chat.id, imageTitle, textHello, reply_markup=markup)


@bot.message_handler(commands=['data_from_database'])
def info(message):
    connection = sqlite3.connect('clients.sql')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    inf = ""
    for i in users:
        inf += f"Имя: {i[1]}, Связь: {i[2]}, Дата: {i[3]}\n"

    cursor.close()
    connection.close()

    bot.send_message(message.chat.id,inf)
    bot.register_next_step_handler(message, onClick)

def onClick(message):
    if message.text == 'Обо мне 😊':
        imageOboMne = open('./template.jpg', 'rb')
        textOboMne = "Привет! меня зовут 'Имя', я мастер по наращиванию ресниц\nиз Твери)\nМоя цель - сделать ваш внешний вид неповторимым и\nподчеркнуть вашу естественную красоту. Я уделяю внимание\nкаждой детали и стремлюсь к безупречному выполнению своих\nуслуг.🥰 Кроме того, я придерживаюсь высоких стандартов\nгигиены и безопасности, чтобы обеспечить ваш комфортный и\nбезопасный визит.🧤\n\nЯ ценю  каждого клиента и стремлюсь создать доверительные отношения.😉"
        bot.send_photo(message.chat.id, imageOboMne, textOboMne)
        bot.register_next_step_handler(message, onClick)

    elif message.text == 'Контакты 📱':
        bot.send_message(message.chat.id, "Связь со мной и примеры работ:")
        textContscts = "Номер телефона: 8900000000\nИнстаграм: Name\nТелеграмм: https://t.me/name\nГруппа ВК: https://vk.com/name\nСтраница ВК: https://vk.com/name"
        bot.send_message(message.chat.id, textContscts)
        bot.register_next_step_handler(message, onClick)
    elif message.text == 'Прайс-лист 📋':
        imClassic = open('./template.jpg', 'rb')
        imPoltoraD = open('./template.jpg', 'rb')
        imTwoD = open('./template.jpg', 'rb')
        imTreeD = open('./template.jpg', 'rb')
        imWaterEffeckt = open('./template.jpg', 'rb')
        imLuchi = open('./template.jpg', 'rb')
        imAmerikanka = open('./template.jpg', 'rb')

        bot.send_photo(message.chat.id, imClassic, "Классика: 1000₽")
        bot.send_photo(message.chat.id, imPoltoraD, "1.5д: 1100₽")
        bot.send_photo(message.chat.id, imTwoD, "2д: 1200₽")
        bot.send_photo(message.chat.id, imTreeD, "3д: 1300₽")
        bot.send_photo(message.chat.id, imWaterEffeckt, "Мокрый эффект: 1500₽")
        bot.send_photo(message.chat.id, imLuchi, "Лучи: +100₽")
        bot.send_photo(message.chat.id, imAmerikanka, "Американка: 1400₽")

        bot.send_message(message.chat.id, "Классика: 1000₽\n1.5д: 1100₽\n2д: 1200₽\n3д: 1300₽\nМокрый эффект: 1500₽\nЛучи: +100₽\nАмериканка: 1400₽")
        bot.register_next_step_handler(message, onClick)

    elif message.text == 'Акции 📈':
        imAkciya = open('./template.jpg', 'rb')
        imAkcFriend = open('./template.jpg','rb')
        bot.send_photo(message.chat.id, imAkciya)
        bot.send_photo(message.chat.id, imAkcFriend)
        bot.register_next_step_handler(message, onClick)

    elif message.text == 'Записаться ✅':


        connection = sqlite3.connect('clients.sql')
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50),dataUser varchar(50),dateTime varchar(50))")
        connection.commit()
        cursor.close()
        connection.close()

        bot.send_message(message.chat.id, "Введите ваше имя")
        bot.register_next_step_handler(message, setName)
        bot.register_next_step_handler(message, onClick)


def setName(message):
    global name
    name = message.text.strip()
    if(name == "Обо мне 😊" or name == "Контакты 📱" or name == "Прайс-лист 📋" or name == "Акции 📈" or name == "Записаться ✅"):
        pass
    else:
        bot.send_message(message.chat.id, "Введите ваш номер телефона или ссылку на одну из соц. сетей: ВК, Телеграмм, Инстаграм. Для связи с вами.\nВнимательно проверьте правильность введённых данных!☺️")
        bot.register_next_step_handler(message, setData)

def setData(message):

    global dataUser
    dataUser = message.text.strip()
    if (dataUser == "Обо мне 😊" or dataUser == "Контакты 📱" or dataUser == "Прайс-лист 📋" or dataUser == "Акции 📈" or dataUser == "Записаться ✅"):
        bot.register_next_step_handler(message, onClick)
        pass
    else:
        imDateTime = open('./template.jpg', 'rb')
        bot.send_photo(message.chat.id, imDateTime)
        bot.send_message(message.chat.id, "Введите дату и время на которую хотите записаться\n(Например: 1ое Сентября 14:30)")
        bot.register_next_step_handler(message, setDateTime)

def setDateTime(message):
    dateTimeUser = message.text.strip()
    if (dateTimeUser == "Обо мне 😊" or dateTimeUser == "Контакты 📱" or dateTimeUser == "Прайс-лист 📋" or dateTimeUser == "Акции 📈" or dateTimeUser == "Записаться ✅"):
        bot.register_next_step_handler(message, onClick)
        pass
    else:
        connection = sqlite3.connect('clients.sql')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO users (name, dataUser, dateTime) VALUES ('%s', '%s', '%s')"%(name, dataUser, dateTimeUser))
        connection.commit()
        cursor.close()
        connection.close()

        bot.send_message(message.chat.id, f"Вы успешно записались на {dateTimeUser}.\nВ скором времени с вами свяжутся для подтверждения записи.✅")

        bot.register_next_step_handler(message, onClick)




bot.polling(none_stop=True)