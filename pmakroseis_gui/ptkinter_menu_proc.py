"""
Отдельные функции в меню и константы, чтобы не загромождать файл ptkinter.py

(C) 2021 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""
# Файл ptkinter_menu_proc

# -- События
VirtualEvents=['<<test_param_1>>', '<<test_param_2>>', '<<create_inf_for_2stage>>']

# -- Значки и иконки
ico_progr = r'graphics\Земл144.ico'
ico_input_inf_ = r'graphics\open_73704.png'
ico_calc_ = r'graphics\play_22349.png'
ico_resmap_ = r'graphics\map_54390.png'
ico_resgraph_ = r'graphics\chart_37129_2.png'
ico_usrmanual_ = r'graphics\text_81214_2.png'

win_name: str = "Макросейсмика"  # название окна программы

usr_manual_fn = 'Макросейсмика_РукПользователя_2021_1_2.docx'
usr_manual_fn_ini = r'!Doc\Макросейсмика_РукПользователя_2021_1_2.docx'

json_fn = 'Makroseis_GUI.json'  # текстовый файл с текущими параметрами

dat_dir = 'dat'
res_dir = 'res'

# -- Для словаря с данными
l1_coef_macro_ = 'коэффициенты a, b, c макросейсмического уравнения'
l2_min_max_magn = 'минимальная и максимальная магнитуда'
l3_min_max_lat = 'минимальная и максимальная широта, градусы'
l4_min_max_lon = 'минимальная и максимальная долгота, градусы'
l5_min_max_dep = 'минимальная и максимальная глубина, км'
l6_ini_appr = 'Начальное приближение для минимизации'
l7_ini_lat_lon = 'широта, долгота'
l8_ini_mag_dep = 'магнитуда, глубина, км'


# -- Для подменю "Файл"
sf_input = "Открыть inf-файл..."
sf_vinf = "Просмотр inf-файла"
sf_vdat = "Просмотр txt/xlsx-файла"
sf_vpar = "Просмотр параметров минимизации"
sf_vimap = "Карта исходных данных"
sf_vifactgr = "Диаграмма I_fact"
sf_vifactadd = "Диаграмма: приращение I_fact-приращение расстояния"
sf_vifactadd2 = "Диаграмма: зависимость интенсивности от расстояния до точки с максимальной интенсивностью"
sf_exit = "Выход"

ss_fdi = "Данные введены"
ss_fdni = "Данные не введены"
ss_fnsf = "Не поддерживаемый формат файлов"
ss_fdfpne = 'путь к dat-файлу не существует = '
ss_fdfne = 'dat-файл не существует = '
ss_fpne = 'путь не существует = '
ss_ffne_ = 'Файл не существует'

ss_fifnf = 'inf - файл не найден'.center(30)
ss_feif = 'Ошибки в inf-файле'.center(30)
ss_fedf = 'Ошибки в файле данных'.center(30)
ss_fedf_nac ='Не все столбцы'.center(40)

ss_fmsee = 'Ошибка в коэффициентах макросейсмического уравнения'
ss_fmde = 'Ошибка в диапазоне магнитуд'

# -- Для подменю "Вычисления"
sc_vres = "Просмотр выбранного результата минимизации"
sc_gres = "Графики интенсивности"
sc_gres_all = "Перебор графиков расчетной интенсивности"
sf_err_rad30 = 'Нет точек в радиусе 30 км. Стандартный расчет'.center(40)

ss_cdse = 'Ошибка хранения данных'
ss_cefse = 'Excel файл результатов не сохранен'
ss_ccb = 'Вычисления начаты'
ss_cce = 'Вычисления закончены'
ss_ccc = 'Вычисления прерваны'
ss_ccne = 'Вычисления не выполнены'
ss_cac = 'О вычислениях'
ss_cvrmap = "Карта исходных данных и результата минимизации"
ss_c2stagechoice = 'Выбор начального приближения для второго этапа минимизации'
ss_canothercalc = 'Вычисления для второй стадии минимизации в пункте меню "Расчет, 2 стадия"'
ss_canothercalc2 = 'inf-файл не для второй стадии минимизации'

ss_uc = 'не сделано'
# -- Для подменю "Файл"
s_error = "Ошибка"
sf_ferror = "Ошибка в файле"
sf_finfni = "inf-файл не введен".center(30)
sf_err_ext = ss_fnsf.center(40)

# -- Для подменю "Расчет"
sc_nif = 'Создан новый inf-файл'

# -- Для подменю "Тестирование"
st_testparam = 'Ввод параметров для тестирования алгоритма'
st_m1tsqunifom = 'Тестирование: квадрат, равномерная сетка'
#so_m1trealdata = 'Тестирование: файл реальных данных'
st_m1tssample = 'Тестирование: на основе inf-файла'
st_pseudo_mag = 'Псевдоинверсия: магнитуды'
st_pseudo_dep = 'Псевдоинверсия: глубины'
sc_create2stinf = 'Создать inf-файл для второго этапа минимизации'
sc_calc2st = 'Расчет, 2 стадия'

st_clusterization = 'Кластеризация методом k-средних'

# -- Для подменю "Настройки"
so_menufont = 'Настройка шрифта меню'

# -- Для подменю "Помощь"
sh_help = "Справка"
sh_about = "О программе"
sh_about1 = 'Программа "Макросейсмика", версия 2021.1.2'.center(40) + "\n" +\
            "Разработчик Иван В. Геник,".center(42) +\
            "\n" + "igenik@rambler.ru".center(52)
# Строки. Функции и методы строк
# https://pythonworld.ru/tipy-dannyx-v-python/stroki-funkcii-i-metody-strok.html

sh_usrmanual = "Файл: Руководство пользователя"
