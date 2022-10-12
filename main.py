import string
import telebot
import random
import requests
import time
from bs4 import BeautifulSoup
import pymysql
from elevate import elevate
from os import walk
from db_config import db_host, db_user, db_password, db_name
import consts
import file_serv

bot = telebot.TeleBot('5751774597:AAG7-vFSojHUZfQNcvkVf1fvYLdGeFKfSgg')
elevate() # даем боту права администратора windows/linux/macos


def generate_personal_code(length):
    random.seed()
    letters = string.ascii_lowercase + string.ascii_uppercase
    pers_code = ''.join(random.choice(letters) for i in range(length))
    return pers_code


def connect_to_db():
    try:
        connection = pymysql.connect(
            host=db_host,
            port=3306,
            user=db_user,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor)
        print('zaebis')
        print('#' * 20)
        return connection
    except Exception as ex:
        print('Connection pizdec')
        print(ex)


def new_user_db(user_id, username):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            insert_query = 'INSERT INTO `user_data` (chat_id, username) VALUES' \
                   f'( \'{user_id}\', \'{username}\');'
            cursor.execute(insert_query)
            connection.commit()
    finally:
        connection.close()


def check_personal_code(pers_code):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            check_query1 = f'SELECT count(*) FROM file_bot_db.regs WHERE personal_code = \'{pers_code}\';'
            cursor.execute(check_query1)
            data = cursor.fetchall()
            # check_query2 = f'SELECT login FROM file_bot_db.regs WHERE personal_code = \'{pers_code}\';'
            # cursor.execute(check_query2)
    finally:
        # data = cursor.fetchall()
        connection.close()
        if int(data[0]["count(*)"]) != 0:
            return True


def new_reg_db(login, password):
    connection = connect_to_db()
    pers_code = generate_personal_code(25)
    try:
        with connection.cursor() as cursor:
            insert_query = 'INSERT INTO `regs` (login, password, personal_code) VALUES' \
                   f'( \'{login}\', \'{password}\', \'{pers_code}\');'
            cursor.execute(insert_query)
            connection.commit()
    finally:
        file_serv.make_new_dir(pers_code)
        connection.close()


def log_in_db(login_check, password_check):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            try:
                select_pers_code = f"SELECT personal_code FROM `regs` WHERE login = \'{login_check}\' and " \
                 f"password = \'{password_check}\'"
                cursor.execute(select_pers_code)
                data = cursor.fetchall()
                for data_temp in data:
                    print(data_temp["personal_code"])
            except Exception as ex:
                print('Problems with '
                      'chat\n')
                print(ex)
    finally:
        connection.close()
        print(data)
        return data_temp["personal_code"]


def alert_users(alert_text):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            select_chat_id = "SELECT chat_id, username FROM `user_data`"
            cursor.execute(select_chat_id)
            data = cursor.fetchall()
            for data_temp in data:
                try:
                    vid = open('pirozkov.mp4', 'rb')
                    bot.send_video(int(data_temp["chat_id"]), vid)
                except Exception as ex:
                    print('Problems with chat\n')
                    print(ex)
    finally:
        connection.close()


def inmenu(message):
    bot.send_message(message.chat.id, '<b>Выход в меню: /menu</b>', parse_mode='html')


@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id, consts.start_menu, parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message):
    new_user_db(message.chat.id, message.from_user.username)
    visitors1 = open('visitors.txt', 'a')
    visitors1.write(f'К нам зашёл {message.from_user.username} в {time.ctime(message.date)}\n\n')
    visitors1.close()
    bot.send_message(message.chat.id, f'Привет, <b><u>{message.from_user.username}</u></b>!', parse_mode='html')
    bot.send_message(message.chat.id, consts.start_menu, parse_mode='html')


@bot.message_handler(commands=['visitors'])
def visitors(message):
    visitor = open('visitors.txt', 'r')
    bot.send_message(message.chat.id, f'{visitor.read()}')


@bot.message_handler(commands=['admin_alert'])
def admin_alert(message):
    mes = "Как дела"
    alert_users(mes)


@bot.message_handler(commands=['admin_tools'])
def admin_tools(message):
    bot.send_message(message.chat.id, consts.admin_tool_menu, parse_mode='html')


@bot.message_handler(commands=['sign_up'])
def sign_up(message):
    bot.send_message(message.chat.id, '<b>Введите ваш новый логин (Количество символов 6-20):</b>', parse_mode='html')
    bot.register_next_step_handler(message, get_new_login)


def get_new_login(message):
    temp_login = message.text
    if len(temp_login) > 20:
        bot.send_message(message.chat.id, '<b>Слишком длинный логин</b>', parse_mode='html')
    elif len(temp_login) < 6:
        bot.send_message(message.chat.id, '<b>Слишком короткий логин</b>', parse_mode='html')
    else:
        print(temp_login)
        bot.send_message(message.chat.id, '<b>Введите пароль (Количество символов 6-20):</b>', parse_mode='html')
        bot.register_next_step_handler(message, get_new_password, temp_login)


def get_new_password(message, temp_login):
    temp_password = message.text
    if len(temp_password) > 20:
        bot.send_message(message.chat.id, '<b>Слишком длинный пароль</b>', parse_mode='html')
    elif len(temp_password) < 6:
        bot.send_message(message.chat.id, '<b>Слишком короткий пароль</b>', parse_mode='html')
    else:
        print(temp_password)
        new_reg_db(temp_login, temp_password)
        bot.send_message(message.chat.id, '<b>Теперь вы можете <u>войти</u>:\n/log_in</b>', parse_mode='html')


@bot.message_handler(commands=['log_in'])
def log_in(message):
    bot.send_message(message.chat.id, '<b>Введите ваш логин:</b>', parse_mode='html')
    bot.register_next_step_handler(message, get_login)


def get_login(message):
    temp_login = message.text
    print(temp_login)
    bot.send_message(message.chat.id, '<b>Введите пароль:</b>', parse_mode='html')
    bot.register_next_step_handler(message, get_password, temp_login)


def get_password(message, temp_login):
    temp_password = message.text
    print(temp_password)
    your_code = log_in_db(temp_login, temp_password)
    bot.send_message(message.chat.id, 'Ваш персональный код доступа:', parse_mode='html')
    bot.send_message(message.chat.id, f'<b>{your_code}</b>', parse_mode='html')
    bot.send_message(message.chat.id, 'Не забудьте скопировать его!\nТеперь вы можете <b>подключиться к серверу!</b>\n\n/menu', parse_mode='html')


@bot.message_handler(commands=['send_file'])
def connect_server_send(message):
    bot.send_message(message.chat.id, '<b>Для подключения к серверу, введите ваш персональный код:</b>', parse_mode='html')
    bot.register_next_step_handler(message, get_personal_code_send)


def get_personal_code_send(message):
    temp_pers_code = message.text
    print(temp_pers_code)
    if check_personal_code(temp_pers_code):
        bot.send_message(message.chat.id, f'<b>Успешное подключение к серверу!</b>',
                         parse_mode='html')
        bot.send_message(message.chat.id, f'<b>Можете присылать свой файл:</b>',
                         parse_mode='html')
        bot.register_next_step_handler(message, serv_get_file, temp_pers_code)
    else:
        bot.send_message(message.chat.id, f'<b>Персональный код не существует</b>',
                         parse_mode='html')
        inmenu(message)


def serv_get_file(message, pers_code):
    print(message)
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_serv.save_new_file(downloaded_file, message.document.file_name, pers_code)
    elif message.content_type == 'photo':
        file_info = bot.get_file(message.chat.photo['file_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        file_serv.save_new_file(downloaded_file, message.photo[1].file_name, pers_code)
    elif message.content_type == 'audio':
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_serv.save_new_file(downloaded_file, message.audio.file_name, pers_code)
    elif message.content_type == 'video':
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_serv.save_new_file(downloaded_file, message.video.file_name, pers_code)
    else:
        bot.send_message(message.chat.id, f'<b>{message.content_type}</b>',
                         parse_mode='html')
        bot.send_message(message.chat.id, f'<b>Вы не отправили файл/фото</b>',
                         parse_mode='html')
        inmenu(message)
        return
    bot.send_message(message.chat.id, f'<b>Хорошо, я сохраню твой файл!</b>', parse_mode='html')
    inmenu(message)


@bot.message_handler(commands=['receive_file'])
def connect_server_receive(message):
    bot.send_message(message.chat.id, '<b>Для подключения к серверу, введите ваш персональный код:</b>', parse_mode='html')
    bot.register_next_step_handler(message, get_personal_code_receive)


def get_personal_code_receive(message):
    temp_pers_code = message.text
    print(temp_pers_code)
    if check_personal_code(temp_pers_code):
        bot.send_message(message.chat.id, f'<b>Успешное подключение к серверу!</b>',
                         parse_mode='html')

        bot.send_message(message.chat.id, f'<b>Список ваших файлов:</b>',
                         parse_mode='html')

        for root, dirs, files in walk(f"D:\\bot_dirs\\{temp_pers_code}"):
            for filename in files:
                bot.send_message(message.chat.id, f'{filename}\n')
        bot.send_message(message.chat.id, f'<b>Отправьте название скачеваемого файла:</b>',
                         parse_mode='html')
        bot.register_next_step_handler(message, serv_send_file, temp_pers_code)
    else:
        bot.send_message(message.chat.id, f'<b>Персональный код не существует</b>',
                         parse_mode='html')
        inmenu(message)


def serv_send_file(message, code):
    name_file = message.text
    try:
        bot.send_document(message.chat.id, file_serv.serv_receive(code, name_file))
        inmenu(message)
    except Exception as ex:
        bot.send_message(message.chat.id, f'<b>Файл не существует!</b>',
                         parse_mode='html')
        print(ex)


bot.infinity_polling(timeout=10, long_polling_timeout=5)
