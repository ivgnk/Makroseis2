"""
Модельная функция для тестирования алгоритма минимизации

(C) 2021 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""
# ptest_alg

import numpy as np
import numba
import codecs
import random
import pfunct
import pathlib
import copy
import geogr_distance
from pinp_struct import *
from math import *


def calc_dist_onsurf(latP: float, lonP:float, lat_arr:np.ndarray, lon_arr:np.ndarray) -> np.ndarray:
    n = len(lat_arr)
    distarr = np.random.random(n)
    for i in range(n):
        r = geogr_distance.calc_geogr_dist(latP, lonP, lat_arr[i], lon_arr[i])
        distarr[i] = r
    return distarr


def calc_second_stage(base_dict_: dict) -> (np.ndarray, float, float, float, int, np.ndarray, np.ndarray, np.ndarray):  # -> (float, float, float, float, int, list):
    step_ = 0.1  # шаг изменения для глубин и магнитуд
    ndep = round((base_dict_['max_dep'] - base_dict_['min_dep'])/step_ + 1)
    nmag = round((base_dict_['max_mag'] - base_dict_['min_mag'])/step_ + 1)
    the_arr = pinp_struct.dat_struct[pinp_struct.curr_nstruct, 1]
    n = len(the_arr)
    lat_arr = the_arr[:, 0]
    lon_arr = the_arr[:, 1]
    alt_arr = the_arr[:, 2]/1000
    ifact_arr = the_arr[:, 3]
    dist_onsurf = calc_dist_onsurf(base_dict_['ini_lat'], base_dict_['ini_lon'], lat_arr, lon_arr)
    dist_onsurf2 = dist_onsurf*dist_onsurf
    res_matr = np.zeros((ndep, nmag), dtype=float)
    arr_dep = np.zeros(ndep*nmag, dtype=float)
    arr_mag = np.zeros(ndep*nmag, dtype=float)
    res_matr_lin = np.zeros(ndep*nmag, dtype=float)
    min_sum = 1e308; dep_ = -13.0; mag_ = -13.0; curr_i:int = 0
    for i in range(ndep):
        curr_dep = base_dict_['min_dep']+i*step_
        for j in range(nmag):
            curr_mag = base_dict_['min_mag']+j*step_
            ssum = 0.0
            for k in range(n):
                dist = sqrt(dist_onsurf2[k] + (alt_arr[k]+curr_dep)**2)
                imod = makroseis_fun(base_dict_['a'], base_dict_['b'], base_dict_['c'], dist, curr_mag, pinp_struct.type_of_macro_fun)
                ssum = ssum + (imod-ifact_arr[k])**2
            res_matr[i, j] = ssum
            res_matr_lin[curr_i] = ssum
            arr_dep[curr_i] = curr_dep
            arr_mag[curr_i] = curr_mag
            curr_i = curr_i +1
            if ssum < min_sum:
                min_sum = ssum
                dep_ = curr_dep
                mag_ = curr_mag
    return res_matr, min_sum, dep_, mag_, curr_i, arr_dep, arr_mag, res_matr_lin
    # return res_lat, res_lon, res_dep, res_mag, nres_, res_list_

def create_2stage_dict(base_dict_: dict, res_list: list, res_choice_n: int) -> dict:
    """
    Создание словаря для inf-файла второй стадии минимизации
    """
    llist = res_list[res_choice_n]
    lat = round(llist[0], 5)
    lon = round(llist[1], 5)
    # print(lat, ' ', lon)
    base_dict = copy.deepcopy(base_dict_)
    base_dict['finf_name_'] = 'st2_'+base_dict['finf_name_']
    base_dict['name_sq'] = base_dict['name_sq']+' 2 стадия'
    base_dict['ini_lat'] = lat; base_dict['ini_lon'] = lon
    base_dict['min_lat'] = lat; base_dict['min_lon'] = lon
    base_dict['max_lat'] = lat; base_dict['max_lon'] = lon
    # print(base_dict['work_dir'])
    base_dict["full_finf_name_"] = "\\".join([base_dict["work_dir"], base_dict["finf_name_"]])
    # print(base_dict["full_finf_name_"])

    base_dict['min_mag'] =  round(base_dict['min_mag'], 1)
    base_dict['max_mag'] =  round(base_dict['max_mag'], 1)
    base_dict['min_dep'] =  round(base_dict['min_dep'], 1)
    base_dict['max_dep'] =  round(base_dict['max_dep'], 1)
    if abs(base_dict['min_mag']) < 1e-8:  base_dict['min_mag'] = 0.1
    if abs(base_dict['min_dep']) < 1e-8:  base_dict['min_dep'] = 0.1

    return base_dict


def create_test_dict(name_sq_: str, fdat_nam_: str, wrk_dr: str, finf_nm: str):
    # заготовка для inf-файла
    test_dict = empty_inf_dict
    test_dict['name_sq'] = name_sq_  # 'Тестовая площадь на основе Новозаречного'
    test_dict['fdat_name_'] = fdat_nam_  # 'test.txt'
    test_dict['a'] = a_def;  test_dict['b'] = b_def;  test_dict['c'] = c_def
    test_dict['min_mag'] = 0.001;    test_dict['max_mag'] = 9.999
    test_dict['min_lat'] = 53.0;     test_dict['max_lat'] = 58.0
    test_dict['min_lon'] = 53.0;     test_dict['max_lon'] = 58.0
    test_dict['min_dep'] = min_dep;  test_dict['max_dep'] = 30
    test_dict['work_dir'] = wrk_dr
    test_dict['finf_name_'] = finf_nm
    test_dict['full_finf_name_'] = "\\".join([test_dict["work_dir"], test_dict["finf_name_"]])
    test_dict['npoint'] = 15*15  # 15*15

    test_dict['ini_mag'] = 8
    test_dict['ini_dep'] = 9  # км

    return test_dict


def create_grid_param(test_dict_) -> (int, int, int, float, float):
    n = test_dict_['npoint']
    nx_lon = round(sqrt(n))
    ny_lat = nx_lon
    step_lon = (test_dict_['max_lon'] - test_dict_['min_lon'])/(nx_lon-1)
    step_lat = (test_dict_['max_lat'] - test_dict_['min_lat'])/(ny_lat-1)
    return n, nx_lon, ny_lat, step_lon, step_lat


def create_point_list1(test_dict_, n_zeml) -> (float, float, list):
    """
    создание глобального списка точек равномерно распределеного по карте
    n_zeml - число очагов
    n_max_zeml - номер максимального очага
    Выходные параметры: широта и долгота точки начального приближения
    """
    point_list = []  # список точек "гипоцентров" - (координаты, магнитуда, глубина)
    def_mgn = test_dict_['ini_mag']  # магнитуда по умолчанию
    def_dep = test_dict_['ini_dep']  # км, глубины очагов
    # print('n_zeml = ', n_zeml)
    # dm_max_zeml = 1.2  # во сколько раз магнитуда в максимальном очаге больше, чем в остальных
    # dm_max_magn = def_mgn*dm_max_zeml
    ini_lat = 0;     ini_lon = 0  # чтобы не было предупреждений IDE
    if n_zeml == 1:
        # точка в центре карты
        lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/2
        lon = test_dict_['min_lon'] + (test_dict_['max_lon'] - test_dict_['min_lon'])/2
        # print(lat, lon, def_dep, dm_max_magn)
        point_list.append((lat, lon, def_dep, def_mgn))
        # нач.прибл. = центр-верх
        ini_lat = test_dict_['max_lat']
        ini_lon = test_dict_['max_lon']

    elif n_zeml == 2:
        # 2 точки по диагональным углам карты
        lat = test_dict_['max_lat']
        lon = test_dict_['max_lon']
        point_list.append((lat, lon, def_dep, 9))

        lat = test_dict_['min_lat']
        lon = test_dict_['min_lon']
        point_list.append((lat, lon, def_dep, 3))
        # нач.прибл. = центр-центр
        ini_lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/2
        ini_lon = test_dict_['min_lon'] + (test_dict_['max_lon'] - test_dict_['min_lon'])/2

    elif n_zeml == 3:
        # две точки по углам треугольника
        lat = test_dict_['min_lat']
        lon = test_dict_['min_lon']
        point_list.append((lat, lon, def_dep*2, 4))

        lat = test_dict_['min_lat']
        lon = test_dict_['max_lon']
        point_list.append((lat, lon, def_dep*2, 4))
        # 1 точка в середине верха
        lat = test_dict_['max_lat']
        lon = test_dict_['min_lon'] + (test_dict_['max_lon']-test_dict_['min_lon'])/2
        point_list.append((lat, lon, def_dep, 9))
        # нач.прибл. = центр-центр
        ini_lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/2
        ini_lon = test_dict_['min_lon'] + (test_dict_['max_lon'] - test_dict_['min_lon'])/2

    elif n_zeml == 4:
        lat = test_dict_['min_lat']
        lon = test_dict_['min_lon']
        point_list.append((lat, lon, def_dep*2, 4))

        lat = test_dict_['max_lat']
        lon = test_dict_['min_lon']
        point_list.append((lat, lon, def_dep*2, 4))

        lat = test_dict_['min_lat']
        lon = test_dict_['max_lon']
        point_list.append((lat, lon, def_dep*2, 4))

        lat = test_dict_['max_lat']
        lon = test_dict_['max_lon']
        point_list.append((lat, lon, def_dep, 10))
        # нач.прибл. = центр-центр
        ini_lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/2
        ini_lon = test_dict_['min_lon'] + (test_dict_['max_lon'] - test_dict_['min_lon'])/2
    return ini_lat, ini_lon, point_list

def calc_test_grid_write_txt(test_dict_, full_txt_fname: str, point_list: list, noise: int, is_view: bool = False) -> (np.ndarray, np.ndarray, np.ndarray, str):
    """
    расчет на прямоугольной сетке значений I_mod и их суммирование
    """
    a = test_dict_["a"]
    b = test_dict_["b"]
    c = test_dict_["c"]
    alt = 0.0   # высота
    di = 1.0
    dn = 2
    rand_list = [-1, 0, 1]
    random.seed(noise)
    # print(noise)
    (n, nx_lon, ny_lat, step_lon, step_lat) = create_grid_param(test_dict_)
    lat_arr = np.random.random(n)
    lon_arr = np.random.random(n)
    imd_arr = np.random.random(n)
    n_hypo = len(point_list)  # print(n_hypo)
    f = open(full_txt_fname, mode = 'w')
    f.write('{0:13s} {1:9s} {2:6s} {3:9s} {4:9s} {5:6s} {6:7s}\n'.format('Lat', 'Lon', 'Alt', 'I_fact', 'dI', 'N', 'Нас.пункт'))
    add_str = ''
    icurr = 0
    for i in range(nx_lon):
        lon_g = test_dict_['min_lon'] + i*step_lon
        if is_view: print('lon_g=', lon_g)
        for j in range(ny_lat):
            lat_g = test_dict_['min_lat'] + j*step_lat
            if is_view: print('lat_g=', lat_g)
            sum_i = 0.0
            for k in range(n_hypo):  # по гипоцентрам
                (lat, lon, dep, mgn) = point_list[k]
                if is_view: print('k=', k, 'dep=', dep, 'mgn=', mgn)

#  def calc_distance(lat_arr: float, lon_arr: float, h_arr: float, lat: float, lon: float, dep: float) -> float:
                dist3 = calc_distance(lat_g, lon_g, alt, lat, lon, dep)
                i_curr_mod = makroseis_fun(a=a, b=b, c=c, dist=dist3, mag=mgn, type_of_macro_fun_=type_of_macro_fun)
                i_curr_mod = i_curr_mod if i_curr_mod > 0 else 0
                if is_view: print(lat_g, lon_g, alt, lat, lon, dist3, i_curr_mod)
                sum_i = sum_i + i_curr_mod
                        # lat_g,   lon_g,    alt,   sum_i,     di,    dn,   sss
            n_point_s = 'n' + str(icurr).rjust(3, '0')
            n_point_s = n_point_s.rjust(11, ' ')
            the_rand = (noise/100)*(random.random()/2)*random.choice(rand_list)
            the_sum_i = sum_i * (1 + the_rand)
            lat_arr[icurr] = lat_g; lon_arr[icurr] = lon_g; imd_arr[icurr] = the_sum_i
            if is_view: print(sum_i)
            f.write('{0:9.4f} {1:9.4f} {2:5.1f} {3:11.4f} {4:6.1f} {5:7d} {6:s}\n'.format(lat_g, lon_g, alt, the_sum_i, di, dn, n_point_s))
            icurr += 1
    f.close()
    return lat_arr, lon_arr, imd_arr, add_str


def cnv2str(*args) -> str:
    s = ''
    for num in args:
        s += str(num)+' '
    return s


def write_inf(test_dict_, full_inf_name: str, lat_ini: float, lon_ini: float):
    f = open(full_inf_name, mode='w', encoding='utf-8')
    f.write(test_dict_['name_sq']+' ; название площади'+'\n')
    f.write(test_dict_['fdat_name_'] + ' ; файл данных'+'\n')
    s = cnv2str(test_dict_['a'], test_dict_['b'], test_dict_['c']) + '; коэффициенты a, b, c макросейсмического уравнения'+'\n'
    f.write(s)  # cp1251
    f.write(cnv2str(test_dict_['min_mag'], test_dict_['max_mag']) + '; минимальная и максимальная магнитуда'+'\n')
    f.write(cnv2str(test_dict_['min_lat'], test_dict_['max_lat']) + '; минимальная и максимальная широта, десятичные градусы'+'\n')
    f.write(cnv2str(test_dict_['min_lon'], test_dict_['max_lon']) + '; минимальная и максимальная долгота, десятичные градусы'+'\n')
    f.write(cnv2str(test_dict_['min_dep'], test_dict_['max_dep']) + '; минимальная и максимальная глубина, км'+'\n')
    f.write(cnv2str(lat_ini, lon_ini) + '; начальное приближение для минимизации: широта, долгота или число - среднее по скольки широтам и долготам n-точек с максимальной I_fact'+'\n')
    f.write(cnv2str(test_dict_['ini_mag'], test_dict_['ini_dep']) + '; начальное приближение для минимизации: магнитуда, глубина, км'+'\n')
    f.close()

    with open(full_inf_name) as fh:
        data = fh.read()

    with open(full_inf_name, 'wb') as fh:
        fh.write(data.encode('cp1251'))

def write_inf2(the_dict):
    f = open(the_dict['full_finf_name_'], mode='w', encoding='utf-8')
    f.write(the_dict['name_sq']+' ; название площади'+'\n')
    f.write(the_dict['fdat_name_'] + ' ; файл данных'+'\n')
    s = cnv2str(the_dict['a'], the_dict['b'], the_dict['c']) + '; коэффициенты a, b, c макросейсмического уравнения'+'\n'
    f.write(s)  # cp1251
    f.write(cnv2str(the_dict['min_mag'], the_dict['max_mag']) + '; минимальная и максимальная магнитуда'+'\n')
    f.write(cnv2str(the_dict['min_lat'], the_dict['max_lat']) + '; минимальная и максимальная широта, десятичные градусы'+'\n')
    f.write(cnv2str(the_dict['min_lon'], the_dict['max_lon']) + '; минимальная и максимальная долгота, десятичные градусы'+'\n')
    f.write(cnv2str(the_dict['min_dep'], the_dict['max_dep']) + '; минимальная и максимальная глубина, км'+'\n')
    f.write(cnv2str(the_dict['ini_lat'], the_dict['ini_lon']) + '; начальное приближение для минимизации: широта, долгота или число - среднее по скольки широтам и долготам n-точек с максимальной I_fact'+'\n')
    f.write(cnv2str(the_dict['ini_mag'], the_dict['ini_dep']) + '; начальное приближение для минимизации: магнитуда, глубина, км'+'\n')
    f.close()

    with open(the_dict['full_finf_name_']) as fh:
        data = fh.read()

    with open(the_dict['full_finf_name_'], 'wb') as fh:
        fh.write(data.encode('cp1251'))

def create_test1(curr_dat_dir: str, nequake: int, noise: int) -> (np.ndarray, np.ndarray, np.ndarray, float, float, str):
    """
    создание тестового набора с распределенными точками
    nequake - число землерясений, noise - уровень шума в % (от исходных данных)
    Выходные данные - векторы X, Y, Z для карты и точка начального приближения
    """
    name_sq = "_".join(['test1', str(nequake), str(noise)])
    short_fname_inf = "".join([name_sq, '.inf'])
    full_fname_inf  = "\\".join([curr_dat_dir, short_fname_inf])
    short_fname_txt = "".join([name_sq, '.txt'])
    full_fname_txt  = "\\".join([curr_dat_dir, short_fname_txt])
    test_dict_ = create_test_dict(name_sq_=name_sq, fdat_nam_=short_fname_txt,
                                  wrk_dr=curr_dat_dir, finf_nm=short_fname_inf)

    ini_lat, ini_lon, point_list_ = create_point_list1(test_dict_, n_zeml=nequake)
    add_str = create_add_str(point_list_, nequake, noise)
    test_dict_['name_sq'] = test_dict_['name_sq'] + add_str
    write_inf(test_dict_, full_fname_inf, ini_lat, ini_lon)
    (lat_, lon_, ifact_, add_str2) = calc_test_grid_write_txt(test_dict_=test_dict_, full_txt_fname=full_fname_txt, point_list=point_list_, noise=noise)
    return lat_, lon_, ifact_, ini_lat, ini_lon, add_str

# --- Для второго тестирования
def create_test2(curr_dat_dir: str, nequake: int, noise: int, name: str,  test_dict_: dict,
                 numpy_arr_: np.ndarray) -> (np.ndarray, np.ndarray, np.ndarray, float, float, str, dict):
    """
    создание тестового набора с распределенными точками
    nequake - число землерясений, noise - уровень шума в % (от исходных данных), name - имя inf-файла на основе которого делаем
    Выходные данные - векторы X, Y, Z для карты и точка начального приближения
    """
    name_sq = "_".join([name, str(nequake), str(noise)])
    short_fname_inf = "".join([name_sq, '.inf'])
    full_fname_inf  = "\\".join([curr_dat_dir, short_fname_inf])
    short_fname_txt = "".join([name_sq, '.txt'])
    full_fname_txt  = "\\".join([curr_dat_dir, short_fname_txt])
    ini_lat, ini_lon, point_list_, max_dep_, max_mag_ = create_point_list2(test_dict_, n_zeml=nequake)
    # print('short_fname_txt=', short_fname_txt)

    test_dict_['max_dep'] = max_dep_
    test_dict_['max_mag'] = max_mag_

    test_dict_['fdat_name_'] = short_fname_txt
    test_dict_['name_sq'] = test_dict_['name_sq'] + create_add_str(point_list_, nequake, noise)
    write_inf(test_dict_, full_fname_inf, ini_lat, ini_lon)
    (lat_, lon_, ifact_, add_str) = calc_test2_grid_write_txt(test_dict_=test_dict_, full_txt_fname=full_fname_txt,
                                                              point_list=point_list_, noise=noise, numpy_arr=numpy_arr_)
    return lat_, lon_, ifact_, ini_lat, ini_lon, add_str, test_dict_

def create_add_str(point_list: list, nequake:int, noise:int) -> str:
    # Добавка к имени участка - глубина и магнитуда тестового примера
    s = ''
    if len(point_list) == 1:
        (lat, lon, dep, mgn) = point_list[0]
        s = '  d='+str(dep)+', m='+str(mgn)+', s='+str(nequake)+', n='+str(noise)
    else:
        flist = find_maxn2_inlist(point_list, 3, 2, [-13, -13])
        mag = flist[0]
        dep = flist[1]
        s = ' max{d='+str(dep)+', m='+str(mag)+'}, s=' + str(nequake) + ', n=' + str(noise)
    return s


def create_point_list2(test_dict_, n_zeml) -> (float, float, list, float, float):
    """
    создание глобального списка точек равномерно распределеного по карте
    n_zeml - число очагов
    n_max_zeml - номер максимального очага
    Выходные параметры:
    широта и долгота точки начального приближения,
    список землетрясений с параметрами
    ограничение по макс. глубине, ограничение по макс. магнитуде
    """
    point_list = []  # список точек "гипоцентров" - (координаты, магнитуда, глубина)
    def_mgn = 7  # test_dict_['ini_mag']  # магнитуда по умолчанию
    def_dep = 9.5  # test_dict_['ini_dep']  # км, глубины очагов
    # print('n_zeml = ', n_zeml)
    # dm_max_zeml = 1.2  # во сколько раз магнитуда в максимальном очаге больше, чем в остальных
    # dm_max_magn = def_mgn*dm_max_zeml
    ini_lat = 0;     ini_lon = 0  # чтобы не было предупреждений IDE
    max_dep_ = 14
    max_mag_ = 10

    if n_zeml == 1:
        # точка в центре карты
        lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/3
        lon = test_dict_['min_lon'] + (test_dict_['max_lon'] - test_dict_['min_lon'])/3
        # print(lat, lon, def_dep, dm_max_magn)
        point_list.append((lat, lon, def_dep, def_mgn))
        # нач.прибл.
        ini_lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/5
        ini_lon = test_dict_['max_lon'] - (test_dict_['max_lon'] - test_dict_['min_lon'])/7

    elif n_zeml == 2:
        # 2 точки
        lat = test_dict_['max_lat'] - (test_dict_['max_lat'] - test_dict_['min_lat'])/7
        lon = test_dict_['max_lon'] - (test_dict_['max_lon'] - test_dict_['min_lon'])/7
        point_list.append((lat, lon, def_dep, 9))

        lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/7
        lon = test_dict_['min_lon'] + (test_dict_['max_lon'] - test_dict_['min_lon'])/7
        point_list.append((lat, lon, def_dep*2, 3))
        # нач.прибл.
        ini_lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/4
        ini_lon = test_dict_['max_lon'] - (test_dict_['max_lon'] - test_dict_['min_lon'])/6

    elif n_zeml == 3:
        # две точки по углам треугольника
        lat = test_dict_['min_lat']
        lon = test_dict_['min_lon']
        point_list.append((lat, lon, def_dep*2, 4))

        lat = test_dict_['min_lat']
        lon = test_dict_['max_lon']
        point_list.append((lat, lon, def_dep*2, 4))
        # 1 точка в справа
        lat = test_dict_['min_lat']
        lon = test_dict_['max_lon'] + (test_dict_['max_lon']-test_dict_['min_lon'])/2
        point_list.append((lat, lon, def_dep, 9))
        # нач.прибл.
        ini_lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/4
        ini_lon = test_dict_['max_lon'] - (test_dict_['max_lon'] - test_dict_['min_lon'])/6

    elif n_zeml == 4:
        lat = test_dict_['min_lat']   # +
        lon = test_dict_['min_lon']
        point_list.append((lat, lon, def_dep, 10))

        lat = test_dict_['min_lat']
        lon = test_dict_['max_lon']  # +
        point_list.append((lat, lon, def_dep*2, 4))

        lat = test_dict_['max_lat']  # +
        lon = test_dict_['min_lon']
        point_list.append((lat, lon, def_dep*2, 4))

        lat = test_dict_['max_lat'] - (test_dict_['max_lat'] - test_dict_['min_lat'])/3
        lon = test_dict_['max_lon'] - (test_dict_['max_lon'] - test_dict_['min_lon'])/3
        point_list.append((lat, lon, def_dep*2, 4))
        # нач.прибл.
        ini_lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/4
        ini_lon = test_dict_['max_lon'] - (test_dict_['max_lon'] - test_dict_['min_lon'])/6
    return ini_lat, ini_lon, point_list, max_dep_, max_mag_


def calc_test2_grid_write_txt(test_dict_, full_txt_fname: str, point_list: list, noise: int,
                              numpy_arr: np.ndarray, is_view: bool = False) -> (np.ndarray, np.ndarray, np.ndarray, str):
    """
    расчет на прямоугольной сетке значений I_mod и их суммирование
    """
    a = test_dict_["a"]
    b = test_dict_["b"]
    c = test_dict_["c"]
    di = 1.0
    dn = 2
    rand_list = [-1, 0, 1]
    random.seed(noise)
    # print(noise)
    n = len(numpy_arr);  n_hypo = len(point_list) # print(n_hypo)
    lat_arr = np.random.random(n)
    lon_arr = np.random.random(n)
    imd_arr = np.random.random(n)

    f = open(full_txt_fname, mode='w')
    f.write('{0:13s} {1:9s} {2:6s} {3:9s} {4:9s} {5:6s} {6:7s}\n'.format('Lat', 'Lon', 'Alt', 'I_fact', 'dI', 'N', 'Нас.пункт'))
    add_str = ''
    icurr = 0
    for i in range(n):
        lat_g = numpy_arr[i, 0]
        lon_g = numpy_arr[i, 1]
        alt = numpy_arr[i, 2]/1000
        if is_view:                                                        # нас.пункт
            print(i, ' ', 'lat_g=', lat_g, 'lon_g=', lon_g, 'alt =', alt,  numpy_arr[i, 6])
        sum_i = 0.0
        for k in range(n_hypo):  # по гипоцентрам
            (lat, lon, dep, mgn) = point_list[k]
            if is_view: print('k=', k, 'dep=', dep, 'mgn=', mgn)
#  def calc_distance(lat_arr: float, lon_arr: float, h_arr: float, lat: float, lon: float, dep: float) -> float:
            dist3 = calc_distance(lat_g, lon_g, alt, lat, lon, dep)
            i_curr_mod = makroseis_fun(a=a, b=b, c=c, dist=dist3, mag=mgn, type_of_macro_fun_=type_of_macro_fun)
            i_curr_mod = i_curr_mod if i_curr_mod>0 else 0
            if is_view: print(lat_g, lon_g, alt, lat, lon, dist3, i_curr_mod)
            sum_i = sum_i + i_curr_mod
                        # lat_g,   lon_g,    alt,   sum_i,     di,    dn,   sss
        n_point_s = numpy_arr[i, 6]
        n_point_s = n_point_s.rjust(23, ' ')
        the_rand = (noise/100)*(random.random()/2)*random.choice(rand_list)
        the_sum_i = sum_i * (1 + the_rand)
        lat_arr[icurr] = lat_g; lon_arr[icurr] = lon_g; imd_arr[icurr] = the_sum_i
        f.write('{0:9.4f} {1:9.4f} {2:8.1f} {3:8.4f} {4:6.1f} {5:7d} {6:s}\n'.format(lat_g, lon_g, alt*1000, the_sum_i,
                                                                                      di, dn, n_point_s))
        icurr += 1
    f.close()
    return lat_arr, lon_arr, imd_arr, add_str
