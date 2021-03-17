"""
# -------------------------------------------------------------------
# Функции сортировок
#
# (C) 2020 Ivan Genik, Perm, Russia
# Released under GNU Public License (GPL)
# email igenik@rambler.ru
# -------------------------------------------------------------------
"""
import numpy as np
import random

def test_struct_numpyarr_sort() -> None:
    """
    сортировка структурированного массива numpy
    numpy.sort - https://pyprog.pro/sort/sort.html
    numpy.append - https://pyprog.pro/array_manipulation/append.html
    https://pyprog.pro/array_manipulation/vstack.html
    """
    data_type = [('name', 'U13'), ('age', int),
                  ('weight', float), ('height', float)]
             #    name    age   weight    height
    person = [('Василий', 18,    57.1,    1.96),
              ('Петр'   , 25,    94.9,    1.51),
              ('Семен'  , 30,    72.5,    1.83),
              ('Антон'  , 30,   146.8,    1.76)]
    person2 = [('Сергей',  8,    36.1,    1.36)]
    dat = np.array(person, dtype=data_type)
    print('Исходные данные');  print(dat)

    dat2 = np.array(person2, dtype=data_type)
    dat = np.append(dat, dat2)
    print('\nИсходные + Добавленные данные');  print(dat)

    print('\nСортировка - sort(dat, order = weight)')
    print(np.sort(dat, order = 'weight') )

    print('нормальное завершение')


def create_2dlist_1(row_: int, col_: int) -> list:
    """
    Создание 2 мерного списка
    https://foxford.ru/wiki/informatika/mnogomernye-spiski-v-python
    """
    A = [0] * row_
    for i in range(row_):
        A[i] = [0] * col_
    return A


def create_2dlist_2(row_: int, col_: int) -> list:
    """
    Создание 2 мерного списка
    https://foxford.ru/wiki/informatika/mnogomernye-spiski-v-python
    """
    A = []
    for i in range(row_):
        A.append([0] * col_)
    return A


def create_2dlist_3(row_: int, col_: int) -> list:
    """
    Создание 2 мерного списка
    https://foxford.ru/wiki/informatika/mnogomernye-spiski-v-python
    """
    A = [[0] * col_ for i in range(row_)]
    return A


def copy_numpy_2dlist(np1:np.ndarray, np2:np.ndarray, llist:list) -> list:
    """
    2 одномерных массива одинаковой длины копируются
    в список с тем же числом строк и числом столбцов = 2
    """
    for i in range(len(llist)):
        llist[i][0] = np1[i]
        llist[i][1] = np2[i]
    return llist

def copy_2dlist_numpy(llist:list, ncol_:int) -> np.ndarray:
    dat:np.ndarray
    llen = len(llist)
    # dat = np.ndarray(llist)
    llist2 = llist[:,ncol_]
    return 0

def sortByDat2(dat):
    """
    Для сортировки двумерного  списка по 2 элементу
    """
    return dat[1]

def sortByDat11(dat):
    """
    Для сортировки двумерного  списка по 2 элементу
    """
    return dat[10]

def test_list() -> None:
    nrow = 5
    ncol = 6
    llist:list = create_2dlist_1(nrow, ncol)
    print(llist)
    for i in range(nrow):
        for j in range(ncol):
            llist[i][j] = j
    print(llist)

def test_list2D_sort() -> None:
    """
    сортировка двумерного списка по 2 элементу
    NumPy, часть 3: random    https://pythonworld.ru/numpy/3.html
    Многомерные списки в Python https://foxford.ru/wiki/informatika/mnogomernye-spiski-v-python
    Python: сортировка списков методом .sort() с ключом — простыми словами https://habr.com/ru/post/138535/
    """
    the_list: list = [[],[]]

    nrow_ = 10
    random.seed()
    dat1int = np.arange(nrow_);
    print('Массив целых чисел = \n',dat1int)

    # dat2float = np.arange(1.1, 9.9, 1.1);   print(dat2float)

    dat2float_random = np.random.uniform(size=nrow_);
    print('Массив случайных действительных чисел = \n', dat2float_random)

    # Первый вариант создания списка
    # the_list[0] = dat1int
    # the_list[1] = dat2float_random
    # print(type(the_list[0]), type(the_list[1]))
    # print(the_list)

    the_list = create_2dlist_3(nrow_, 2)
    print('Список = \n', the_list)
    print('Длина списка = ',len(the_list))

    print('Список после заполнения = \n', the_list)
    the_list = copy_numpy_2dlist(dat1int, dat2float_random, the_list)
    print(the_list)

    # Python: сортировка списков методом .sort() с ключом — простыми словами
    # https://habr.com/ru/post/138535/
    newList = sorted(the_list, key=sortByDat2)
    print('\n Сортировка двумерного списка по 2 элементу \n',newList)


# test_struct_numpyarr_sort()
# test_list2D_sort()
# test_list()