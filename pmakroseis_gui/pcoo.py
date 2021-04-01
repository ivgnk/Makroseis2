# -------------------------------------------------------------------
# Функции преобразования координат // Coordinate conversion functions
# формулы взяты из стандарта // formulas are taken from the standard
# Глобальная навигационная спутниковая система Системы координат.
# Методы преобразований координат определяемых точек ГОСТ 32453-2013.pdf
# Global navigation satellite system coordinate.
# Systems methods for converting coordinates of defined points GOST 32453-2013
#
# (C) 2020 Ivan Genik, Perm, Russia
# Released under GNU Public License (GPL)
# email igenik@rambler.ru
# -------------------------------------------------------------------

from math import sin, cos, tan, pi, sqrt, trunc, radians

# Модуль math, список функций https://pythonworld.ru/moduli/modul-math.html
# используются в pcoo
# math.degrees(X) - конвертирует радианы в градусы.
# math.radians(X) - конвертирует градусы в радианы.
# math.cos(X) - косинус X (X указывается в радианах).
# math.sin(X) - синус X (X указывается в радианах).
# math.floor(X) - округление вниз
# math.trunc(X) - усекает значение X до целого.


def calc_num_zone(lg: float) -> int:
    """
    Входные данные:
    lg - долгота, градусы
    Алгоритм:
    Глобальная навигационная спутниковая система Системы координат Методы преобразований координат определяемых точек
    ГОСТ 32453-2013, стр.8, формула (28)
    """
    n: int = trunc((6+lg)/6)
    return n
# --------------------- from_gradminsec_to_decimal_degrees


def from_gradminsec_to_decimal_degrees(grad: int, minut: int, sec: int) -> float:
    """
    Входные данные: grad - градусы, minut - минуты, sec - секунды
    http://sitegeodesy.com/3.html -> Перевод угловых градусов минут и секунд в десятичные градусы
    """
    dat: float = grad + (minut/60) + (sec/3600)
    return dat
# --------------------- from_gradminsec_to_decimal_degrees


def from_geodetic_to_flatspatial(bg: float, lg: float, B: float, L: float) -> ([float], [float]):
    """
    входные данные
    bg, lg —   геодезические широта и долгота точки соответственно,  градусы
    тоже самое, но в радианах
    B, L —   геодезические широта и долгота точки соответственно
    на эллипсоиде Красовского;
    выходные данные, м
    x, y —   плоские  прямоугольные  координаты в проекции Гаусса— Крюгера
    x - на север, y - на восток

    Алгоритм: ГОСТ 32453-2013, стр.7,
    раздел 5.4   Преобразование геодезических координат в плоские прямоугольные координаты
    и обратно.
    Подраздел 5.4.1, формулы (25) и (26) с посмощью формул (27)-(28)
    """
    # вычисление n -  номер шестиградусной зоны в проекции Гаусса— Крюгера
    # формула (28)
    n: int = trunc((6+lg)/6)
    # print('n (номер зоны) = ', n)
    # вычисление l -  расстояние от определяемой точки до осевого меридиана зоны,  выраженное в радианной мере
    # формула (27)
    nn: int = 3+6*(n-1)
    l: float = (lg - nn)/57.29577951

    # общие заготовки для формул (25)-(26)
    sin2b = sin(2*B)
    sinb = sin(B)
    sinb_2 = sinb*sinb
    sinb_4 = sinb_2*sinb_2
    sinb_6 = sinb_4*sinb_2
    l2 = l*l

    # вычисление x - на север
    # формула (25)
    x: float = 6367558.4968*B - sin2b*(16002.8900 + 66.9607*sinb_2 + 0.3515*sinb_4 -
           l2*(1594561.25 + 5336.535*sinb_2 + 26.790*sinb_4 + 0.149*sinb_6 +
           l2*(672483.4 - 811219.9*sinb_2 + 5420*sinb_4 - 10.6*sinb_6 +
           l2 * (278194 - 830174*sinb_2 + 572434*sinb_4 - 16010*sinb_6 +
           l2 * (109500 - 574700*sinb_2 + 863700*sinb_4 - 398600*sinb_6)))))

    # вычисление y - на восток
    # формула (26)
    y: float = (5 + 10*n)*100000 + l*cos(B)*(6378245 + 21346.1415*sinb_2 + 107.1590*sinb_4 +
                0.5977*sinb_6 + l2*(1070204.16 - 2136826.66*sinb_2 + 17.98*sinb_4 - 11.99*sinb_6 +
                l2*(270806 - 1523417*sinb_2 + 1327645*sinb_4 - 21701*sinb_6 +
                l2*(79690 - 866190*sinb_2 + 1730360*sinb_4 - 945460*sinb_6))))

    return x, y
# ---------------------  from_geodetic_to_flatspatial


def calc_geogr_dist_onGOST(StartLat: float, StartLong: float, EndLat: float, EndLong: float) -> float:
    """
    Вычисление расстояния между токами: расчет плоских координат по ГОСТ и вычисление потом расстояния
    Входные данные:
    StartLat (начальная широта) = Градусы и сотые доли
    StartLong (начальная долгота) = Градусы и сотые доли
    EndLat (конечная широта) = Градусы и сотые доли
    EndLong (конечная долгота) = Градусы и сотые доли
    Выходные данные:
    Distance (расстояние) = Расстояние в километрах
    Вычисления:
    1) X и Y для Start & End функцией from_geodetic_to_flatspatial
    2) Вычисление расстояния между токами
    """
    if ((abs(StartLat - EndLat) < 1e-8) and (abs(StartLong - EndLong) < 1e-8)):
        Distance: float = 0
        return Distance

    StartLat_R: float = radians(StartLat)  # в радианах
    StartLong_R: float = radians(StartLong)  # в радианах
    EndLat_R: float = radians(EndLat)  # в радианах
    EndLong_R: float = radians(EndLong)  # в радианах
    (start_x, start_y) = from_geodetic_to_flatspatial(StartLat, StartLong, StartLat_R, StartLong_R)
    (end_x, end_y) = from_geodetic_to_flatspatial(EndLat, EndLong, EndLat_R, EndLong_R)
    distance: float = sqrt(pow(start_x - end_x, 2)+pow(start_y-end_y, 2))
    return distance


def from_geodetic_to_rectangular(b: float, l: float, h: float) -> ([float], [float], [float]):
    """
    входные данные
    b, l —   геодезические широта и долгота точки соответственно,  рад;
    h —   геодезическая высота точки,  м;
    выходные данные, м
    x, y, z —   прямоугольные пространственные координаты точки;

    Алгоритм: ГОСТ 32453-2013, стр.4,
    раздел 5.1  Преобразование геодезических координат в прямоугольные пространственные
    координаты и обратно.
    Подраздел 5.1.1, формулы (1) на основании (2)-(3)
    """

    # -------------------------------------------------------------------
    # Константы CК-42 и СК-95 - эллипосоид Красовского
    # ГОСТ 32453-2013, стр.4
    a_kp: float = 6378245.0  # метры, большая полуось
    alpha_kp: float = 1 / 298.3  # сжатие
    # Формула 3, вычисление e2 - квадрата эксцентриситета эллипсоида
    e2: float = 2 * alpha_kp - alpha_kp * alpha_kp

    # Формула 2, вычисление n -  радиуса кривизны первого вертикала, в метрах
    cos_b: float = cos(b)  # cos B, широты
    sin_b: float = sin(b)
    sin_2b: float = sin_b*sin_b
    cos_l: float = cos(l)  # cos L, долготы
    sin_l: float = sin(l)
    n: float = a_kp/sqrt(1-e2*sin_2b)
# Формула 1,  Преобразование геодезических координат в прямоугольные пространственные координаты
    x: float = (n+h)*cos_b*cos_l
    y: float = (n+h)*cos_b*sin_l
    z: float = ((1-e2)*n+h)*sin_b
    return x, y, z
# --------------------- from_geodetic_to_rectangular


def from_geodetic_to_flatspatial_fromwiki(dLon: float, dLat: float) -> ([float], [float]):
    """
    Latitude - широта, Longitude - долгота
    Алгоритм: https://ru.wikibooks.org/wiki/Реализации_алгоритмов/Перевод_географических_координат_в_прямоугольные_в_прямоугольные_координаты_проекции_Гаусса-Крюгера
    dLon, dLat —  долгота и широта точки соответственно,  градусов
    n, e - северное и востояное смещение, метры
    """
    # Номер зоны Гаусса-Крюгера (если точка рассматривается в системе
    # координат соседней зоны, то номер зоны следует присвоить вручную)
    zone = int(dLon/6.0+1)

    # Параметры эллипсоида Красовского
    a: float = 6378245.0          # Большая (экваториальная) полуось
    b: float = 6356863.019        # Малая (полярная) полуось
    e2: float = (a**2-b**2)/a**2  # Эксцентриситет
    n = (a-b)/(a+b)        # Приплюснутость

    # Параметры зоны Гаусса-Крюгера
    F = 1.0                   # Масштабный коэффициент
    Lat0 = 0.0                # Начальная параллель (в радианах)
    Lon0 = (zone*6-3)*pi/180  # Центральный меридиан (в радианах)
    N0 = 0.0                  # Условное северное смещение для начальной параллели
    E0 = zone*1e6+500000.0    # Условное восточное смещение для центрального меридиана

    # Перевод широты и долготы в радианы
    Lat: float = dLat*pi/180.0
    Lon: float = dLon*pi/180.0

    # Вычисление переменных для преобразования
    v = a*F*(1-e2*(sin(Lat)**2))**-0.5
    p = a*F*(1-e2)*(1-e2*(sin(Lat)**2))**-1.5
    n2 = v/p-1
    M1 = (1+n+5.0/4.0*n**2+5.0/4.0*n**3)*(Lat-Lat0)
    M2 = (3*n+3*n**2+21.0/8.0*n**3)*sin(Lat-Lat0)*cos(Lat+Lat0)
    M3 = (15.0/8.0*n**2+15.0/8.0*n**3)*sin(2*(Lat-Lat0))*cos(2*(Lat+Lat0))
    M4 = 35.0/24.0*n**3*sin(3*(Lat-Lat0))*cos(3*(Lat+Lat0))
    M = b*F*(M1-M2+M3-M4)
    I = M+N0
    II = v/2*sin(Lat)*cos(Lat)
    III = v/24*sin(Lat)*(cos(Lat))**3*(5-(tan(Lat)**2)+9*n2)
    IIIA = v/720*sin(Lat)*(cos(Lat)**5)*(61-58*(tan(Lat)**2)+(tan(Lat)**4))
    IV = v*cos(Lat)
    V = v/6*(cos(Lat)**3)*(v/p-(tan(Lat)**2))
    VI = v/120*(cos(Lat)**5)*(5-18*(tan(Lat)**2)+(tan(Lat)**4)+14*n2-58*(tan(Lat)**2)*n2)

    # Вычисление северного и восточного смещения (в метрах)
    N = I+II*(Lon-Lon0)**2+III*(Lon-Lon0)**4+IIIA*(Lon-Lon0)**6
    E = E0+IV*(Lon-Lon0)+V*(Lon-Lon0)**3+VI*(Lon-Lon0)**5

    return N, E   # N - Северное смещение, E - Восточное смещение
# --------------------- from_geodetic_to_flatspatial_fromwiki(
