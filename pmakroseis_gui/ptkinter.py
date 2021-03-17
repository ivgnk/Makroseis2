from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import scrolledtext as st

from typing import Any
import Pmw
import ptkinter_menu_proc

from ptkintertools import *
# from pmakroses_proc import *
from dataclasses import dataclass
from ptkinter_menu_proc import *

from PIL import Image, ImageTk
import os, sys
import winsound
#------ Из Makro_seis
import pfile, pinp_proc
# import pinp_struct

p_width:int = 1400 # ширина окна программы
p_height:int = 900  # высота окна программы

vf_width:int = 700 # ширина окна просмотра
vf_height:int = 700  # высота окна программы

status_bar_width = 220
status_bar_height = 20

#  1 июля 2018 Введение в Data classes (Python 3.7)
#  https://habr.com/ru/post/415829/
@dataclass
class status_bar_label:
    status_bar: Any
    the_status: int


# ----------- Источники
# Создание графического интерфейса https://metanit.com/python/tutorial/9.1.php
# Диалоговые (всплывающие) окна / tkinter 9 https://pythonru.com/uroki/dialogovye-vsplyvajushhie-okna-tkinter-9

# ----------- ООП
# Библиотека Tkinter - 9 - Использование ООП
# https://www.youtube.com/watch?v=GhkyLQ6A6Yw&list=PLfAlku7WMht4Vm6ewLgdP9Ou8SCk4Zhar&index=9

class MakroseisGUI(Frame):
    # Константы для смены надписей в StatusBar
    SBC_st = 0    # Программа запущена
    SBC_fdni =10  # Данные не введены
    SBC_fdi = 11  # Данные введены
    SBC_fvpar = 14 # Просмотр параметров минимизации
    SBC_ce = 22  # Вычисление закончено
    SBC_cc = 22  # Вычисление прервано
    SBC_hab = 41  # О программе
    SBC_hum = 42  # Руководство пользователя
    SBC_ns = 50

    is_input_inf = False;     fn_current_inf=''    # текущий inf-файл
    is_input_txt = False;     fn_current_txt =''   # текущий txt-файл
    is_input_xlsx = False;    fn_current_xlsx =''  # текущий xlsx-файл
    is_exist_resf = False;    fn_current_resf =''  # текущий res-файл
    fn_inf = ''
    dn_current_dir=''
    dn_current_dat_dir=''
    # Константы меня
    def __init__(self, main):
        super().__init__(main)
        # the_status_bar_label1   # 0 - Начата работа программы        # 1 - Данные введены
                                  # 2 - Вычисление закончено           # 3 - Вычисление прервано
        self.the_status_bar_label1 = status_bar_label(status_bar = Label(main, text=" Программа запущена ", bd=1, relief=SUNKEN, anchor=W), the_status=0)
        self.the_status_bar_label2 = status_bar_label(status_bar = Label(main, text="                    ", bd=1, relief=SUNKEN, anchor=W), the_status=0)
        self.the_status_bar_label3 = status_bar_label(status_bar = Label(main, text="                    ", bd=1, relief=SUNKEN, anchor=W), the_status=0)
        main.title(win_name)
        (form_w_, form_h_, addx, addy) = mainform_positioning(main, p_width, p_height)
        # main.geometry(root_geometry_string_auto(main, p_width, p_heiht)) # 1920x1080 мой монитор
        main.geometry(root_geometry_string(form_w_, form_h_, addx, addy))
        # Python Tkinter, как запретить расширять окно программы на полный экран?
        # https://otvet.mail.ru/question/191704214
        main.resizable(width=False, height=False)
        main.config(menu=self.create_menu())
        main.iconbitmap(ico_progr)
        # self.the_status_bar_label1.status_bar.pack(side=LEFT, fill=X)
        # self.the_status_bar_label2.status_bar.pack(side=LEFT, fill=X)
        #-------- Создание Status bar
        rest_width = form_w_ - (2*(status_bar_width+2+2))
        self.the_status_bar_label1.status_bar.place(x=1,                     y=form_h_-status_bar_height-3, width=status_bar_width, height=status_bar_height)
        self.the_status_bar_label2.status_bar.place(x=status_bar_width+2,    y=form_h_-status_bar_height-3, width=status_bar_width, height=status_bar_height)
        self.the_status_bar_label3.status_bar.place(x=2*(status_bar_width+2),y=form_h_-status_bar_height-3, width=rest_width, height=20)
        #-------- Создание панели инструментов
        # Меню, подменю и панель инструментов в Tkinter
        # https://python-scripts.com/tkinter-menu-toolbars-example

        # Pmw.Balloon
        # http://pmw.sourceforge.net/doc/Balloon.html
        self.balloon = Pmw.Balloon(main)
        self.create_tool_bar(main)
        # toolbar = Frame(main, bd=1, relief=RAISED)
        # self.create_button1('E:\Work_Lang\Python\PyCharm\Tkinter\Ico\exit.png', self.command1, toolbar)
        # self.create_button1('E:\Work_Lang\Python\PyCharm\Tkinter\Ico\Info.png', self.command2, toolbar)
        # self.create_button1('E:\Work_Lang\Python\PyCharm\Tkinter\Ico\Ball1.png', self.command3, toolbar)
        # toolbar.pack(side=TOP, fill=X)

        # Определяем текущую папку с программой https://ru.stackoverflow.com/questions/535318/Текущая-директория-в-python
        self.dn_current_dir =os.getcwd()
        self.dn_current_dat_dir = "\\".join([self.dn_current_dir, dat_dir])
        # print(self.dn_current_dir)


    def create_tool_bar(self, main):
        toolbar = Frame(main, bd=1, relief=RAISED)
        # https://icon-icons.com/ru/download/
        # полный формат ввода иконки 'E:\Work_Lang\Python\PyCharm\Tkinter\Ico\play_22349.png
        self.create_button1(ico_file_open_ , self.file_open_, toolbar, 'Открыть файл данных')
        self.create_button1(ico_calc_, self.cmd_calc, toolbar, 'Расчет')
        self.create_button1(ico_resmap_, self.cmd_calc_resmap, toolbar, 'Карта результатов')
        self.create_button1(ico_resgraph_, self.cmd_calc_resmap, toolbar, 'График результатов')
        self.create_button1(ico_usrmanual_ , self.help_usrmanual_, toolbar, sh_usrmanual)
        toolbar.pack(side=TOP, fill=X)


    def change_status_bar1(self, status, status_bar):
        self.the_status = status
        if status == self.SBC_st:
            status_bar['text'] = 'Программа запущена'
        elif status == self.SBC_fdi:
            status_bar['text'] = ss_fdi
        elif status == self.SBC_fdni:
            status_bar['text'] = ss_fdni
        elif status == self.SBC_fvpar:
            status_bar['text'] =sf_vpar
        elif status == self.SBC_ce:
            status_bar['text'] = 'Вычисление закончено'
        elif status == self.SBC_cc:
            status_bar['text'] = 'Вычисление прервано'
        #---- Подменю Помощь
        elif status == self.SBC_hab:
            status_bar['text'] = sh_about
        elif status == self.SBC_hum:
            status_bar['text'] = sh_usrmanual
        else:
            status_bar['text'] = 'Неопределенный статус'

    #---- Панель инструментов
    def create_button1(self, icofilename:str, the_command, the_toolbar, the_hint):
        """
        Создание кнопки
        """
        self.img = Image.open(icofilename)
        eimg = ImageTk.PhotoImage(self.img)
        the_Button = Button(
            the_toolbar, image=eimg, relief=FLAT,
            command=the_command
        )
        the_Button.image = eimg
        the_Button.pack(side=LEFT, padx=2, pady=2)
        self.balloon.bind(the_Button, the_hint)

    # def cmd_open(self):  winsound.Beep(frequency=150, duration=1000)

    def cmd_calc(self):
        winsound.Beep(frequency=200, duration=1000)

    def cmd_calc_resmap(self):
        winsound.Beep(frequency=250, duration=1000) # Set Duration To 1000 ms == 1 second

    def input_from_inf(self, fname:str)->bool:
        good_end = pinp_proc.the_input(fname = fname,  is_view = False)
        return good_end
        # return True

    def input_from_txt(self, fname:str)->bool:
        pass

    def input_from_xlsx(self, fname:str)->bool:
        pass


    #---- Подменю Файл
    def file_open_(self):
        # print('file_open_()')
        ext_type=''
        good_new_data = ''

        fn_dat = fd.askopenfilename(initialdir=self.dn_current_dat_dir,
            defaultextension='.inf', filetypes=[('inf файлы','*.inf'), ('txt файлы','*.txt'),
                                                ('xlsx файлы','*.xlsx'), ('Все файлы','*.*')])
        the_ext = pfile.gfe(fn_dat)
        if the_ext=='.inf':
            ext_type = 'i'
            good_new_data = self.input_from_inf(fn_dat)
        elif the_ext=='.txt':
            ext_type = 't'
            good_new_data = self.input_from_txt(fn_dat)
        elif the_ext=='.xlsx':
            ext_type = 'x'
            good_new_data = self.input_from_xlsx(fn_dat)
        elif the_ext == '':
            ext_type = ''
        else:
            ext_type = 'n'
            mb.showerror(s_error, sf_err_ext)

        if (ext_type == ''):
            #self.change_status_bar1(self.SBC_fdni, self.the_status_bar_label1.status_bar)
            # self.the_status_bar_label3.status_bar['text'] = ''
            pass
        elif (ext_type == 'n'):
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

    def input_inf(self):
       # (good_end, thecurr_dict) = pinp_struct.input_inf(self.fn_inf)
        pass


    def view_file(self, fname:str):
        # (form_w_, form_h_, addx, addy) = mainform_positioning(self, p_width, p_height)
        # # main.geometry(root_geometry_string_auto(main, p_width, p_heiht)) # 1920x1080 мой монитор
        # self.geometry(root_geometry_string(form_w_, form_h_, addx, addy))
        # # Python Tkinter, как запретить расширять окно программы на полный экран?
        # # https://otvet.mail.ru/question/191704214
        # self.self.resizable(width=False, height=False)
        #
        #
        #
        # txt = st.ScrolledText(window, width=40, height=10)
        # txt.insert(INSERT, 'Текстовое поле')
        # txt.grid(column=0, row=0)
        pass

    def input_txt(self):
        pass

    def input_xlsx(self):
        pass

    def view_inf(self):

        pass

    def view_txt(self):
        pass

    def view_xlsx(self):
        pass

    def view_par(self):
        pass
        # self.change_status_bar1(self.SBC_fvpar, self.the_status_bar_label1.status_bar)



    def file_exit_(self):
        # https: // ru.stackoverflow.com / questions / 459170 /
        sys.exit(0)

    #---- Подменю Расчет
    def calc_calc_(self):
        self.change_status_bar1(self.SBC_ce, self.the_status_bar_label1.status_bar)
        # print(self.the_status)

    #---- Подменю Помощь
    def help_about_(self):
        mb.showinfo(sh_about, sh_about1)
        self.change_status_bar1(self.SBC_hab, self.the_status_bar_label1.status_bar)

    def help_usrmanual_(self):
        # Открытие файла в оконном режиме   https://www.cyberforum.ru/python/thread2047476.html
        os.startfile(usr_manual_fn)
        self.change_status_bar1(self.SBC_hum, self.the_status_bar_label1.status_bar)

    # ---- Подменю Помощь "о программе"

    def create_menu(self):
        #----- Меню
        # https://metanit.com/python/tutorial/9.10.php
        main_menu = Menu()
        #---- Подменю Файл
        file_menu = Menu(tearoff=0) #font=("Verdana", 13)
        file_menu.add_command(label=sf_input, command=self.file_open_)
        file_menu.add_command(label=sf_vinf , command=self.view_inf)
        file_menu.add_command(label=sf_vdat)
        file_menu.add_command(label=sf_vpar, command=self.view_par)
        file_menu.add_command(label=sf_vimap)
        file_menu.add_separator()
        file_menu.add_command(label=sf_exit, command=self.file_exit_)
        # ---- Подменю Расчет
        calc_menu = Menu(tearoff=0)
        calc_menu.add_command(label="Расчет", command=self.calc_calc_)
        calc_menu.add_separator()
        calc_menu.add_command(label="Карта результатов")
        calc_menu.add_command(label="График расчетной интенсивности")
        calc_menu.add_command(label="Просмотр всех результатов")
        # ---- Подменю Опции
        opti_menu = Menu(tearoff=0)
        opti_menu.add_command(label="Настройка вычислений")
        opti_menu.add_command(label="Настройка сохранения")
        # ---- Подменю Помощь
        help_menu = Menu(tearoff=0)
        help_menu.add_command(label=sh_usrmanual, command=self.help_usrmanual_)
        help_menu.add_command(label=sh_about, command=self.help_about_)
        # ---- Главное меню
        main_menu.add_cascade(label="Файл", menu=file_menu)
        main_menu.add_cascade(label="Вычисления", menu=calc_menu)
        main_menu.add_cascade(label="Настройки", menu=opti_menu)
        main_menu.add_cascade(label=sh_help, menu=help_menu)

        return main_menu
# ------------ class MakroseisGUI -------- END

def btn_esc(event):
    sys.exit(0)


# Строка статуса
# https://www.delftstack.com/ru/tutorial/tkinter-tutorial/tkinter-status-bar/

def the_program() -> None:
    #----- Инициализация, начальные установки окна
    root = Tk()
    root.bind('<Escape>', btn_esc)
    Makroseis = MakroseisGUI(root)
    root.mainloop()


#============= Команды

# from tkinter import *
# root = Tk()
# root.geometry('350x350')
# # Button(bg='red').place(x=75, y=20)
# Label(bg='red').place(x=0, y=318, width=50, height=30)
# Label(bg='green').place(x=52, y=318, width=50, height=30)
# root.mainloop()

