"""
Разные дополнительные средства для tkinter

(C) 2020 Ivan Genik, Perm, Russia
Released under GNU Public License (GPL)
email igenik@rambler.ru
"""
# Graphical User Interfaces with Tk
# https://docs.python.org/3/library/tk.html
# tkinter — Python interface to Tcl/Tk
# https://docs.python.org/3/library/tkinter.html

# import ctypes
from tkinter import *


def the_change_progr_ico(the_root) -> None:
    """
    Смена иконки программы
    Как поставить свою цветную иконку на программу написанную на tkinter?
    https://ru.stackoverflow.com/questions/797093/Как-поставить-свою-цветную-иконку-на-программу-написанную-на-tkinter
    """
    the_root.iconbitmap(r'graphics\Земл144.ico')


def get_screen_size(tkinter_Tk) -> (int, int):
    """
    Определение средствами tkinter ширины и высоты экрана
    https://askdev.ru/q/kak-poluchit-razreshenie-monitora-v-python-33296/
    Как получить разрешение монитора в Python?
    https://askdev.ru/q/kak-poluchit-razreshenie-monitora-v-python-33296/

    return: screen_width screen_height
    """
    # user32 = ctypes.windll.user32
    # the_screen_width = user32.GetSystemMetrics(0) # 1920 # tkinter.Tk().winfo_screenwidth()
    # the_screen_height = user32.GetSystemMetrics(1) # 1080 # tkinter.Tk().winfo_screenheight()
    the_screen_width = tkinter_Tk.winfo_screenwidth()
    the_screen_height = tkinter_Tk.winfo_screenheight()
    return the_screen_width, the_screen_height


def center_form_positioning(scr_w: int, scr_h: int, pr_width: int, pr_height: int) -> (int, int, int, int):
    """
    Позиционирование любой формы по центру экрана
    return: параметры w_, h_, add_width_, add_height_ для root.geometry("w_xh_+add_width_+add_height_")
    """
    add_width_: int
    add_height_: int
    if pr_width >= scr_w:
        add_width_ = 0
        w_ = scr_w
    else:
        add_width_ = (scr_w-pr_width) // 2
        w_ = pr_width

    if pr_height >= scr_h:
        add_height_ = 0
        h_ = scr_h
    else:
        add_height_ = round((scr_h-pr_height) / 2.5)
        h_ = pr_height
    return w_, h_, add_width_, add_height_


def mainform_positioning(tkinter_Tk, pr_width: int, pr_height: int) -> (int, int, int, int, int, int):
    """
    Позиционирование главной формы по центру экрана
    return: параметры w_, h_, add_width_, add_height_ для root.geometry("w_xh_+add_width_+add_height_")
    """
    add_width_: int
    add_height_: int
    (scr_w, scr_h) = get_screen_size(tkinter_Tk)
    if pr_width >= scr_w:
        add_width_ = 0
        w_ = scr_w
    else:
        add_width_ = (scr_w-pr_width) // 2
        w_ = pr_width

    if pr_height >= scr_h:
        add_height_ = 0
        h_ = scr_h
    else:
        add_height_ = round((scr_h-pr_height) / 2.5)
        h_ = pr_height
    return scr_w, scr_h, w_, h_, add_width_, add_height_


def root_geometry_string(form_w_: int, form_h_: int, x: int, y: int) -> str:
    """
    Форматирование строки для root.geometry("form_w_xform_h_+x+y")
    """
    s = str(form_w_)+"x"+str(form_h_)+"+"+str(x)+"+"+str(y)
    return s


def root_geometry_string_auto(tkinter_Tk, form_w_: int, form_h_) -> str:
    """
    Форматирование строки для root.geometry("form_w_xform_h_+x+y")
    """
    (form_w_, form_h_, addx, addy) = mainform_positioning(tkinter_Tk, form_w_, form_h_)
    s = str(form_w_)+"x"+str(form_h_)+"+"+str(addx)+"+"+str(addy)
    return s

# ---------------------- Тесты -------------------
# def test_get_screen_size(tkinter_Tk)-> None:
#     (screen_width, screen_height) = get_screen_size(tkinter_Tk)
#     print('screen_width = ', screen_width)
#     print('screen_height = ',screen_height)
#
#
# def all_test():
#     root = Tk()
#     test_get_screen_size(root)
#     form_w_: int=1400
#     form_h_: int=900
#     print('1-этапный расчет = ',root_geometry_string_auto(root, form_w_, form_h_))
#
#     (form_w_, form_h_, addx, addy) = mainform_positioning(root, form_w_, form_h_)
#     s:str=root_geometry_string(form_w_, form_h_, addx, addy)
#     print('2-этапный расчет = ',s)

# all_test()
# test_get_screen_size()
