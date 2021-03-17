"""
Апроксимация данных, по логике близка к оптимизации/минимизации

(C) 2020 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""

from scipy.optimize import curve_fit
import numpy as np
# from scipy.optimize import curve_fit

def f_parabola(x, a, b, c):
    return a + b*x + c*x*x

def test_curve_fit():
    x = np.arange(1, 382)
    print(x)
    y = np.loadtxt(r'E:\Work_Lang\Python\PyCharm\Makroseis\Dat\test.txt')
    print(y)
    if len(x) == len(y):
        popt, pcov = curve_fit(f_parabola, x, y)
        print('Результаты curve_fit \n')
        print(popt)
    else:
        print('массивы разной длины')
    z =  f_parabola(x, popt[0], popt[1], popt[2])
    # print('Аппроксимированная кривая \n');  print(z)
    print('np.argmin = ',np.argmin(z))
    # минимальные индексы в numpy
    # https://pyprog.pro/sort/argmin.html
    # https://askdev.ru/q/kak-vernut-vse-minimalnye-indeksy-v-numpy-138837/

def curve_fit_parabola(x: np.ndarray, y: np.ndarray) -> (float, float, float, int):
    """
    Подгонка данных параболой
    """
    popt, pcov = curve_fit(f_parabola, x, y)
    z = f_parabola(x, popt[0], popt[1], popt[2])
    ind:int = np.argmin(z)
    return popt[0], popt[1], popt[2], ind

def test_curve_fit_parabola():
    a = 8;  b = -6; c = 1;
    n = 20
    x:np.ndarray = np.arange(n); print(x)
    y:np.ndarray = f_parabola(x, a, b, c)
    print(y)
    a1, b1, c1, ind = curve_fit_parabola(x,y)
    print('Результаты = \n', a1, b1, c1, ind, y[ind])
# test_curve_fit()


# test_curve_fit_parabola()
