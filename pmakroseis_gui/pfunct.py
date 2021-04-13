# -------------------------------------------------------------------
# Разные функции общего назначения
#
# (C) 2020 Ivan Genik, Perm, Russia
# Released under GNU Public License (GPL)
# email igenik@rambler.ru
# -------------------------------------------------------------------

import math
import numpy as np
from functools import reduce

def list2d3_to_3nparray(ll:list) -> (np.ndarray, np.ndarray, np.ndarray):
    llen = len(ll)
    x = np.random.random(llen)
    y = np.random.random(llen)
    z = np.random.random(llen)
    for i in range(llen):
        d = ll[i]
        x[i] = d[0]
        y[i] = d[1]
        z[i] = d[2]
    return x, y, z


def out_of_diap2(dat, dat_min, dat_max) -> (float, float):
    """
    Расчет выхода за диапазон - абсолютные и относительные значения (доли 1)
    """
    llen = dat_max-dat_min
    if dat_min > dat:
        d = dat_min - dat
        return d, d/llen
    if dat_max < dat:
        d = dat - dat_max
        return d, d/llen


def out_of_diap1proc(dat, dat_min, dat_max) -> float:
    """
    Расчет выхода за диапазон - относительные значения (доли 1)
    """
    llen = dat_max-dat_min
    if dat_min > dat:
        d = dat_min - dat
        return d/llen
    if dat_max < dat:
        d = dat - dat_max
        return d/llen


def out_of_diap2proc(dat, dat_min, dat_max) -> float:
    """
    Расчет выхода за диапазон - абсолютные и относительные значения (доли 1)
    Вычисления в логарифмическом масштабе
    """
    dat_minln = math.log10(dat_min)  # print(dat_min)
    dat_maxln = math.log10(dat_max)
    if dat < 0:
        dat_ln = -10
    else:
        dat_ln = math.log10(dat)

    llen = dat_maxln-dat_minln
    d = 0
    if dat_minln > dat_ln:
        d = dat_minln - dat_ln
    if dat_maxln < dat_ln:
        d = dat_ln - dat_max
    # print(d/llen)
    return abs(d/llen)


def dat_in_diap(dat, dat_min, dat_max) -> bool:
    return (dat_min <= dat) and (dat <= dat_max)


def dat2_in_diap(dat1, dat2, dat_min, dat_max, isview: bool = False) -> bool:
    if isview:
        print(dat1, dat2, dat_min, dat_max)
    return (dat_min <= dat1) and (dat1 <= dat_max) and (dat_min <= dat2) and (dat2 <= dat_max)

# ============ Работа с двумерными списками
def find_maxn_inlist(dlist: list, npos: int, reduce_init:float):
    # поиск в двумерном списке чисел
    n = npos
    def mmax(x, y):
        nonlocal n
        #  print('x=',x)
        #  print('y=',y)
        if x > y[n]:
            return x
        else:
            return y[n]
    return reduce(mmax, dlist, reduce_init)

def find_maxn2_inlist(dlist: list, npos: int, nposextr: int, reduce_init:list):
    # поиск в двумерном списке чисел и сохраение списка:
    # наибольшее и указаннон
    n = npos
    nextr = nposextr
    def mmax(x, y):
        nonlocal n
        nonlocal nextr
        #  print('x=',x)
        #  print('y=',y)
        if x[0] > y[n]:
            return x
        else:
            return [y[n], y[nextr]]

    return reduce(mmax, dlist, reduce_init)


# ============  Тестирование
def create_2d_nparray_r1c2(row, col, dat00=0.0, dat01=0.0) -> object:
    a = np.zeros((row, col), dtype=object)
    a[0, 0] = dat00
    a[0, 1] = dat01
    return a


def add_2d_nparray(nparr1, dat00, dat01) -> object:
    # Функции numpy.hstack() и numpy.vstack()
    # https://pythonist.ru/funkczii-numpy-hstack-i-numpy-vstack/
    nparr2 = create_2d_nparray_r1c2(1, 2, dat00, dat01)
    return np.vstack((nparr1, nparr2))

# def test_2d_nparray() -> None:
#     nparr = create_2d_nparray_r1c2(1,2)
#     print(nparr, end='\n\n')
#     nparr = add_2d_nparray(nparr, 10, 20)
#     print(nparr)
# print(dat2_in_diap(0.001, 9.999, 0.0, 10.0, isview=True))
# print(dat2_in_diap(float('nan'), float('nan'), float('nan'), float('nan'), isview=True))
# test_2d_nparray()
# print_format_examples()
