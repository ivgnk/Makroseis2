"""
Главный объект программы class MakroseisGUI(Frame):

(C) 2020 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""

from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import scrolledtext
# from tkinter.constants import END

from typing import Any
import Pmw
import ptkinter_menu_proc

from ptkintertools import *
# from pmakroses_proc import *
from dataclasses import dataclass
from ptkinter_menu_proc import *

# --- matplotlib imports
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PIL import Image, ImageTk
import os
import sys
import pathlib
import winsound
# ------ Из Makro_seis
import pfile
import pfunct
import pinp_proc
import pinp_struct
import pmain_proc
import json


p_width: int = 1400  # ширина окна программы
p_height: int = 900  # высота окна программы

view_inf_fw: int = 1150  # ширина окна проcмотра inf-файла
view_inf_fh: int = 400  # высота окна проcмотра inf-файла

view_datt_fw: int = 1150  # ширина окна проcмотра dat-файла txt
view_datt_fh: int = 800  # высота окна проcмотра dat-файла  txt

view_datx_fw: int = 900  # ширина окна проcмотра dat-файла  xls
view_datx_fh: int = 800  # высота окна проcмотра dat-файла  xls

view_map_fw: int = 1140  # ширина окна проcмотра карты
view_map_fh: int = 780  # высота окна проcмотра карты

view_graph_fw: int = 1140  # ширина окна проcмотра графика
view_graph_fh: int = 780  # высота окна проcмотра графика

view_par_fw: int = 750  # ширина окна проcмотра параметров минимизации
view_par_fh: int = 200  # высота окна проcмотра параметров минимизации

view_res_fw: int = 450  # ширина окна проcмотра результатов минимизации
view_res_fh: int = 220  # высота окна проcмотра результатов минимизации


vf_width: int = 700  # ширина окна просмотра
vf_height: int = 700  # высота окна программы

status_bar_width = 220
status_bar_height = 20

#  1 июля 2018 Введение в Data classes (Python 3.7)
#  https://habr.com/ru/post/415829/

res0dict = dict(  # --- общие
                calc_status=False,  # как завершено - False - неуспех, True - успех
                lin_coeff=8.0,  # коэффициент для барьерной функции, см. pinp_struct.lin_coeff
                max_num_iter=1_000_000,
                # --- конкретные
                file_res_name='',
                num=-13   , lat_=-13.0, lon_=-13.0,
                dep_=-13.0, mag_=-13.0, fun_=-13.0)


@dataclass
class StatusBarLabel:
    status_bar: Any
    the_status: int

# класс для результатов вычислений
@dataclass
# class ResultCalcClass:
#     #--- общие
#     calc_status: bool = False # как завершено - False - неуспех, True - успех
#     lin_coeff: int = 8   # коэффициент для барьерной функции, см. pinp_struct.lin_coeff
#     max_num_iter: int = 1_000_000
#     #--- конкретные
#     file_res_name: str = ''
#     num: int = -13
#     lat_: float = -13
#     lon_: float = -13
#     dep_: float = -13
#     mag_: float = -13
#     fun_: float = -13

# ----------- Источники
# Создание графического интерфейса https://metanit.com/python/tutorial/9.1.php
# Диалоговые (всплывающие) окна / tkinter 9 https://pythonru.com/uroki/dialogovye-vsplyvajushhie-okna-tkinter-9

# ----------- ООП
# Библиотека Tkinter - 9 - Использование ООП
# https://www.youtube.com/watch?v=GhkyLQ6A6Yw&list=PLfAlku7WMht4Vm6ewLgdP9Ou8SCk4Zhar&index=9

class MakroseisGUI(Frame):
    # Константы для смены надписей в StatusBar
    SBC_st = 0    # Программа запущена
    SBC_fdni = 10  # Данные не введены
    SBC_fdi = 11  # Данные введены
    SBC_fvpar = 14  # Просмотр параметров минимизации

    SBC_cb = 21  # Вычисления начаты
    SBC_ce = 22  # Вычисления закончены
    SBC_cc = 23  # Вычисления прерваны

    SBC_hab = 41  # О программе
    SBC_hum = 42  # Руководство пользователя
    SBC_ns = 50

    is_input_inf = False;     fn_current_inf = ''    # текущий inf-файл
    is_input_txt = False;     fn_current_txt = ''   # текущий txt-файл
    is_input_xlsx = False;    fn_current_xlsx = ''  # текущий xlsx-файл
    is_exist_resf = False;    fn_current_resf = ''  # текущий res-файл
    dict_struct = pinp_struct.empty_inf_dict
    res_dict = res0dict
    res_list = []

    # fn_inf = '' # имя inf-файла
    dn_current_dir = ''
    dn_current_dat_dir = ''
    dn_current_res_dir = ''

    scr_w = 0  # ширина экрана
    scr_h = 0  # высота экрана

    def __init__(self, main):
        super().__init__(main)
        # Строка статуса
        # https://www.delftstack.com/ru/tutorial/tkinter-tutorial/tkinter-status-bar/
        # the_status_bar_label1   # 0 - Начата работа программы        # 1 - Данные введены
                                  # 2 - Вычисление закончено           # 3 - Вычисление прервано
        self.the_status_bar_label1 = StatusBarLabel(status_bar = Label(main, text=" Программа запущена ", bd=1, relief=SUNKEN, anchor=W), the_status=0)
        self.the_status_bar_label2 = StatusBarLabel(status_bar = Label(main, text="                    ", bd=1, relief=SUNKEN, anchor=W), the_status=0)
        self.the_status_bar_label3 = StatusBarLabel(status_bar = Label(main, text="                    ", bd=1, relief=SUNKEN, anchor=W), the_status=0)

        main.title(win_name)
        (self.scr_w, self.scr_h, form_w_, form_h_, addx, addy) = mainform_positioning(main, p_width, p_height)
        # print('self.scr_w, self.scr_h')
        # print(self.scr_w, self.scr_h)

        # main.geometry(root_geometry_string_auto(main, p_width, p_heiht)) # 1920x1080 мой монитор
        main.geometry(root_geometry_string(form_w_, form_h_, addx, addy))
        # Python Tkinter, как запретить расширять окно программы на полный экран?
        # https://otvet.mail.ru/question/191704214
        main.resizable(width=False, height=False)
        main.config(menu=self.create_menu())
        main.iconbitmap(ico_progr)

        # разлчиные варианты выхода
        # https://fooobar.com/questions/83280/how-do-i-handle-the-window-close-event-in-tkinter
        main.protocol("WM_DELETE_WINDOW", self.on_closing)
        main.bind('<Escape>', self.btn_esc)
        # main.bind('<Control-b>', self.view2_txt_dat)  #  еще раз просмотр файла данных, но собранного из массива np.
        # main.bind('<Control-i>', self.view_inf_inf_)  #  вывод служебной информации
        main.bind('<Control-g>', self.calc_view_graph_res_event_btn)  #  построение графика

        # self.the_status_bar_label1.status_bar.pack(side=LEFT, fill=X)
        # self.the_status_bar_label2.status_bar.pack(side=LEFT, fill=X)
        # -------- Создание Status bar
        rest_width = form_w_ - (2*(status_bar_width+2+2))
        self.the_status_bar_label1.status_bar.place(x=1,                      y=form_h_-status_bar_height-3, width=status_bar_width, height=status_bar_height)
        self.the_status_bar_label2.status_bar.place(x=status_bar_width+2,     y=form_h_-status_bar_height-3, width=status_bar_width, height=status_bar_height)
        self.the_status_bar_label3.status_bar.place(x=2*(status_bar_width+2), y=form_h_-status_bar_height-3, width=rest_width, height=20)
        # -------- Создание панели инструментов
        # Меню, подменю и панель инструментов в Tkinter
        # https://python-scripts.com/tkinter-menu-toolbars-example

        # Pmw.Balloon
        # http://pmw.sourceforge.net/doc/Balloon.html
        self.balloon = Pmw.Balloon(main)
        self.create_tool_bar(main)

        # Определяем текущую папку с программой https://ru.stackoverflow.com/questions/535318/Текущая-директория-в-python
        self.dn_current_dir = os.getcwd()
        self.dn_current_dat_dir = "\\".join([self.dn_current_dir, dat_dir])
        self.dn_current_res_dir = "\\".join([self.dn_current_dir, res_dir])

        # проверяем наличие и при отсутствии создаем папку результатов
        path = pathlib.Path(self.dn_current_res_dir)
        if not path.is_dir():
            path.mkdir()

        # Определяем есть ли json файл
        path = pathlib.Path(json_fn)
        if path.is_file():
            self.get_from_json()
            self.dict_struct["saved_in_json"] = 1
            pinp_proc.the_input(fname=self.dict_struct['full_finf_name_'], res_dir = self.dn_current_res_dir, is_view=False)
        else:
            self.dict_struct["saved_in_json"] = 0

    def on_closing(self):
        sys.exit(0)

    def btn_esc(self, event):
        sys.exit(0)
        # root.bind('<Escape>', btn_esc)

    def create_tool_bar(self, main):
        toolbar = Frame(main, bd=1, relief=RAISED)
        # https://icon-icons.com/ru/download/
        # полный формат ввода иконки 'E:\Work_Lang\Python\PyCharm\Tkinter\Ico\play_22349.png
        self.create_button1(ico_input_inf_, self.input_inf_, toolbar, 'Открыть файл данных')
        self.create_button1(ico_calc_, self.c_calc_, toolbar, 'Расчет')
        self.create_button1(ico_resmap_, self.cmd_calc_resmap_event, toolbar, 'Карта результатов')
        self.create_button1(ico_resgraph_, self.calc_view_graph_res_event, toolbar, 'График результатов')
        self.create_button1(ico_usrmanual_, self.help_usrmanual_, toolbar, sh_usrmanual)
        toolbar.pack(side=TOP, fill=X)

    # Всплывающие окна   https://pythonru.com/uroki/vsplyvajushhie-okna-tkinter-11
    # 2020_Tkinter Программирование на GUI Python_Шапошникова.pdf  11. Окна, стр. 48, 86
    # tkinter, Усложнение диалогов window_09.py http://www.russianlutheran.org/python/nardo/nardo.html
    # https://fooobar.com/questions/14054375/grabset-in-tkinter-window

    def create_scrolledtext_win(self, main):

        # https://ru.stackoverflow.com/questions/791876/Отображение-виджетов-в-tkinter-скрыть-и-вернуть-обратно
        scrolledtext_frame = Frame(main, bd=2)
        # frame1.pack(fill='both', expand='yes')
        scrolledtext_frame.pack(side=TOP, fill=X)
        scrolledtext_win = scrolledtext.ScrolledText(scrolledtext_frame, wrap=WORD,  width=20, height=10)
        scrolledtext_win.pack(padx=10, pady=10, fill=BOTH, expand=True)
        scrolledtext_win.pack_forget()
        scrolledtext_win.insert(INSERT,
                        """\
                        Integer posuere erat a ante venenatis dapibus.
                        Posuere velit aliquet.
                        Aenean eu leo quam. Pellentesque ornare sem.
                        Lacinia quam venenatis vestibulum.
                        Nulla vitae elit libero, a pharetra augue.
                        Cum sociis natoque penatibus et magnis dis.
                        Parturient montes, nascetur ridiculus mus.
                        """)
        return scrolledtext_win

    def change_status_bar1(self, status, status_bar):
        self.the_status = status
        if status == self.SBC_st:
            status_bar['text'] = 'Программа запущена'
        elif status == self.SBC_fdi:
            status_bar['text'] = ss_fdi
        elif status == self.SBC_fdni:
            status_bar['text'] = ss_fdni
        elif status == self.SBC_fvpar:
            status_bar['text'] = sf_vpar
        elif status == self.SBC_cb:
            status_bar['text'] = ss_ccb  # 'Вычисления начаты'
        elif status == self.SBC_ce:
            status_bar['text'] = ss_cce  # 'Вычисления закончены'
        elif status == self.SBC_cc:
            status_bar['text'] = ss_ccc  # 'Вычисления прерваны'
        # ---- Подменю Помощь
        elif status == self.SBC_hab:
            status_bar['text'] = sh_about
        elif status == self.SBC_hum:
            status_bar['text'] = sh_usrmanual
        else:
            status_bar['text'] = 'Неопределенный статус'

    # ---- Панель инструментов
    def create_button1(self, icofilename: str, the_command, the_toolbar, the_hint):
        """
        Создание кнопки
        """
        self.img = Image.open(icofilename)
        eimg = ImageTk.PhotoImage(self.img)
        the_button = Button(
            the_toolbar, image=eimg, relief=FLAT,
            command=the_command
        )
        the_button.image = eimg
        the_button.pack(side=LEFT, padx=2, pady=2)
        self.balloon.bind(the_button, the_hint)

    # def cmd_open(self):  winsound.Beep(frequency=150, duration=1000)

    def cmd_calc(self):
        winsound.Beep(frequency=200, duration=1000)

    def cmd_calc_resmap_event(self):
        self.f_view_map_res()

    def input_from_inf(self, fname: str) -> bool:
        (good_end, self.dict_struct) = pinp_proc.the_input(fname=fname, res_dir = self.dn_current_res_dir, is_view=False)

        self.put_to_json()
        self.dict_struct["saved_in_json"] = 1
        return good_end

    # def input_from_txt(self, fname: str) -> bool:
    #     pass
    #
    # def input_from_xlsx(self, fname: str) -> bool:
    #     pass

    # ---- Подменю Файл
    def input_inf_(self):
        ext_type = ''
        good_new_data = ''

        fn_dat = fd.askopenfilename(initialdir=self.dn_current_dat_dir,
             defaultextension='.inf', filetypes=[('inf файлы', '*.inf')])
        # , ('txt файлы', '*.txt'), ('xlsx файлы', '*.xlsx'), ('Все файлы', '*.*')

        the_ext = pfile.gfe(fn_dat)
        if the_ext == '.inf':
            ext_type = 'i'
            good_new_data = self.input_from_inf(fn_dat)
            if good_new_data:
                # self.dict_struct['full_finf_name_'] = fn_dat
                # self.dict_struct['finf_name_'] =
                self.dict_struct['typeof_input'] = 1
        # elif the_ext == '.txt':
        #     ext_type = 't'
        #     good_new_data = self.input_from_txt(fn_dat)
        #     self.dict_struct['typeof_input'] = 2
        # elif the_ext == '.xlsx':
        #     ext_type = 'x'
        #     good_new_data = self.input_from_xlsx(fn_dat)
        #     self.dict_struct['typeof_input'] = 3
        elif the_ext == '':
            ext_type = ''
        else:
            ext_type = 'n'
            mb.showerror(s_error, sf_err_ext)

        if ext_type == '':
            # self.change_status_bar1(self.SBC_fdni, self.the_status_bar_label1.status_bar)
            # self.the_status_bar_label3.status_bar['text'] = ''
            pass
        elif ext_type == 'n':
            # self.change_status_bar1(self.SBC_fdni, self.the_status_bar_label1.status_bar)
            # self.the_status_bar_label3.status_bar['text'] = ss_fnsf
            pass
        else:
            if good_new_data:
                self.change_status_bar1(self.SBC_fdi, self.the_status_bar_label1.status_bar)
                self.the_status_bar_label3.status_bar['text'] = fn_dat
            else:
                self.change_status_bar1(self.SBC_fdni, self.the_status_bar_label1.status_bar)
                self.the_status_bar_label3.status_bar['text'] = sf_ferror

    def put_to_json(self):  # запись dict_struct в json
        # https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
        with open(json_fn, 'w') as file:
            json.dump((self.dict_struct,self.res_dict,self.res_list), file)

    def get_from_json(self):  # чтение dict_struct из json
        # https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
        with open(json_fn, 'r') as file:
            (self.dict_struct, self.res_dict,self.res_list) = json.load(file)
            # print(self.res_dict)

    def view_file(self, fname: str):
        pass

    def input_txt(self):
        pass

    def input_xlsx(self):
        pass

    def f_view_inf(self) -> None:
        if self.dict_struct['full_finf_name_'] == '':
            mb.showerror(s_error, sf_finfni)
        else:
            ffn = self.dict_struct['full_finf_name_']
            f = open(ffn, 'r')
            s = f.read()

            (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_inf_fw, view_inf_fh)
            self.dialog = CViewTxt(self.master, sf_vinf + '    ' + ffn, root_geometry_string(form_w_, form_h_, addx, addy))
            self.dialog.go(s.encode('cp1251').decode('utf-8'))
            f.close()

    def f_view_dat(self):
        if (self.dict_struct["saved_in_json"] == 1) or (self.dict_struct['typeof_input'] > 0):
            dfn = self.dict_struct['full_fdat_name_']
            if dfn == '':
                mb.showerror(s_error, ss_fdfne+dfn)
            else:
                ffn = self.dict_struct['full_fdat_name_']
                ss = pfile.gfe(ffn)
                if ss =='.txt':
                    f = open(self.dict_struct['full_fdat_name_'], 'r')
                    s = f.read()
                    # s = '1\n22\n333'
                    f.close()
                    (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_datt_fw, view_datt_fh)
                    self.dialog = CViewTxt(self.master, sf_vdat + '    ' + ffn, root_geometry_string(form_w_, form_h_, addx, addy))
                    self.dialog.go(s)  #  .encode('cp1251').decode('utf-8')
                elif ss == '.xlsx':
                    # https://pythonru.com/uroki/chtenie-i-zapis-fajlov-excel-xlsx-v-python
                    s = '   Lat          Lon      Alt      I_fact        dI            N                  Нас.пункт' + '\n'
                    s += pinp_struct.get_dat_array_for_view()
                    (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_datx_fw, view_datx_fh)
                    self.dialog = CViewTxt(self.master, sf_vdat + '    ' + ffn, root_geometry_string(form_w_, form_h_, addx, addy))
                    self.dialog.go(s)  #  .encode('cp1251').decode('utf-8')
                    # mb.showerror(s_error, s_error)
        else:
            mb.showerror(s_error, ss_fdni)

    def f_view_xlsx(self):
        pass

    def view2_txt_dat(self, event):    # еще раз просмотр файла данных, но собранного из массива np.
        # mb.showerror(s_error, 'Заглушка')
        s = self.create_txt_dat_str()
        (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_datt_fw, view_datt_fh)
        self.dialog = CViewTxt(self.master, sf_vpar, root_geometry_string(form_w_, form_h_, addx, addy))
        self.dialog.go(s)  # .encode('cp1251').decode('utf-8')

    def view_inf_inf_(self, event):    # еще раз просмотр файла данных, но собранного из массива np.
        # pinp_struct.get_Lat_Lon()
        # pinp_struct.get_ifact()
        pass


    def create_txt_dat_str(self) -> str:
        s = '                  Lat              Lon      Alt        I_fact            dI            N                  Нас.пункт' + '\n    '
        s += str(pinp_struct.curr_nstruct)+'\n    '
        if pinp_struct.curr_nstruct < 0:  # не введены данные
            pass
        else:
            the_arr = pinp_struct.dat_struct[pinp_struct.curr_nstruct, 1]
            s += str(len(the_arr))
        return s

    def create_parminim_str(self, infstr: str) -> str:
        d = self.dict_struct
        s = infstr + '\n    '  # пробелы в качестве левого отступа следующей строки
        s += '\n    '
        s += l1_coef_macro_  + ' = '+str(d['a'])+'  '+str(d['b'])+'  '+str(d['c']) + '\n    '
        s += l2_min_max_magn + ' = '+str(d['min_mag'])+'  '+str(d['max_mag'])+'\n    '
        s += l3_min_max_lat  + ' = '+str(d['min_lat'])+'  '+str(d['max_lat'])+'\n    '
        s += l4_min_max_lon  + ' = '+str(d['min_lon'])+'  '+str(d['max_lon'])+'\n    '
        s += l5_min_max_dep  + ' = '+str(d['min_dep'])+'  '+str(d['max_dep'])+'\n    '
        s += l6_ini_appr.rjust(55) + '\n    '
        s += l7_ini_lat_lon  + ' = '+str(d['ini_lat'])+'  '+str(d['ini_lon'])+'\n    '
        s += l8_ini_mag_dep  + ' = '+str(d['ini_mag'])+'  '+str(d['ini_dep'])
        return s

    def f_view_par_minim(self):
        infstr: str = ''
        if self.dict_struct["finf_name_"] == "":
            infstr = 'Параметры по умолчанию'.rjust(45)
        else:
            infstr = 'Параметры из inf-файла   ' + self.dict_struct["full_finf_name_"]

        if (self.dict_struct["saved_in_json"] == 1) or (self.dict_struct['typeof_input'] > 0):
           s = self.create_parminim_str(infstr)
           (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_par_fw, view_par_fh)
           self.dialog = CViewTxt(self.master, sf_vpar, root_geometry_string(form_w_, form_h_, addx, addy))
           self.dialog.go(s)  # .encode('cp1251').decode('utf-8')
        else:
           if self.dict_struct['typeof_input'] == 0:  # не введено
                mb.showerror(s_error, ss_fdni)
           else:
               pass

    def f_get_macro_and_ini(self):
    # взятие точек макросейсмического обследования и начального приближения
        xmap: np.ndarray  # Lon из файла
        ymap: np.ndarray  # Lat макросейсмического
        zmap: np.ndarray  # I_fact обследования

        (ymap, xmap) = pinp_struct.get_Lat_Lon()
        zmap =  pinp_struct.get_ifact()

        xini: float = self.dict_struct['ini_lon'] # начальное приближение Х, Lon
        yini: float = self.dict_struct['ini_lat'] # начальное приближение Y, Lat
        #      Lon   Lat   I_fact ini_lon ini_lat
        return xmap, ymap, zmap, xini, yini

    def f_view_map_ini(self):
        # if self.dict_struct['typeof_input'] ==  0:  # не введено
        #     mb.showerror(s_error, ss_fdni)
        # else:
        if pinp_struct.curr_nstruct==-1:
            mb.showerror(s_error, ss_fdni)
        else:
            xmap: np.ndarray  # Lon    из файла
            ymap: np.ndarray  # Lat    макросейсмического
            zmap: np.ndarray  # I_fact обследования
            xini: float # начальное приближение Х, Lon
            yini: float # начальное приближение Ym Lat
            # Lon   Lat   I_fact ini_lon ini_lat
            (xmap, ymap, zmap, xini, yini) = self.f_get_macro_and_ini()
            (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_map_fw, view_map_fh)
            # print('f_view_map_ini')
            # print('self.scr_w, self.scr_h');             print(self.scr_w, self.scr_h)
            # print('view_map_fw, view_map_fh');            print(view_map_fw, view_map_fh)
            # print('addx, addy');            print(addx, addy)

            map_name = 'Участок ' + self.dict_struct["name_sq"]+'. Карта интенсивности I_fact и точка начального приближения'
            self.dialog = CViewMap2(self.master, sf_vimap, map_name, root_geometry_string(form_w_, form_h_, addx, addy),
                                    xmap, ymap, zmap, xini, yini, None, True)
            self.dialog.go()

    def file_exit_(self):
        # https://ru.stackoverflow.com/questions/459170
        self.destroy()
        # sys.exit(0)

    # ---- Подменю Расчет
    def c_calc_(self):
        if self.dict_struct['typeof_input'] != 1:
            mb.showerror(s_error, ss_fdni)
        else:
            self.change_status_bar1(self.SBC_cb, self.the_status_bar_label1.status_bar)
            (result_bool, num, lat_, lon_, dep_, mag_, fun_, res_list_) = pmain_proc.work_with_data(is_view1 = False)
            self.res_list = res_list_
            if result_bool:
                self.put_to_res_dict(num, lat_, lon_, dep_, mag_, fun_)
                ini_lat_ = self.dict_struct['ini_lat']  # начальное приближение Lat
                ini_lon_ = self.dict_struct['ini_lon']  # начальное приближение Lon
                self.put_to_json()
                str_info = pmain_proc.create_str_res(ini_lat_, ini_lon_, num, lat_, lon_, dep_, mag_, fun_)

                (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_res_fw, view_res_fh)
                self.dialog = CViewTxt(self.master, sc_vres, root_geometry_string(form_w_, form_h_, addx, addy))
                self.dialog.go(str_info)  # .encode('cp1251').decode('utf-8')

                self.change_status_bar1(self.SBC_ce, self.the_status_bar_label1.status_bar)
            else:
                mb.showerror(s_error, ss_cdse) #  'ошибка хранения данных'
                self.change_status_bar1(self.SBC_cc, self.the_status_bar_label1.status_bar)

    def put_to_res_dict(self, num: int, lat_: float, lon_: float, dep_: float, mag_: float, fun_: float):
        self.res_dict['num'] = num;         self.res_dict['lat_'] = lat_
        self.res_dict['lon_'] = lon_;       self.res_dict['dep_'] = dep_
        self.res_dict['mag_'] = mag_;       self.res_dict['fun_'] = fun_
        self.res_dict['file_res_name'] = pmain_proc.log_file_name


    def get_from_res_dict(self) -> (int, float, float, float, float, float):
        num  = self.res_dict['num']
        lat_ = self.res_dict['lat_']
        lon_ = self.res_dict['lon_']
        dep_ = self.res_dict['dep_']
        mag_ = self.res_dict['mag_']
        fun_ = self.res_dict['fun_']
        return num, lat_ , lon_ , dep_ , mag_, fun_

    def c_view_main_res(self):
        if self.res_list == []:
            mb.showerror(s_error, ss_ccne)
        else:
            (num, lat_ , lon_ , dep_ , mag_, fun_) = self.get_from_res_dict()
            ini_lat_ = self.dict_struct['ini_lat']  # начальное приближение Lat
            ini_lon_ = self.dict_struct['ini_lon']  # начальное приближение Lon

            str_info = pmain_proc.create_str_res(ini_lat_, ini_lon_, num, lat_, lon_, dep_, mag_, fun_)

            (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_res_fw, view_res_fh)
            self.dialog = CViewTxt(self.master, sc_vres, root_geometry_string(form_w_, form_h_, addx, addy))
            self.dialog.go(str_info)  # .encode('cp1251').decode('utf-8')

    def c_view_all_res(self):
        # Определяем есть ли файл
        if self.res_list == []:
            mb.showerror(s_error, ss_ccne)
        else:
            fn = self.res_dict['file_res_name']
            path = pathlib.Path(fn)
            if path.is_file():
                os.startfile(fn)
                self.change_status_bar1(self.SBC_hum, self.the_status_bar_label1.status_bar)
            else:
                mb.showerror(s_error, ss_ffne_.center(70)+'\n'+fn)

    def exract_lat_lon_list(self, ini_list) -> list:
        n = len(ini_list)
        res0list = list()
        for i in range(n):
            res0list.append([ini_list[i][0], ini_list[i][1]])
        return res0list

    def f_view_map_res(self):
        # if self.dict_struct['typeof_input'] ==  0:  # не введено
        #     mb.showerror(s_error, ss_fdni)
        # else:
        if pinp_struct.curr_nstruct==-1:
            mb.showerror(s_error, ss_fdni)
        elif self.res_list == []:
            mb.showerror(s_error, ss_ccne)
        else:
            xmap: np.ndarray  # Lon    из файла
            ymap: np.ndarray  # Lat    макросейсмического
            zmap: np.ndarray  # I_fact обследования
            # Lon   Lat   I_fact ini_lon ini_lat
            (xmap, ymap, zmap, xini, yini) = self.f_get_macro_and_ini()
            xres: float = self.res_dict['lon_']  # Результат Lon
            yres: float = self.res_dict['lat_']  # Результат Lat

            lat_lon_list = self.exract_lat_lon_list(self.res_list)

            (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_map_fw, view_map_fh)
            map_name = 'Участок ' + self.dict_struct["name_sq"]+'. Карта интенсивности I_fact, всех результатов и выбранного результата минимизации'
            self.dialog = CViewMap2(self.master, ss_cvrmap, map_name, root_geometry_string(form_w_, form_h_, addx, addy),
                                    xmap, ymap, zmap, xres, yres, lat_lon_list, False)
            self.dialog.go()

    def calc_view_graph_res_event(self):
        self.f_view_graph_res()

    def calc_view_graph_res_event_btn(self, event):
        self.f_view_graph_res()

    def calc_i_mod_for_res(self, r, mag_:float):
        # I = a∙M –b∙log10R + c
        # вычисление для итоговых значений на основании r - расстояния от гипоцентра
        # Из pinp_struct.objective_function
        # Imod = a*mag_ - b*math.log10(dist3 + 0.0185*pow(10, 0.43*mag_)) + c

        # dat = self.dict_struct['a']*mag_ - self.dict_struct['b']*math.log10(r) + self.dict_struct['c']
        dat = self.dict_struct['a'] * mag_ - self.dict_struct['b'] * math.log10(r + 0.0185*pow(10, 0.43*mag_)) + self.dict_struct['c']
        return dat

    def calc_len_2intens(self, num_res) -> list:
        n = self.dict_struct['npoint']
        spec_list =[[]]*n  # создали список из n пустых списков

        (the_dict, the_arr) = pinp_struct.get_dat_struct(pinp_struct.curr_nstruct)
        d = self.res_list[num_res]
        hypo_lat = d[0]
        hypo_lon = d[1]
        hypo_dep = d[2]
        hypo_mag = d[3]
        # hypo_lat = self.res_dict['lat_']
        # hypo_lon = self.res_dict['lon_']
        # hypo_dep = self.res_dict['dep_']
        # print(hypo_lat,' ',hypo_lon,' ', hypo_dep)
        for i in range(n):
                          # Длина, I_fact, I_mod
            curr_lat = the_arr[i, 0]
            curr_lon = the_arr[i, 1]
            curr_alt = the_arr[i, 2]/1000
            hypo_len = pinp_struct.calc_distance(curr_lat, curr_lon, curr_alt, hypo_lat, hypo_lon, hypo_dep)
            I_fact = the_arr[i, 3]
            I_mod = self.calc_i_mod_for_res(hypo_len, hypo_mag)
            spec_list[i] = [hypo_len, I_fact, I_mod]
        # сортировка по длине
        # https://ru.stackoverflow.com/questions/1066887/Сортировка-двумерного-массива-по-1-элементу
        spec_list.sort(key=lambda x: x[0])
        # print(spec_list)
        return spec_list

    # ToDo 2) Сделать вывод таблицы для num=106 с рассчитанными расстояниями и интенсивностями
    # ToDo 3) Сделать интерактивную страницу с выбором координат, глубин, магнитуд, параметрами макросейсмич. уравнения
    # ToDo 4) На карту исх.данных выводить цифры I_fact точек
    # ToDo 5) На карту результатов выводить цифры I_fact, I_mod точек
    def f_view_graph_res_all(self):
        if self.dict_struct['typeof_input'] != 1:
            mb.showerror(s_error, ss_fdni)
        if self.res_list == []:
            mb.showerror(s_error, ss_ccne)
        else:
            num =0
            spec_list = self.calc_len_2intens(num)
            (x_len, y_i_fact, y_i_mod) = pfunct.list2d3_to_3nparray(spec_list)

            (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_graph_fw, view_graph_fh)
            map_name = 'Участок ' + self.dict_struct["name_sq"]+'. Графики исходной (синий) и расчитанной ' +str(num)+' (краcный) интенсивности'
            self.dialog = CViewGraph(self.master, sc_gres, map_name, root_geometry_string(form_w_, form_h_, addx, addy),
                                    x_len, y_i_fact, y_i_mod)
            self.dialog.go()

    def f_view_graph_res(self):
        if self.dict_struct['typeof_input'] != 1:
            mb.showerror(s_error, ss_fdni)
        if self.res_list == []:
            mb.showerror(s_error, ss_ccne)
        else:
            num = self.res_dict['num']
            spec_list = self.calc_len_2intens(num)
            (x_len, y_i_fact, y_i_mod) = pfunct.list2d3_to_3nparray(spec_list)

            (form_w_, form_h_, addx, addy) = center_form_positioning(self.scr_w, self.scr_h, view_graph_fw, view_graph_fh)
            map_name = 'Участок ' + self.dict_struct["name_sq"]+'. Графики исходной (синий) и расчитанной (краcный) итоговой интенсивности'
            self.dialog = CViewGraph(self.master, sc_gres, map_name, root_geometry_string(form_w_, form_h_, addx, addy),
                                    x_len, y_i_fact, y_i_mod)


    # ---- Подменю Помощь
    def help_about_(self):
        mb.showinfo(sh_about, sh_about1)
        self.change_status_bar1(self.SBC_hab, self.the_status_bar_label1.status_bar)

    def help_usrmanual_(self):
        # Открытие файла в оконном режиме   https://www.cyberforum.ru/python/thread2047476.html
        # Определяем есть ли файл
        path = pathlib.Path(usr_manual_fn_ini)
        if path.is_file():
            os.startfile(usr_manual_fn_ini)
            self.change_status_bar1(self.SBC_hum, self.the_status_bar_label1.status_bar)
        else:
            mb.showerror(s_error, ss_ffne_.center(70) +'\n' + usr_manual_fn_ini)

    # ---- Подменю Помощь "о программе"

    def create_menu(self):
        # ----- Меню
        # https://metanit.com/python/tutorial/9.10.php
        main_menu = Menu()
        # ---- Подменю Файл
        file_menu = Menu(tearoff=0)  #font=("Verdana", 13)
        file_menu.add_command(label=sf_input, command=self.input_inf_)
        file_menu.add_separator()
        file_menu.add_command(label=sf_vinf , command=self.f_view_inf)
        file_menu.add_command(label=sf_vdat , command=self.f_view_dat)
        file_menu.add_command(label=sf_vpar, command=self.f_view_par_minim)
        file_menu.add_command(label=sf_vimap, command=self.f_view_map_ini)
        # file_menu.add_command(label=sf_vimap, command=self.graph)
        file_menu.add_separator()
        file_menu.add_command(label=sf_exit, command=self.file_exit_)
        # ---- Подменю Расчет
        calc_menu = Menu(tearoff=0)
        calc_menu.add_command(label="Расчет", command=self.c_calc_)
        calc_menu.add_command(label=sc_vres, command=self.c_view_main_res) # Просмотр выбранного результата минимизации
        calc_menu.add_separator()
        calc_menu.add_command(label="Карта результатов", command=self.f_view_map_res)
        calc_menu.add_command(label=sc_gres+'               Ctrl-G', command=self.f_view_graph_res) # График расчетной интенсивности
#       calc_menu.add_command(label=sc_gres_all, command=self.f_view_graph_res_all) # Перебор графиков расчетной интенсивности
        calc_menu.add_separator()
        calc_menu.add_command(label="Файл: все результаты минимизации", command=self.c_view_all_res)
        # # ---- Подменю Опции
        # opti_menu = Menu(tearoff=0)
        # opti_menu.add_command(label="Настройка вычислений")
        # opti_menu.add_command(label="Настройка сохранения")
        # ---- Подменю Помощь
        help_menu = Menu(tearoff=0)
        help_menu.add_command(label=sh_usrmanual, command=self.help_usrmanual_)
        help_menu.add_separator()
        help_menu.add_command(label=sh_about, command=self.help_about_)
        # ---- Главное меню
        main_menu.add_cascade(label="Файл", menu=file_menu)
        main_menu.add_cascade(label="Вычисления", menu=calc_menu)
        # main_menu.add_cascade(label="Настройки", menu=opti_menu)
        main_menu.add_cascade(label=sh_help, menu=help_menu)

        return main_menu

# ------------ class MakroseisGUI -------- END


class CViewTxt:
    def __init__(self, master, win_title: str, the_root_geometry_string: str):
        self.slave = Toplevel(master)
        self.slave.iconbitmap(ico_progr)
        self.slave.title(win_title)
        self.slave.geometry(the_root_geometry_string)
        self.frame = Frame(self.slave)
        self.frame.pack(side=BOTTOM)
        # Python - Tkinter Text
        # https://www.tutorialspoint.com/python/tk_text.htm
        self.text = Text(self.slave, background='white', exportselection=0)  #
        self.text.pack(side=TOP, fill=BOTH, expand=YES)

    def go(self, my_text=''):
        self.text.insert('0.0', my_text)
        self.newValue = None
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()

class CViewGraph:
    # https://ru.stackoverflow.com/questions/602148/Отрисовка-графиков-посредством-matplotlib-в-окне-tkinter
    def __init__(self, master, win_title: str, map_name:str, the_root_geometry_string: str,
                 x_len, y_i_fact, y_i_mod):
        self.slave = Toplevel(master)
        self.slave.iconbitmap(ico_progr)
        self.slave.title(win_title)
        self.slave.geometry(the_root_geometry_string)
        self.frame = Frame(self.slave)
        self.frame.pack(side=BOTTOM)

        # self.frame.fig = mpl.figure.Figure(figsize=(5, 5), dpi=100)
        # self.frame.a = self.frame.fig.add_subplot(111)
        # self.frame.a.plot(x_len, y_i_fact , color = 'blue')
        # self.frame.a.plot(x_len, y_i_mod , color = 'red')
        # self.frame.a.set_title(map_name)

        self.frame.fig,  self.frame.ax   = plt.subplots(nrows=1)
        self.frame.ax.plot(x_len, y_i_fact , color = 'blue')
        self.frame.ax.plot(x_len, y_i_mod  , color = 'red')
        self.frame.ax.set_title(map_name, fontsize=15, fontname='Times New Roman')
        self.frame.ax.set_xlabel('Расстояние от гипоцентра, км')
        self.frame.ax.set_ylabel('Интенсивность')
        self.frame.ax.grid()

        self.frame.canvas = FigureCanvasTkAgg(self.frame.fig, self.slave)
        self.frame.canvas.draw()
        self.frame.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.frame.canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)

    def go(self):
        self.newValue = None
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()

class CViewMap2:
    # https://ru.stackoverflow.com/questions/602148/Отрисовка-графиков-посредством-matplotlib-в-окне-tkinter
    def __init__(self, master, win_title: str, map_name:str, the_root_geometry_string: str,
                 xmap: np.ndarray, ymap: np.ndarray, zmap: np.ndarray, xini: float, yini: float, lat_lon_list: list, is_ini_map1):
        self.is_ini_map = is_ini_map1
        self.slave = Toplevel(master)
        self.slave.iconbitmap(ico_progr)
        self.slave.title(win_title)
        self.slave.geometry(the_root_geometry_string)
        self.frame = Frame(self.slave)
        self.frame.pack(side=BOTTOM)

        # self.frame.fig = mpl.figure.Figure(figsize=(5, 5), dpi=300)
        # self.frame.a = self.frame.fig.add_subplot(111)
        # self.frame.a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        # self.frame.canvas = FigureCanvasTkAgg(self.frame.fig, self.slave)
        # self.frame.canvas.draw()
        # self.frame.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        # self.frame.canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.frame.fig,  self.frame.ax2   = plt.subplots(nrows=1)
        self.frame.ax2.tricontour(xmap, ymap, zmap, levels=14, linewidths=0.5, colors='k')
        cntr2 = self.frame.ax2.tricontourf(xmap, ymap, zmap, levels=14, cmap="RdBu_r")
        if lat_lon_list != None:  # Карта результатов
            # print('---- lat_lon_list -----')
            n = len(lat_lon_list)
            # print(n)
            for i in range(n):
                xmap1 = float(lat_lon_list[i][1])
                ymap1 = float(lat_lon_list[i][0])
                # print()
                self.frame.ax2.plot(xmap1, ymap1, 'o', ms=4, color="yellow")  # green

        if self.is_ini_map: # Карта исходных данных
            (lat_arr, lon_arr, ifact_arr) = pinp_struct.get_Lat_Lon_ifact()
            n = len(lat_arr)
            for i in range(n):
                xmap1 = float(lon_arr[i])
                ymap1 = float(lat_arr[i])
                zmap1 = float(ifact_arr[i])
                # https://pythonru.com/biblioteki/pyplot-uroki
                self.frame.ax2.text(xmap1, ymap1, format(zmap1,'2.1f'), fontsize=6)  # green


        self.frame.fig.colorbar(cntr2, ax=self.frame.ax2)
        self.frame.ax2.plot(xini, yini, 'o', ms=12, color = "red")  #ko
        self.frame.ax2.plot(xmap, ymap, 'o', ms=3, color = "orange") #
        self.frame.ax2.set(xlim=(min(xmap), max(xmap)), ylim=(min(ymap), max(ymap)))
        self.frame.ax2.set_title(map_name, fontsize=15, fontname='Times New Roman')
        self.frame.ax2.grid()
        # self.frame.a = self.frame.fig.add_subplot(111)
        # self.frame.a.draw()
        self.frame.canvas = FigureCanvasTkAgg(self.frame.fig, self.slave)
        self.frame.canvas.draw()
        self.frame.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        self.frame.canvas._tkcanvas.pack(side=BOTTOM, fill=BOTH, expand=True)

    def go(self):
        self.newValue = None
        self.slave.grab_set()
        self.slave.focus_set()
        self.slave.wait_window()


class CViewMap3:  # Рисование на главном окне
    # https://ru.stackoverflow.com/questions/602148/Отрисовка-графиков-посредством-matplotlib-в-окне-tkinter
    def __init__(self, master):
        self.fig = mpl.figure.Figure(figsize=(5, 5), dpi=300)
        self.a = self.fig.add_subplot(111)
        self.a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)


# def btn_esc(event):             ## ========= Выход
#     sys.exit(0)
#     # root.bind('<Escape>', btn_esc)

def the_program() -> None:
    # ----- Инициализация, начальные установки окна
    root = Tk()
#   root.bind('<Escape>', btn_esc)  ## ========= Выход
    makroseis = MakroseisGUI(root)
    makroseis.mainloop()
    # root.mainloop()
