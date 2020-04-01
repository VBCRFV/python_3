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
print(json_read('settings.txt'))
json_write_item('settings.txt',{'whait':600})
print(json_read('settings.txt'))
json_write_item('settings.txt',{'whait':500})
print(json_read('settings.txt'))