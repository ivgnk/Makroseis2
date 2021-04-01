# import numpy as np
from math import *
from pcoo import *
import numba


# @numba.njit
def calc_geogr_dist(StartLat: float, StartLong: float, EndLat: float, EndLong: float) -> float:
    """
    Вычисления расстояние на земном эллипсоиде между двумя точками, км
    Входные данные:
    StartLat (начальная широта) = Градусы и сотые доли
    StartLong (начальная долгота) = Градусы и сотые доли
    EndLat (конечная широта) = Градусы и сотые доли
    EndLong (конечная долгота) = Градусы и сотые доли
    Выходные данные:
    Distance (расстояние) = Расстояние в километрах
    Bearing (смещение) = Смещение в градусах}
    """

    # // Переменные, используемые для вычисления смещения и расстояния
    # fPhimean: Double; // Средняя широта
    # fdLambda: Double; // Разница между двумя значениями долготы
    # fdPhi: Double; // Разница между двумя значениями широты
    # fAlpha: Double; // Смещение
    # fRho: Double; // Меридианский радиус кривизны
    # fNu: Double; // Поперечный радиус кривизны
    # fR: Double; // Радиус сферы Земли
    # fz: Double; // Угловое расстояние от центра сфероида
    # fTemp: Double; // Временная переменная, использующаяся в вычислениях
    # проверка на неравенсктво точек. Если точки равны, то расстояние = 0 и досрочный выход
    if ((abs(StartLat - EndLat) < 1e-8) and (abs(StartLong - EndLong) < 1e-8)):
        Distance: float = 0
        Bearing: float = 0
        return Distance # , Bearing

    # const Константы, используемые для вычисления смещения и расстояния
    D2R: float = pi/180  # //0.017453;            // Константа для преобразования градусов в радианы
    R2D: float = 180/pi  # //57.295781;           // Константа для преобразования радиан в градусы
    a: float = 6378.1370  # // Основные полуоси
    b: float = 6356.752314245  # // Неосновные полуоси
    e2: float = 0.006739496742337  # // Квадрат эксцентричности эллипсоида
    f: float = 0.003352810664747  # // Выравнивание эллипсоида

    # // Вычисляем разницу между двумя долготами и широтами и получаем среднюю широту
    fdLambda: float = (StartLong - EndLong) * D2R
    fdPhi: float = (StartLat - EndLat) * D2R
    fPhimean: float = ((StartLat + EndLat) / 2.0) * D2R

    # // Вычисляем меридианные и поперечные радиусы кривизны средней широты
    fTemp: float = 1 - e2 * (pow(sin(fPhimean), 2))
    fRho: float = (a * (1 - e2)) / pow(fTemp, 1.5)
    fNu: float = a / (sqrt(1 - e2 * (sin(fPhimean) * sin(fPhimean))))

#    print('fz1=', fz)
    # // Вычисляем угловое расстояние
    fz: float = sqrt(pow(sin(fdPhi / 2.0), 2) + cos(EndLat * D2R) * cos(StartLat * D2R) * pow(sin(fdLambda / 2.0), 2))
#    print('fz1=', fz)
    fz: float = 2 * asin(fz)
#    print('fz2=', fz)
    Bearing: float = degrees(fz)  # RadToDeg -> math.degrees(X) - конвертирует радианы в градусы

    # // Вычисляем смещение
    fAlpha: float = cos(EndLat * D2R) * sin(fdLambda) * 1 / sin(fz)
    fAlpha: float = asin(fAlpha)
    # {Bearing := RadToDeg(fAlpha);}
    # // Вычисляем радиус Земли
    fR: float = (fRho * fNu) / ((fRho * pow(sin(fAlpha), 2)) + (fNu * pow(cos(fAlpha), 2)))

    # // Получаем смещение и расстояние
    Distance: float = (fz * fR)

    return Distance  # , Bearing
# --------------- CalcGeogrDist


def test_calc_geogr_dist() -> None:
    """
    Тестирование функции def calc_geogr_dist(StartLat: float, StartLong: float, EndLat: float, EndLong: float):
    """
    print('Функция test_calc_geogr_dist')
    # первые 2 точки из точки_ввод.xls
    StartLat: float = 54.854
    StartLong: float = 58.422
    EndLat: float = 54.938
    EndLong: float = 58.809
    Distance = calc_geogr_dist(StartLat, StartLong, EndLat, EndLong)
    print(f'Distance  = {Distance:#10.5F} ')
    #  print(f'Bearing = {Bearing:#10.5F}')
    print()
# --------------- CalcGeogrDist


def compare_distance() -> None:
    """
    Сравнение результатов функций
    1) из geogr_distance.py -  calc_geogr_dist(StartLat: float, StartLong: float, EndLat: float, EndLong: float):
    2) из pcoo.py - def from_geodetic_to_flatspatial(bg:float,lg:float, B: float, L: float) -> ([float], [float]):
    """
    # границы 6-градусных зон: 42, 48, 54, 60, 66
    print('Функция compare_distance()')
    #         Город,     Широта	Долгота
    #                    Lat	Lon
    towns = {'Юрюзань': [54.854, 58.422], 'Бакал': [54.938, 58.809], 'Новозаречный': [54.912, 57.321],
             'Вязовая': (54.903, 58.350), 'Верх-Катавка': (54.618, 58.282), 'Кропачева': (55.012, 57.989)}
    StartLat: float = towns['Юрюзань'][0]
    StartLong: float = towns['Юрюзань'][1]
    for key in towns:
        print(key)  # ,'  ',towns[key],'  ',towns[key][0],'  ',towns[key][1]
        EndLat: float = towns[key][0]
        EndLong: float = towns[key][1]

        Len_Gost = calc_geogr_dist_onGOST(StartLat, StartLong, EndLat, EndLong)  # в метрах
        Len_NoNa = calc_geogr_dist(StartLat, StartLong, EndLat, EndLong)  # в километрах
        # первое значение - в метры, второе - километры
        print("Len (Gost), км = %11.6f  Len(NoNa), км = %11.6f" % (Len_Gost/1000, Len_NoNa[0]))

        # print('Len (Gost) = ',Len_Gost,'  Len(NoNa) = ',Len_NoNa[0])


def test_calc_geogr_dist2() -> None:
    """
    Просто расчет расстояний для проверки по функции def calc_geogr_dist(StartLat: float, StartLong: float, EndLat: float, EndLong: float):
    """
    print('Красный ключ - Челябинск')
    StartLat: float = 55.3881557   # Красный ключ
    StartLong: float = 56.655421
    EndLat: float = 55.154  # Челябинск
    EndLong: float = 61.429
    Distance = calc_geogr_dist(StartLat, StartLong, EndLat, EndLong)
    print(f'Distance  = {Distance:#10.5F} ')

    StartLat: float = 54.912   # Новозаречный
    StartLong: float = 57.321
    EndLat: float = 55.154  # Челябинск
    EndLong: float = 61.429
    Distance = calc_geogr_dist(StartLat, StartLong, EndLat, EndLong)
    print(f'Distance  = {Distance:#10.5F} ')

# test_calc_geogr_dist2()
