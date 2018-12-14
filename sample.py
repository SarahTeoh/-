#出てくるウインドウズの制御プログラム
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import time
import sys
import transcribe_streaming_mic
import stream_infinite #音声認識と話速度を出すmic.py 
import scoring

#発表時間3分にする
PRACTICETIME = 10

class App(tk.Tk):   
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = tk.Frame(self, height = 50000, width = 50000, bg = "white")
        self.container.pack(side="top", fill="both", expand = True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
         
        self.create_windows(SignInPage, 0, 0)

    #ページの切り替え
    def create_windows(self, cont, speechrate, pitch):
        if cont is ResultPage:
            frame = cont(self.container, self, speechrate, pitch)
        else:
            frame = cont(self.container, self)
        self.frames[cont] = frame
        frame.grid(row = 0, column = 0, sticky="nsew")
        frame.tkraise()
    
#ユーザー名を入力し、サインインてもらう
class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg="white")

        self.logo = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo.png")
        self.logo_image = tk.Label(self, image = self.logo, bg ="white")
        
        self.entry_name = tk.Entry(self, borderwidth=0, font = "遊ゴジックLight 15",bg = "gray95", justify = "center")
        self.entry_name.delete(0, END)
        self.entry_name.insert(0, "名前を入力してください")
        self.signinButton = tk.Button(self, text="ログイン",  font ="遊ゴジックLight 17", borderwidth=0, bg ="light blue", command = lambda: controller.create_windows(StartPage, 0, 0))

        self.logo_image.place(relwidth = 0.4, relheight = 0.4, relx = 0.5, rely = 0.2, anchor = "center")
        self.entry_name.place(relwidth = 0.6, relheight = 0.08, relx = 0.5, rely = 0.65, anchor ="center")
        self.signinButton.place(relwidth = 0.6, relheight = 0.09, relx = 0.5, rely = 0.75,  anchor ="center")

#練習に入る前のページ
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg="white")

        self.logo_image = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo.png")
        self.logo = tk.Label(self, image = self.logo_image, bg ="white")
        self.label = tk.Label(self,text = "スタートボタンを押してプレゼンテーションを始めてください", font ="遊ゴジックLight 15 bold", bg ="white")
        self.startButton_image = PhotoImage(file="C:/Users/Programming exp/Desktop/研究/卒研レジュメ/digram(jpeg&photoshop)/play_button.png")
        self.startButton = tk.Button(self, text="スタート", bg ="white", image = self.startButton_image, borderwidth=0, command = lambda: controller.create_windows(PracticePage, 0, 0))
        
        self.logo.place(relwidth = 0.4, relheight = 0.4, relx = 0.5, rely = 0.2, anchor = "center")
        self.label.place(relwidth = 0.8, relheight = 0.4, relx = 0.5, rely = 0.5, anchor = "center")
        self.startButton.place(relwidth = 0.8, relheight = 0.4, relx = 0.5, rely = 0.8, anchor = "center")

#練習しているウィンドウズ
class PracticePage(tk.Frame, App):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg="white")

        self.controller = controller
        self.logo = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo_small.png")
        self.logo_image = tk.Label(self, image = self.logo, bg ="white")
        self.timeLeft = tk.Label(self, text= "", font ="遊ゴジックLight 20 bold", bg ="white")
        self.comment = tk.Label(self, text= "", font ="遊ゴジックLight 20 bold", bg ="white")
        self.backButton = tk.Button(self, text="やり直す", borderwidth=0,   font ="遊ゴジックLight 17", bg ="light blue", command = lambda: controller.create_windows(StartPage, 0, 0))
        self.homeButton = tk.Button(self, text="サインアウト", borderwidth=0, font ="遊ゴジックLight 17", bg ="powder blue", command = lambda: controller.create_windows(SignInPage, 0, 0))
        #TODO:backButtonかhomeButtonが押されたら音声認識、録音などをやり直す

        self.logo_image.place(relwidth = 0.4, relheight = 0.9, relx = 0.5, rely = 0.2, anchor = "center")
        self.timeLeft.place(relwidth = 0.4, relheight = 0.1, relx = 0.5, rely = 0.45, anchor = "center")
        self.comment.place(relwidth = 0.4, relheight = 0.1, relx = 0.5, rely = 0.65, anchor = "center")
        self.backButton.place(relwidth = 0.6, relheight = 0.09, relx = 0.5, rely = 0.8, anchor = "center")
        self.homeButton.place(relwidth = 0.6, relheight = 0.09, relx = 0.5, rely = 0.9, anchor = "center")
        
        #発表の残り時間
        self.remaining = 0
        
        #カウントダウンと録音の同時実行
        self.thread1 = threading.Thread(target = stream_infinite.run)
        self.thread2 = threading.Thread(target = self.countdown,args=[PRACTICETIME])
            
        #ウィンドウズを閉じたらスレッドも止まるようにする
        self.thread1.setDaemon(True)
        self.thread2.setDaemon(True)

        self.thread1.start()
        self.thread2.start()

    #残り時間を表示する
    def countdown(self, remaining = None): 
            if remaining is not None:
                self.remaining = remaining

            if self.remaining <= 0:
                transcribe_streaming_mic.close = True
                self.timeLeft.configure(text="お疲れ様です！")
                self.after(2000, self.show_result) 

            else: 
                mins, secs = divmod(self.remaining,60)
                mins = round(mins)
                secs = round(secs)
                self.timeLeft.configure(text=str(mins) +"分"+ str(secs) +"秒")
                if self.remaining == 7:
                    first_min_rate = transcribe_streaming_mic.num_chars_printed
                    print(first_min_rate)
                    self.set_comment(first_min_rate)
                elif self.remaining == 3:
                    second_min_rate = transcribe_streaming_mic.num_chars_printed
                    print(second_min_rate)
                    self.set_comment(second_min_rate)
                self.remaining = self.remaining - 1
                self.after(1000, self.countdown)   
    
    def set_comment(self, rate):
        self.comment.configure(text=scoring.speechRateComment(rate))
        self.after(2000, self.erase_comment)

    def erase_comment(self):        
        self.comment.configure(text="")

    def show_result(self):
        speechrate = transcribe_streaming_mic.rate 
        #pitch =　
        #score = 
        self.controller.create_windows(ResultPage, speechrate, 0)  #採点結果ページResultPageの表示

#点数とコメントウインドウズ
class ResultPage(tk.Frame):
    def __init__(self, parent, controller, speechrate, pitch):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg="white")

        self.logo = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo.png")
        self.logo_image = tk.Label(self, image = self.logo)
        self.result_title = tk.Label(self,text= "採点結果")
        self.speechrate_label = tk.Label(self, text= "話速度")
        self.speechrate = tk.Label(self, text= speechrate) #TODO:take mark and comment from scoring.py
        self.pitch_label = tk.Label(self, text= "声の高さ")
        self.pitch = tk.Label(self, text= pitch) 
        self.mark_label = tk.Label(self, text= "点数")
        self.mark = tk.Label(self, text = "")
        self.comment_label = tk.Label(self, text= "コメント")
        self.comment = tk.Label(self, text = "")
        
        self.logo_image.place(relwidth = 0.4, relheight = 0.4, relx = 0.5, rely = 0.2, anchor = "center")
        self.result_title.grid(row=0, columnspan=2)
        self.speechrate_label.grid(row=1, column=0)
        self.speechrate.grid(row=1, column=1)
        self.pitch_label.grid(row=2, column=0)
        self.pitch.grid(row=2, column=1)
        self.mark_label.grid(row=3, column=0)
        self.mark.grid(row=3, column=1)
        self.comment_label.grid(row=4, column=0)
        self.comment.grid(row=4, column=1)

def end_fullscreen(event=None):
    apps.attributes("-fullscreen", False)

def quit(event=None):
    apps.destroy()

apps = App()
apps.configure(bg="white")
apps.attributes("-fullscreen", True) #フールスクリーンモード
apps.bind("<Escape>", quit)     #escキーを押すとウインドウズ閉じる
apps.bind("<Tab>", end_fullscreen)  #Tabキーを押すとフールスクリーンモードを終了
apps.mainloop()

