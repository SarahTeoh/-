# -*- coding: utf-8 -*
import tkinter as tk
from tkinter import *
from tkinter import ttk
import time

PRACTICETIME=120

class App(tk.Tk):   
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self,"PreSys")

        self.container = tk.Frame(self, height = 1000, width =1000)
        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SignInPage, StartPage):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SignInPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        """if cont == PracticePage:
            frame.remaining = PRACTICETIME
            frame.setTimeLeft()"""
        frame.tkraise()   

    def create_practicePage(self,cont):
        frame = PracticePage(self.container, self)

        self.frames[PracticePage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PracticePage)


class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        self.label = tk.Label(self,text = "名前を入力してください")
        self.entry_name = tk.Entry(self)
        self.signinButton = ttk.Button(self, text="サインイン", command = lambda: controller.show_frame(StartPage))#, command=record)

        self.label.grid(row=0) 
        self.entry_name.grid(row=0, column=1)
        self.signinButton.grid(row=1, column=1) 


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        self.label = tk.Label(self,text = "スタートボタンを押してプレゼンテーションを始めてください")
        self.startButton = ttk.Button(self, text="スタート", command = lambda: controller.create_practicePage(PracticePage))

        self.label.pack()
        self.startButton.pack()

class PracticePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.timeLeft = tk.Label(self,text= "")
        self.backButton = ttk.Button(self, text="やり直す", command = lambda: controller.show_frame(StartPage))
        self.homeButton = ttk.Button(self, text="サインアウト", command = lambda: controller.show_frame(SignInPage))
        
        self.timeLeft.pack()
        self.backButton.pack()
        self.homeButton.pack()
        
        self.remaining = 0
        self.countdown(120)

    def countdown(self, remaining = None):
        if remaining is not None:
            self.remaining = remaining

        if self.remaining <= 0:
            self.timeLeft.configure(text="お疲れ様です！")
        else:
            mins, secs = divmod(self.remaining,60)
            mins = round(mins)
            secs = round(secs)
            self.timeLeft.configure(text=str(mins) +"分"+ str(secs) +"秒")
            self.remaining = self.remaining - 1
            self.after(1000, self.countdown)

apps = App()
apps.mainloop()
