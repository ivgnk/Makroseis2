import os
import winsound

from PIL import Image, ImageTk
from tkinter import *

# from tkinter import Tk, Frame, Menu, Button
# from tkinter import LEFT, TOP, X, FLAT, RAISED

import pbutton

class Example(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    # def create_button1(self, icofilename, the_command, the_toolbar):
    #     self.img = Image.open(icofilename)
    #     eimg = ImageTk.PhotoImage(self.img)
    #     the_Button = Button(
    #         the_toolbar, image=eimg, relief=FLAT,
    #         command=the_command
    #     )
    #     the_Button.image = eimg
    #     the_Button.pack(side=LEFT, padx=2, pady=2)

    def command1(self):
        print('\a')


    def command2(self):
        frequency = 250  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second
        winsound.Beep(frequency, duration)


    def initUI(self):
        self.master.title("Панель инструментов")
        self.create_button1 = pbutton.create_button

        menubar = Menu(self.master)
        self.fileMenu = Menu(self.master, tearoff=0)
        self.fileMenu.add_command(label="Выход", command=self.onExit)
        menubar.add_cascade(label="Файл", menu=self.fileMenu)

        toolbar = Frame(self.master, bd=1, relief=RAISED)
        self.create_button1(self, 'E:\Work_Lang\Python\PyCharm\Tkinter\Ico\exit.png', self.quit, toolbar)
        self.create_button1(self, 'E:\Work_Lang\Python\PyCharm\Tkinter\Ico\Info.png', self.command1, toolbar)
        self.create_button1(self, 'E:\Work_Lang\Python\PyCharm\Tkinter\Ico\Ball1.png', self.command2, toolbar)

        toolbar.pack(side=TOP, fill=X)
        self.master.config(menu=menubar)
        self.pack()

    def onExit(self):
        self.quit()


def the_main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example()
    root.mainloop()

the_main()