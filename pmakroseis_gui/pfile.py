"""
Дополнительные фунцкии для работы с файлами

(C) 2020 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""

import os
import time
import pathlib

def text_file_num_lines(fname:str) -> int:
    """
    Определяет число строк в текстовом файле
    Небольшие файлы не более нескольких тысяч строк
    https://askdev.ru/q/kak-podschitat-obschee-kolichestvo-strok-v-tekstovom-fayle-s-pomoschyu-python-147949/
    """

    with open(fname) as f:
         myList = [line.split() for line in f]
    f.close()
    return len(myList)

    # f = open(fname, 'r')
    # i = 1;     line = f.readline();   print(line);
    # while line:
    #     line = f.readline();
    #     # line = line.rstrip('\n')
    #     print(line)
    #     i = i+1

    # f = open(fname,'r')
    #    i = i + 1
    #    print(i, line)

    # f = open(fname,'r')
    # return len(f.readlines())

    # f = open(fname, 'r')
    # i:int =0
    # for line in f:
    #     i=i+1
    # return i


def get_datfile_time(fname: str, thetest: bool = False) -> str:
    """
    Вывод времени создания файла
    2018 Python 3 – Время. Метод strftime()
    https://andreyex.ru/yazyk-programmirovaniya-python/uchebnik-po-python-3/python-3-vremya-metod-strftime/
    """
    beauty_time: float = os.path.getmtime(fname)
    if thetest: print(os.path.getmtime(fname))
    beauty_time1: str = time.strftime("%d/%m/%y : %H:%M:%S", time.localtime(beauty_time))  # gmtime
    print('Время файла = ', beauty_time1)
    if thetest: print('type(beauty_time) = ', type(beauty_time1))
    return beauty_time1

def gfn(filename:str) ->str: # выделить только имя файла в нижнем регистре, исключая точку
    # https://python-scripts.com/pathlib
    # full_name = os.path.basename(filename)
    # name = os.path.splitext(full_name)[0]
    # return name.lower()

    # https://python-scripts.com/pathlib
    s = pathlib.Path(filename).stem
    return s.lower()


def gfe(filename:str) ->str: # выделить расширение файла в нижнем регистре, включая точку
    # Pathlib — манипуляция путями, создание и удаление папок и файлов
    # https://python-scripts.com/pathlib
    # https://all-python.ru/osnovy/put-imya-i-rasshirenie-fajla.html
    s = pathlib.Path(filename).suffix
    return s.lower()

def name_and_ext(name:str, extension:str) -> str: # объединение имени и расширения
    return "\\".join([name, extension])

# Проверка работы функций
# print(gfe(r'E:\Work_Lang\Python\PyCharm\Makroseis\Dat\.точки_ввод.txt'))
# print(gfe(r'E:\Work_Lang\Python\PyCharm\Makroseis\Dat\.точки_ввод.XLSX'))
# print(gfe(r'E:\Work_Lang\Python\PyCharm\Makroseis\Dat\.точки_ввод.Xlsx'))
# print(gfn(r'E:\Work_Lang\Python\PyCharm\Makroseis\Dat\точки_ввод.Xlsx'))

