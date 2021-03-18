"""
Отдельные функции в меню и константы, чтобы не загромождать файл ptkinter.py

(C) 2021 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""
#-- Значки и иконки
ico_progr = r'graphics\Земл144.ico'
ico_file_open_ = r'graphics\open_73704.png'
ico_calc_ = r'graphics\play_22349.png'
ico_resmap_ = r'graphics\map_54390.png'
ico_resgraph_ = r'graphics\chart_37129_2.png'
ico_usrmanual_ = r'graphics\text_81214_2.png'

win_name:str= "Макросейсмика" # название окна программы

usr_manual_fn = r'!Doc\Макросейсмика_РукПользователя_2021_1_1.docx'
ini_fn = 'makro_seis.ini' # текстовый файл с текущими параметрами
dat_dir = 'dat'

#-- Для подменю "Файл"
sf_input = "Открыть..."
sf_vinf = "Просмотр inf-файла"
sf_vdat = "Просмотр txt/xlsx-файла"
sf_vpar = "Просмотр параметров минимизации"
sf_vimap = "Карта исходных данных"
sf_exit = "Выход"

ss_fdi = "Данные введены"
ss_fdni = "Данные не введены"
ss_fnsf = "Не поддерживаемый формат файлов"

#-- Для подменю "Файл"
s_error = "Ошибка"
sf_ferror = "Ошибка в файле"
sf_finfni = "inf-файл не введен".center(30)
sf_err_ext = ss_fnsf.center(40)

#-- Для подменю "Расчет"


#-- Для подменю "Помощь"
sh_help = "Справка"
sh_about = "О программе"
sh_about1 = 'Программа "Макросейсмика"'.center(40) + "\n" +\
            "Разработчик Геник И.В.,".center(48) +\
            "\n" + "igenik@rambler.ru".center(52)
# Строки. Функции и методы строк
# https://pythonworld.ru/tipy-dannyx-v-python/stroki-funkcii-i-metody-strok.html

sh_usrmanual = "Руководство пользователя"
