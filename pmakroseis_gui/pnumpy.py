# -------------------------------------------------------------------
# Разные функции для работы с Numpy
#
# (C) 2020 Ivan Genik, Perm, Russia
# Released under GNU Public License (GPL)
# email igenik@rambler.ru
# -------------------------------------------------------------------
import numpy as np
# import math


def test_findmax_arrindex1d():
    x = np.array([112, 1111, 13, 14, 12, 11])
    llen = len(x)
    print(x)
    # !!! https://askdev.ru/q/kak-poluchit-indeksy-n-maksimalnyh-znacheniy-v-massive-numpy-4667/
    # print(np.argpartition(x, llen-1), end = '\n\n')
    z = (-x).argsort()[:llen]
    print(type(z))
    print(round(1.2), round(0.8))


def findmax_arrindex1d(x: np.ndarray):
    """
    Находит массив индексов элементов в порядке убывания
    x - одномерный массив
    """
    llen: int = len(x)
    return (-x).argsort()[:llen]


def test_add_dat_in_ndarray():
    """
    Проверка создания "списка данных" на основе numpy
    """
    # numpy.vstack
    # https://pyprog.pro/array_manipulation/vstack.html
    arr = np.zeros(5)
    print(arr)
    for i in range(1, 10):
        zz = np.zeros(5)
        zz = zz + i
        arr = np.vstack((arr, zz))
    print(arr)


def test_add_dat_in_ndarray2():
    """
    Проверка 2 создания "списка данных" на основе numpy
    https://coderoad.ru/568962/Как-создать-пустой-массив-матрицу-в-NumPy
    """
    arr = np.empty(shape=[0, 6])
    print(arr)
    for i in range(0, 10):
        ll = [i*1, i*2, i*3, i*4, i*5, i*6]
        arr = np.append(arr, [ll], axis=0)
    print(arr)


def test_add_dat_in_list():
    """
    Проверка 2 создания списка данных
    """
    mylist = []
    for i in range(0, 10):
        mylist.append([i*1, i*2, i*3, i*4, i*5, i*6])
    print(mylist)
    print(mylist[0])
    print(mylist[1])
    # mat = numpy.array(mylist)

# test_findmax_arrindex1d()
# test_add_dat_in_list()

# https://riptutorial.com/ru/python/example/3973/бесконечность-и-nan---не-число--
# print( 100 > math.nan )
