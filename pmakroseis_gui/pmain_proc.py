"""
Макросейсмика, 2020,
главный модуль
"""
# pmain_proc

import numpy as np
from geogr_distance import *
from pinp_proc import *

# from pinp_struct import *
import pinp_struct

from pnumpy import *
import math
import numba
from scipy.optimize import minimize
import copy
import openpyxl
# from psort import *
# from pfit import *
from tkinter import messagebox as mb
from ptkinter_menu_proc import *

log_file_name: str
gran = 0.001  # 0.001% изменения функции по абсолютной величине
# для analyze_diff, порог для max_var/max_fun, возможные уровни срабатывания 1, 10, 20, 100, 400


def main_proc(is_view1: bool) -> None:
    global log_file_name
    if test_mode:
        if is_view1:
            print('тестовый режим')                # txt_input работает, когда inf_input = False
        (file_name, log_file_name) = prepare_input_filename(inf_input=True, txt_input=True, is_view=is_view1)
        if is_view1:
            print(file_name, log_file_name)
        good_end = the_input(file_name, is_view1)
        if not good_end:
            print('Ошибка в данных, программа расчеты не выполняла')
        work_with_data(is_view1)

    print('Нормальное завершение')


def work_with_data(is_view1: bool) -> (bool, int, float, float, float, float, float, list):
    """
    Подготовка к работе и минимизация
    bool
    """
    row: int; i: int;

    if is_view1: print('work_with_data')
    (the_dict, the_arr) = pinp_struct.get_dat_struct(pinp_struct.curr_nstruct)
    row = the_dict["npoint"]
    lat_arr = the_arr[:, 0]  # Lat
    # print('lat_arr ', np.size(lat_arr)); print(lat_arr)
    lon_arr = the_arr[:, 1]  # Lat
    # print('lon_arr ', np.size(lon_arr)); print(lon_arr)
    h_arr = the_arr[:, 2]/1000  # Alt переводим в км
    # print('h_arr ', np.size(h_arr)); print(h_arr)
    i_fact_arr = the_arr[:, 3]
    npoint = np.size(i_fact_arr)
    eqval = (row == npoint)
    # print('i_fact_arr ', np.size(i_fact_arr)); print(i_fact_arr)
    if not eqval:
        # заглушка для данных
        num, lat_, lon_, dep_, mag_, fun_ = -13, -13, -13, -13, -13, -13,
    else:
        (num, lat_, lon_, dep_, mag_, fun_, res_list_) = minimize_func(npoint, lat_arr, lon_arr, h_arr, i_fact_arr)
    return eqval, num, lat_, lon_, dep_, mag_, fun_, res_list_
    # view_2d_array(dat, nrow: int, ncol: int, test_info='Просмотр в work_with_data '):


def calc_diff(iii: int, x0: float, x1: float, x2: float, x3: float, f: float, result_list: list) -> \
                                                        (float, float, float, float, float, float):
                                                        # dx0    dx1   dx2    dx3,   df,    gran
    if iii == 0:
        return math.nan, math.nan, math.nan, math.nan, math.nan, math.nan
    else:
        n = 100
        dat = result_list[iii-1]
        dx0 = ((x0 - dat[0])/dat[0])*n  # lat_ = x0[0]
        dx1 = ((x1 - dat[1])/dat[1])*n  # lon_ = x0[1]
        dx2 = ((x2 - dat[2])/dat[2])*n  # dep_ = x0[2]
        dx3 = ((x3 - dat[3])/dat[3])*n  # mag_ = x0[3]
        df  = ((f  - dat[4])/dat[4])*n  # f = x0[4]
        dgran_ = get_diffgran(dx0, dx1, dx2, dx3, df)
        return (dx0, dx1, dx2, dx3, df, dgran_)


def get_diffgran(dx0: float, dx1: float, dx2: float, dx3: float, df: float) -> float:
    # max_dvar = abs(max(dx0, dx1, dx2, dx3))
    max_dvar = max(abs(dx0), abs(dx1), abs(dx2), abs(dx3))
    max_dfun = abs(df)
    # max_dvar/max_dfun - числа не более 1, 10, 40 - как бы "линейная" зависимость
    # max_dfun/max_dvar - как бы парабола, ветви вверх, аппроксимируем, находим индекс минимума
    # как бы 2-3 минимума, но они после больших значений, так что реагировать будут на первый
    return max_dvar/max_dfun


def analyze_diff(iii: int, result_list: list) -> bool:
    """
    Определяет как быстро меняется самая вариабельная переменная относительно изменения функции
    Если более gran, то return True / иначе return False
    """
    global gran
    if iii != 0:   # 5    6     7   8     9
        dat = result_list[iii]
        # max_var = max(abs(dat[5]), abs(dat[6]), abs(dat[7]), abs(dat[8]))
        max_fun = abs(dat[9])
        # d = max_var/max_fun  # как быстро меняется самая вариабельная переменная относительно изменения функции
        d = max_fun  # как быстро меняется целевая функция
        # print('max_var/max_fun = %7.5f' %  d)
        if d > gran:  # если  - числа не более 1, 10, 40 - как бы "линейная" зависимость
            # print('d > gran')
            return True
        else:
            return False


def output_txt_res(fname: str, result_list: list) -> None:
    """
    Неполный вариант по выводим данным, полный см. output_xls_res
    Вывод в txt файл итераций минимизации:
    номер, lat, lon, dep, mag, fun
    """
    fff = open(fname,  mode='w')  # открытие log-файла
    llen = len(result_list)
    fff.write('{0:6s} {1:9s} {2:9s} {3:9s} {4:9s} {5:11s} {6:9s} {7:9s} {8:9s} {9:9s} {10:11s} {11:11s}\n'.format('N', 'Lat', 'Lon', 'Dep', 'Mag', 'Fun', 'dLat,%', 'dLon,%', 'dDep,%', 'dMag,%', 'dFun,%', 'max_var,%/dFun,%'))
    for i in range(llen):
        d = result_list[i]
        fff.write('{0:5d} {1:9.5f} {2:9.5f} {3:9.5f} {4:9.5f} {5:11.5f} {6:9.5f} {7:9.5f} {8:9.5f} {9:9.5f}  {10:11.5f} {11:11.5f}\n'.format(i, d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10]))
    fff.close()


def output_xls_res(fname: str, result_list: list) -> None:
    """
    Вывод в xlsx файл итераций минимизации:
    номер, lat, lon, dep, mag, fun, dLat %, dLon %, dDep %, dMag %, dFun %
    """
    # Чтение и запись в файл Excel с использованием модуля Python openpyxl
    # https://pythononline.ru/question/chtenie-i-zapis-v-fayl-excel-s-ispolzovaniem-modulya-python-openpyxl
    my_wb = openpyxl.Workbook()
    my_sheet = my_wb.active
    my_sheet.title = "Результаты"
    llen = len(result_list)
    my_sheet.cell(row=1, column= 1).value = 'i'
    my_sheet.cell(row=1, column= 2).value = 'Lat'
    my_sheet.cell(row=1, column= 3).value = 'Lon'
    my_sheet.cell(row=1, column= 4).value = 'Dep'
    my_sheet.cell(row=1, column= 5).value = 'Mag'
    my_sheet.cell(row=1, column= 6).value = 'Fun'
    my_sheet.cell(row=1, column= 7).value = 'dLat, %'
    my_sheet.cell(row=1, column= 8).value = 'dLon, %'
    my_sheet.cell(row=1, column= 9).value = 'dDep, %'
    my_sheet.cell(row=1, column=10).value = 'dMag, %'
    my_sheet.cell(row=1, column=11).value = 'dFun, %'
    my_sheet.cell(row=1, column=12).value = 'max_var,%/dFun,%'
    for i in range(llen):
        d = result_list[i]
        rrow = i + 2
        my_sheet.cell(row=rrow, column=1).value = i  # i
        my_sheet.cell(row=rrow, column=2).value = d[0]  # Lat
        my_sheet.cell(row=rrow, column=3).value = d[1]  # Lon
        my_sheet.cell(row=rrow, column=4).value = d[2]  # Dep
        my_sheet.cell(row=rrow, column=5).value = d[3]  # Mag
        my_sheet.cell(row=rrow, column=6).value = d[4]  # Fun
        if rrow > 2:
            my_sheet.cell(row=rrow, column= 7).value = d[5]  # dLat
            my_sheet.cell(row=rrow, column= 8).value = d[6]  # dLon
            my_sheet.cell(row=rrow, column= 9).value = d[7]  # dDep
            my_sheet.cell(row=rrow, column=10).value = d[8]  # dMag
            my_sheet.cell(row=rrow, column=11).value = d[9]  # dFun
            my_sheet.cell(row=rrow, column=12).value = d[10]  # max(dvar)/dFun

    my_wb.save(fname)

                                         # num, lat_,  lon_,  dep_,  mag_,  fun_
def get_true_result(result_list: list) -> (int, float, float, float, float, float):
    """
    Выборка из result_list
    """
    global gran
    llen = len(result_list)
    # print('llen =', llen)
    num = 0
    for i in range(1, llen):
        d = result_list[i]
        if abs(d[9]) < gran:
            num = i
            break

    d = result_list[num]
    lat_ = d[0]  # Lat
    lon_ = d[1]  # Lon
    dep_ = d[2]  # Dep
    mag_ = d[3]  # Mag
    fun_ = d[4]  # Fun

    return num, lat_,  lon_,  dep_,  mag_,  fun_


# @numba.njit
def minimize_func(n: int, lat_arr: np.ndarray, lon_arr: np.ndarray,
                           h_Arr: np.ndarray, i_fact_arr: np.ndarray) -> (int, float, float, float, float, float, list):
    global log_file_name
    a: float; b: float; c: float
    str_res_: str
    f1: float
    proc_f: float  # процент изменения f на каждой итерации
    iii: int = 0
    result_list: list= []

    def main_objective_function(x0) -> float:
        nonlocal iii
        nonlocal result_list
        f1 = pinp_struct.objective_function(n, lat_arr, lon_arr, h_Arr, i_fact_arr, x0[0], x0[1], x0[2], x0[3], a, b, c)

        # вычисление доп.параметров для останова приращений переменных и функции и dgran_ - спец.итоговой функции
        (dx0, dx1, dx2, dx3, df, dgran_) = calc_diff(iii, x0[0], x0[1], x0[2], x0[3], f1, result_list)
        result_list.append([x0[0], x0[1], x0[2], x0[3], f1,
                              dx0, dx1,   dx2,   dx3,  df, dgran_])
        # print('%5d lat_ %10.6f =   lon_ =  %10.6f   dep_ = %10.6f   mag_ = %10.6f   f = %10.6f' % (iii, x0[0], x0[1], x0[2], x0[3], f1))
        # print('      dlat_ = %10.6f  dlon_ =  %10.6f  ddep_ = %10.6f  dmag_ = %10.6f  df = %10.6f' % (dx0, dx1, dx2, dx3, df))
        # print('           %10.6f            %10.6f           %10.6f          %10.6f       %10.6f' % (dx0, dx1, dx2, dx3, df))
        iii += 1
        return f1

    # scipy.optimize.minimize
    # If callback returns True the algorithm execution is terminated
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html
    # Python3.4 scipy.optimize.minimize callbacks multiple times the objective function in one iteration
    # https://stackoverflow.com/questions/32477371/python3-4-scipy-optimize-minimize-callbacks-multiple-times-the-objective-functio
    def call_back_f(Xi) -> bool:
        nonlocal iii
        nonlocal result_list

        res_analyz: bool = analyze_diff(iii-1, result_list)
        return res_analyz

    (a, b, c) = pinp_struct.get_a_b_c(pinp_struct.curr_nstruct)
    (ini_lat_, ini_lon_, ini_dep_, ini_mag_) = pinp_struct.get_ini(pinp_struct.curr_nstruct)
    #               x0[0]      x0[1]     x0[2]     x0[3]
    x0 = np.array([ini_lat_, ini_lon_, ini_dep_, ini_mag_])
    # print('x0 = ', x0);   sys.exit()
    f = main_objective_function
    # res = minimize(f, x0, method='nelder-mead', tol=1e-10,
    #                options={'maxiter': 80000, 'xatol': 0.00001, 'fatol': 1e-12, 'adaptive': True})
    # res = minimize(f, x0, method='nelder-mead', tol=1e-10)

    res = minimize(f, x0, method='nelder-mead', callback=call_back_f)
    # res = minimize(f, x0, method='nelder-mead', options={'maxiter': 8000,'fatol': 0.01, 'adaptive': True})

    # вывод всей последовательности точек минимизации в файл
    # [если истина] if [выражение] else [если ложь]
    if pinp_struct.is_txt_res_file:
        output_txt_res(log_file_name, result_list)
    else:
        output_xls_res(log_file_name, result_list)

    # print('Начальные значения')
    # print('ini_lat_ = %7.3f' % ini_lat_)
    # print('ini_lon_ = %7.3f' % ini_lon_)

    # print('Результат автоматический')
    # print('res.x', res.x)
    # print('lat = res.x[0] = %8.5f' % res.x[0])
    # print('lon = res.x[1] = %8.5f' % res.x[1])
    # print('dep = res.x[2] = %8.5f' % res.x[2])
    # print('mag = res.x[3] = %8.5f' % res.x[3])
    # print('res.success = ', res.success)  # bool - Whether or not the optimizer exited successfully.
    # print('res.message = ', res.message)  # str - Description of the cause of the termination.
    # print('res.fun = ', res.fun)  # fun - Values of objective function
    # print('res.nfev = ', res.nfev, ' main_objective_function, число вычислений')      # Number of evaluations of the objective functions
    # print('res.nit = ', res.nit)      # int - Number of iterations performed by the optimizer
    # print(f.__name__+' = ', f(res.x))  # main_objective_function

    (num, lat_, lon_, dep_, mag_, fun_) = get_true_result(result_list)

    return num, lat_, lon_, dep_, mag_, fun_, result_list

def create_str_res(ini_lat_, ini_lon_, num, lat_, lon_, dep_, mag_, fun_) -> str:
    as_ = ' '*5
    str_res_ = '\n'
    str_res_ += as_+'        Начальное приближение\n'
    str_res_ += as_+'     Широта = '+format(ini_lat_,'7.3f') + '\n'
    str_res_ += as_+'    Долгота = '+format(ini_lon_,'7.3f') + '\n' + '\n'

    str_res_ += as_+'        Выбраный результат минимизации' + '\n'
    str_res_ += as_+'   Итерация (строка в файле результата) = ' + format(num,'>4d') + '\n'
    str_res_ += as_+'       Широта = '+format(lat_,'7.3f') + '\n'
    str_res_ += as_+'      Долгота = '+format(lon_,'7.3f') + '\n'
    str_res_ += as_+'      Глубина = '+format(dep_,'7.3f') + '\n'
    str_res_ += as_+'    Магнитуда = '+format(mag_,'7.3f') + '\n'
    str_res_ += as_+' Значение целевой функции = '+format(fun_,'7.3f') + '\n'
    return str_res_


def add_info():
    lat_ = 55.92745139505674;  lon_ = 57.33186006061451; dep_ = 29.999999999999993; mag_ = 5.723468511118773
    print('N результата 1731')
    # N1731 res.fun =  44.16925687182368
    result_control(lat_, lon_, dep_, mag_)

    print('N  результата 35')
    # N35 res.fun = 46.196595366820034
    lat_ = 55.860328095037005; lon_  = 57.002550801519476;  dep_ = 10.062189981696722;  mag = 5.612690867989407
    result_control(lat_, lon_, dep_, mag_)

    print('N  результата 51')
    # N51 res.fun = 44.99874411859368
    lat_ = 55.84245014011909;  lon_ = 57.22878737017246;  dep_ = 10.172387821353635; mag_ = 5.699159301892644
    result_control(lat_, lon_, dep_, mag_)
