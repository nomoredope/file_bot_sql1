import string
import os
import stat
# from elevate import elevate
import consts


def make_new_dir(dir_name):
    os.mkdir(f'{consts.win_set_dirs}{dir_name}', mode=stat.S_IWUSR, dir_fd=None)


def save_new_file(file_bot, file_name_bot, code):
    src = consts.win_set_dirs + code + consts.win_set_delimeter + file_name_bot
    with open(src, 'wb') as new_file:
        new_file.write(file_bot)


def show_files(code):
    for root, dirs, files in os.walk(consts.win_set_dirs + code):
        for filename in files:
            print(filename)


def serv_receive(code, name):
    f = open(consts.win_set_dirs + code + consts.win_set_delimeter + name, 'rb')
    return f
