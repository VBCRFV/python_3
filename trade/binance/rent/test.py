# -*- coding: utf8 -*-
from mod_txt import text_read,text_write

if __name__ == '__main__':
    txt = text_read('export.csv')
    txt = txt.replace(",",";").replace(".",",").replace("1970-01-01T08:00:01","0000-00-00 00:00:00")
    print(txt)
    text_write('export2.csv',txt,mode='w',encoding='utf8')