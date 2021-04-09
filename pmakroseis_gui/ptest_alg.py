"""
Модельная функция для тестирования алгоритма минимизации

(C) 2021 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""
# ptest_alg
import numpy as np
import codecs
from pinp_struct import *
from math import *


def create_test_dict(name_sq_: str, fdat_nam_: str, wrk_dr: str, finf_nm: str):
    # заготовка для inf-файла
    test_dict = empty_inf_dict
    test_dict['name_sq'] = name_sq_  # 'Тестовая площадь на основе Новозаречного'
    test_dict['fdat_name_'] = fdat_nam_  #  'test.txt'
    test_dict['a'] = a_def;  test_dict['b'] = b_def;  test_dict['c'] = c_def
    test_dict['min_mag'] = 0.001;    test_dict['max_mag'] = 9.999
    test_dict['min_lat'] = 53.0;     test_dict['max_lat'] = 58.0
    test_dict['min_lon'] = 53.0;     test_dict['max_lon'] = 58.0
    test_dict['min_dep'] = min_dep;  test_dict['max_dep'] = 30
    test_dict['work_dir'] = wrk_dr
    test_dict['finf_name_'] = finf_nm
    test_dict['full_finf_name_'] = "\\".join([test_dict["work_dir"], test_dict["finf_name_"]])
    test_dict['npoint'] = 15*15 # 15*15

    test_dict['ini_mag'] = 8
    test_dict['ini_dep'] = 9 # км

    return test_dict

def create_grid_param(test_dict_) -> (int, int, int, float, float):
    n = test_dict_['npoint']
    nx_lon = round(sqrt(n))
    ny_lat = nx_lon
    step_lon = (test_dict_['max_lon'] - test_dict_['min_lon'])/(nx_lon-1)
    step_lat = (test_dict_['max_lat'] - test_dict_['min_lat'])/(ny_lat-1)
    return n , nx_lon, ny_lat, step_lon, step_lat

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
    dm_max_zeml = 1.2 # во сколько раз магнитуда в максимальном очаге больше, чем в остальных
    dm_max_magn = def_mgn*dm_max_zeml
    ini_lat = 0;     ini_lon = 0 # чтобы не было предупреждений IDE
    if n_zeml == 1:
        # точка в центре карты
        lat = test_dict_['min_lat'] + (test_dict_['max_lat'] - test_dict_['min_lat'])/2
        lon = test_dict_['min_lon'] + (test_dict_['max_lon'] - test_dict_['min_lon'])/2
        print(lat, lon, def_dep, dm_max_magn)
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

def calc_test_grid_write_txt(test_dict_, full_txt_fname: str, point_list: list) -> (np.ndarray, np.ndarray, np.ndarray, str):
    """
    расчет на прямоугольной сетке значений I_mod и их суммирование
    """
    a = test_dict_["a"]
    b = test_dict_["b"]
    c = test_dict_["c"]
    alt = 0.0   # высота
    di = 1.0
    dn = 2
    (n, nx_lon, ny_lat, step_lon, step_lat) = create_grid_param(test_dict_)
    lat_arr = np.random.random(n)
    lon_arr = np.random.random(n)
    imd_arr = np.random.random(n)
    n_hypo = len(point_list) # print(n_hypo)
    f = open(full_txt_fname, mode = 'w')
    f.write('{0:13s} {1:9s} {2:6s} {3:9s} {4:9s} {5:6s} {6:7s}\n'.format('Lat', 'Lon', 'Alt','I_fact', 'dI', 'N', 'Нас.пункт'))
    add_str = ''
    icurr = 0
    for i in range(nx_lon):
        lon_g = test_dict_['min_lon'] + i*step_lon
        print('lon_g=',lon_g)
        for j in range(ny_lat):
            lat_g = test_dict_['min_lat'] + j*step_lat
            print('lat_g=', lat_g)
            sum_i = 0.0
            for k in range(n_hypo):  # по гипоцентрам
                (lat, lon, dep, mgn) = point_list[k]
                print('k=',k, 'dep=',dep,'mgn=',mgn)

#  def calc_distance(lat_arr: float, lon_arr: float, h_arr: float, lat: float, lon: float, dep: float) -> float:
                dist3 = calc_distance(lat_g, lon_g, alt, lat, lon, dep)
                i_curr_mod = macroseis_fun(a=a, b=b, c=c, dist=dist3, mag=mgn, type_of_macro_fun_=type_of_macro_fun)
                i_curr_mod = i_curr_mod if i_curr_mod>0 else 0
                print(lat_g, lon_g, alt, lat, lon, dist3, i_curr_mod)
                sum_i = sum_i + i_curr_mod
                        # lat_g,   lon_g,    alt,   sum_i,     di,    dn,   sss
            n_point_s = 'n' + str(icurr).rjust(3, '0')
            n_point_s = n_point_s.rjust(11, ' ')
            lat_arr[icurr] = lat_g; lon_arr[icurr] = lon_g; imd_arr[icurr] = sum_i
            print(sum_i)
            f.write('{0:9.4f} {1:9.4f} {2:5.1f} {3:11.4f} {4:6.1f} {5:7d} {6:s}\n'.format(lat_g, lon_g, alt, sum_i, di, dn, n_point_s))
            icurr += 1
    f.close()
    return lat_arr, lon_arr, imd_arr, add_str

def cnv2str(*args) -> str:
    s = ''
    for num in args:
        s += str(num)+' '
    return s

def write_inf(test_dict_, full_inf_name:str, lat_ini: float, lon_ini: float):
    f = open(full_inf_name, mode = 'w', encoding='utf-8')
    f.write(test_dict_['name_sq']+' ; название площади'+'\n')
    f.write(test_dict_['fdat_name_']+ ' ; файл данных'+'\n')
    s = cnv2str(test_dict_['a'],test_dict_['b'],test_dict_['c']) + '; коэффициенты a, b, c макросейсмического уравнения'+'\n'
    f.write(s) # cp1251
    f.write(cnv2str(test_dict_['min_mag'],test_dict_['max_mag']) + '; минимальная и максимальная магнитуда'+'\n')
    f.write(cnv2str(test_dict_['min_lat'],test_dict_['max_lat']) + '; минимальная и максимальная широта, десятичные градусы'+'\n')
    f.write(cnv2str(test_dict_['min_lon'],test_dict_['max_lon']) + '; минимальная и максимальная долгота, десятичные градусы'+'\n')
    f.write(cnv2str(test_dict_['min_dep'],test_dict_['max_dep']) + '; минимальная и максимальная глубина, км'+'\n')
    f.write(cnv2str(lat_ini, lon_ini) + '; начальное приближение для минимизации: широта, долгота или число - среднее по скольки широтам и долготам n-точек с максимальной I_fact'+'\n')
    f.write(cnv2str(test_dict_['ini_mag'],test_dict_['ini_dep']) + '; начальное приближение для минимизации: магнитуда, глубина, км'+'\n')
    f.close()

    with open(full_inf_name) as fh:
        data = fh.read()

    with open(full_inf_name, 'wb') as fh:
        fh.write(data.encode('cp1251'))

def create_test1(curr_dat_dir:str, nequake :int) -> (np.ndarray, np.ndarray, np.ndarray, float, float, str):
    # создание тестового набора с распределенными точками
    # Выходные данные - векторы X, Y, Z для карты и точка начального приближения
    name_sq='test1_'+str(nequake)+'_all'
    short_fname_inf = "".join([name_sq, '.inf'])
    full_fname_inf  = "\\".join([curr_dat_dir, short_fname_inf])
    short_fname_txt = "".join([name_sq, '.txt'])
    full_fname_txt  = "\\".join([curr_dat_dir, short_fname_txt])
    test_dict_ = create_test_dict(name_sq_=name_sq, fdat_nam_=short_fname_txt,
                                  wrk_dr=curr_dat_dir, finf_nm=short_fname_inf)
    ini_lat, ini_lon, point_list_ = create_point_list1(test_dict_, n_zeml = nequake)
    write_inf(test_dict_, full_fname_inf, ini_lat, ini_lon)
    (lat_, lon_, ifact_, add_str) = calc_test_grid_write_txt(test_dict_, full_fname_txt, point_list_)
    return lat_, lon_, ifact_, ini_lat, ini_lon, add_str