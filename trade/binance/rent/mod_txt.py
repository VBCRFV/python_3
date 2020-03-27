#!python3
# -*- coding: utf-8 -*-
__version__ = 20191107
""" Модуль функций обработки текстовых файлов.
20191023
    Стартовая версия.
20191107
    text_write()
        Добавлены параметры: mode, encoding.
"""
def file_exists(path):
    import os.path
    return os.path.exists(path)

def text_read(file_name):
    f = open(file_name)
    file = f.read()
    f.close()
    return file

def text_write(file_name,text,mode='w',encoding='utf8'):
    f = open(file_name, mode, encoding=encoding)
    f.write(str(text))
    f.close()

def json_write(file_name,data):
    """
    записать данные data(list, dict) , в текстовый файл file_name.
    (тип datatime, преобразовывать к строке до процедуры.)
    :param file_name: Имя файла.
    :param data: переменноя хранящая данные типа list и\или dict.
    :return: None
    """
    import json
    f = open(file_name, 'w')
    data = json.dumps(data)
    f.write(data)
    f.close()

def json_read(file_name):
    """
    прочитать переменную(list, dict) из файла file_name.
    :param file_name: имя текстового файла из которого читаем данные.
    :return: данные преобразованые к типу list и\или dict.
    """
    import json
    f = open(file_name)
    data = f.read()
    f.close()
    data = json.loads(data)
    return data

def json_write_item(file_name, item, el=None):
    '''
    запесать(добавить\земенить) пару ключ-значение item в файле file_name
    :return:
    '''
    data = json_read(file_name)
    if el is not None:
        data[el].update(item)
    else:
        data.update(item)
    json_write(file_name, data)

if __name__ == '__main__':
    pass

