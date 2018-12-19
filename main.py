#出てくるウインドウズの制御プログラム
import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import time
import sys
from playsound import playsound
import numpy
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import transcribe_streaming_mic
import stream_infinite  
import fundamental_freq
import scoring
#発表時間3分にする
PRACTICETIME = 180

class App(tk.Tk):   
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.container = tk.Frame(self, height=2000, width = 1000, bg = "white")
        self.container.pack(side="top", fill="both", expand = True)
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
         
        self.create_windows(SignInPage)

    #ウインドウズの切り替え
    def create_windows(self, cont):
        frame = cont(self.container, self)
        self.frames[cont] = frame
        frame.grid(row = 0, column = 0, sticky="nsew")
        frame.tkraise()
    
#ユーザー名を入力し、サインインてもらう
class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, height = 600, width = 700, bg="white")

        self.logo = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo.png") 
        self.logo_image = tk.Label(self, image = self.logo, bg ="white", borderwidth = 0)
        
        self.entry_name = tk.Entry(self, borderwidth=0, font = "遊ゴジックLight 25",bg = "gray95", justify = "center")
        self.entry_name.delete(0, END)
        self.entry_name.insert(0, "名前を入力してください")
        self.signinButton = tk.Button(self, text="ログイン",  font ="遊ゴジックLight 30", borderwidth=0, bg ="light blue", command = lambda: controller.create_windows(StartPage))

        self.logo_image.place(relx = 0.5, rely = 0.2, anchor = "center")
        self.entry_name.place(relwidth = 0.6, relheight = 0.08, relx = 0.5, rely = 0.65, anchor ="center")
        self.signinButton.place(relwidth = 0.6, relheight = 0.09, relx = 0.5, rely = 0.75,  anchor ="center")

#練習に入る前のページ
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg="white")

        self.logo_image = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo.png")
        self.logo = tk.Label(self, image = self.logo_image, bg ="white", borderwidth = 0)
        self.label = tk.Label(self,text = "スタートボタンを押しててください", font ="遊ゴジックLight 25 bold", bg ="white")
        self.startButton_image = PhotoImage(file="C:/Users/Programming exp/Desktop/研究/卒研レジュメ/digram(jpeg&photoshop)/play_button.png")
        self.startButton = tk.Button(self, text="スタート", bg ="white", image = self.startButton_image, borderwidth=0, command = lambda: controller.create_windows(PracticePage))
        
        self.logo.place(relx = 0.5, rely = 0.2, anchor = "center")
        self.label.place(relwidth = 1.0, relheight = 0.4, relx = 0.5, rely = 0.5, anchor = "center")
        self.startButton.place(relwidth = 0.8, relheight = 0.4, relx = 0.5, rely = 0.8, anchor = "center")

#練習しているウィンドウズ
class PracticePage(tk.Frame, App):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg="white")

        self.controller = controller
        self.logo_image = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo_small.png")
        self.logo = tk.Label(self, image = self.logo_image, bg ="white", borderwidth = 0)
        self.timeLeft_label =  tk.Label(self, text= "残り時間", font ="遊ゴジックLight 30", bg ="white")
        self.timeLeft = tk.Label(self, text= "", font ="遊ゴジックLight 45", bg ="white")
        self.comment = tk.Label(self, text= "", font ="遊ゴジックLight 20 ", bg ="white")
        self.warning_label = tk.Label(self, text= "", font ="遊ゴジックLight 25 ", bg ="white")
        self.backButton = tk.Button(self, text="やり直す", borderwidth=0,   font ="遊ゴジックLight 30", bg ="light blue", command = lambda: controller.create_windows(StartPage))
        self.homeButton = tk.Button(self, text="サインアウト", borderwidth=0, font ="遊ゴジックLight 30", bg ="powder blue", command = lambda: controller.create_windows(SignInPage))
        
        self.logo.place(relx = 0.5, rely = 0.2, anchor = "center")
        self.timeLeft.place(relwidth = 1.0, relheight = 0.1, relx = 0.5, rely = 0.45, anchor = "center")
        self.timeLeft_label.place(relwidth = 1.0, relheight = 0.1, relx = 0.5, rely = 0.35, anchor = "center")
        self.comment.place(relwidth = 1.0, relheight = 0.1, relx = 0.5, rely = 0.55, anchor = "center")
        self.warning_label.place(relwidth = 1.0, relheight = 0.1, relx = 0.5, rely = 0.70, anchor = "center")
        self.backButton.place(relwidth = 0.6, relheight = 0.09, relx = 0.5, rely = 0.80, anchor = "center")
        self.homeButton.place(relwidth = 0.6, relheight = 0.09, relx = 0.5, rely = 0.90, anchor = "center")
        
        #発表の残り時間
        self.remaining = 0
        
        #カウントダウンと録音の同時実行
        self.thread1 = threading.Thread(target = stream_infinite.run)
        self.thread2 = threading.Thread(target = self.countdown,args=[PRACTICETIME])
        self.thread3 = threading.Thread(target = fundamental_freq.main)
            
        #ウィンドウズを閉じたらスレッドも止まるようにする
        self.thread1.setDaemon(True)
        self.thread2.setDaemon(True)
        self.thread3.setDaemon(True)
        
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()

    #残り時間を表示する
    def countdown(self, remaining = None): 
            if remaining is not None:
                self.remaining = remaining

            if self.remaining <= 0:
                transcribe_streaming_mic.close = True
                fundamental_freq.close = True
                self.timeLeft.configure(text="お疲れ様です！")
                self.after(2000, self.show_result) 

            else: 
                mins, secs = divmod(self.remaining,60)
                mins = round(mins)
                secs = round(secs)
                self.timeLeft.configure(text=str(mins) +"分"+ str(secs) +"秒")
                if transcribe_streaming_mic.warn:
                    self.set_warning()
                if self.remaining == 120:
                    first_min_rate = transcribe_streaming_mic.num_chars_printed
                    self.set_comment(first_min_rate)

                elif self.remaining == 60:
                    second_min_rate = transcribe_streaming_mic.num_chars_printed
                    self.set_comment(second_min_rate)
                self.remaining = self.remaining - 1
                self.after(1000, self.countdown)   

    #有声休止を言ったときに警告を表示する
    def set_warning(self):
        self.warning_label.configure(text="\"えっと\"を言わないで！")
        playsound("blip01.mp3")
        self.after(1000,self.erase_warning)

    #有声休止に対する警告を消す
    def erase_warning(self):
        self.warning_label.configure(text="")
        transcribe_streaming_mic.set_warn()
        
    #一分ごとに話速度についてのコメントを表示
    def set_comment(self, rate):
        playsound("coin02.mp3")
        self.comment.configure(text=scoring.speechRateComment(rate)[0])
        self.after(2000, self.erase_comment)    #2秒後に自動的に消える

    #話速度についてのコメントを消す
    def erase_comment(self):  
        self.comment.configure(text="")
        
    #プレゼン全体に点数を付けるための処理をして、クラスResultPageに移す
    def show_result(self):
        self.controller.create_windows(ResultPage)  #採点結果ウインドウズResultPageを表示
        
#点数などの結果を表示するウインドウズ
class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg="white")

        #話速度、ピッチ、それらに対するコメントと全体の点数を取ってくる
        self.speechrate = transcribe_streaming_mic.num_chars_printed/3 #[字/分]
        self.pitch_data = fundamental_freq.sound_data #[Hz]のリスト
        self.pitch = float(fundamental_freq.hensa) #ピッチの標準偏差(単位なし) 
        self.speechrate_comment, self.which_rate = scoring.speechRateComment(self.speechrate) #話速度に対するコメント
        self.pitch_comment = scoring.pitchComment(self.pitch, self.which_rate) #ピッチに対するコメント
        self.comment = self.speechrate_comment + self.pitch_comment #上の二つのコメントを結合
        self.score = float(scoring.cos_sim(self.speechrate, self.pitch)) #全体の点数

        self.logo_image = PhotoImage(file="C:/Users/Programming exp/Desktop/Presys_logo_small.png")
        self.logo = tk.Label(self, image = self.logo_image, borderwidth = 0)
        self.title_label = tk.Label(self,text= "採点結果", font = "遊ゴジックLight 30", bg ="white")

        self.logo.place(relx = 0.5, rely = 0.1, anchor = "center")
        self.title_label.place(relx = 0.5, rely = 0.18, anchor = "center")
        
        #点数
        self.mark_frame = tk.Frame(self, bg="light cyan")
        self.mark_frame.grid_rowconfigure(0, weight=1)     
        self.mark_frame.grid_columnconfigure(0, weight=2)  
        self.mark_frame.grid_rowconfigure(1, weight=1)     
        self.mark_frame.grid_columnconfigure(1, weight=2)   
        self.mark_label = tk.Label(self.mark_frame, text= "あなたの点数", font = "遊ゴジックLight 30", bg ="light blue") #PaleTurquoise1
        self.mark = tk.Label(self.mark_frame,text= str(round(self.score)), font = "遊ゴジックLight 90", justify = "center", bg ="light cyan")
        self.point = tk.Label(self.mark_frame,text= "点", font = "遊ゴジックLight 50", bg ="light cyan")
        
        self.mark_frame.place(relx = 0.25, rely = 0.37, relwidth = 0.45, relheight = 0.3, anchor = "center")
        self.mark_label.place(relx = 0, rely = 0, relwidth = 1.0, relheight = 0.3)#grid(row = 0, columnspan = 2, sticky = "nsew")
        self.mark.grid(row = 1, columnspan = 2, sticky = "nsew")
        self.point.grid(row = 2, columnspan = 2, sticky = "se")

        #コメント
        self.comment_frame = tk.Frame(self,  bg="light cyan")
        self.comment_frame.grid_rowconfigure(0, weight=1)     
        self.comment_frame.grid_columnconfigure(0, weight=2)  
        self.comment_frame.grid_rowconfigure(1, weight=2)     
        self.comment_frame.grid_columnconfigure(1, weight=2)   
        self.comment_label = tk.Label(self.comment_frame,text= "コメント", font = "遊ゴジックLight 30", bg ="light blue")
        self.comment = tk.Label(self.comment_frame,text= self.comment, font = "遊ゴジックLight 20", wraplength=280, bg ="light cyan")
        
        self.comment_frame.place(relx = 0.75, rely = 0.37, relwidth = 0.45, relheight = 0.3, anchor = "center")
        self.comment_label.place(relx = 0, rely = 0, relwidth = 1.0, relheight = 0.24)#, anchor = "center")#grid(rowspan = 1, columnspan = 2, sticky = "nsew")
        self.comment.grid(row = 1, columnspan = 2, sticky = "nsew")

        #話速度
        self.speechrate_frame = tk.Frame(self, width = 40, bg="light cyan")
        self.speechrate_frame.grid_rowconfigure(0, weight=2)     
        self.speechrate_frame.grid_columnconfigure(0, weight=2)  
        self.speechrate_frame.grid_rowconfigure(1, weight=2)     
        self.speechrate_frame.grid_columnconfigure(1, weight=2)  
        self.speechrate_label = tk.Label(self.speechrate_frame,text= "話速度", font = "遊ゴジックLight 25", bg ="light blue")
        self.speechrate = tk.Label(self.speechrate_frame,text= str(round(self.speechrate, 1))+"字/分", font = "遊ゴジックLight 23", bg ="light cyan")
        
        self.speechrate_frame.place(relx = 0.25, rely = 0.58, relwidth = 0.45, relheight = 0.08, anchor = "center")
        self.speechrate_label.grid(row = 0, columnspan = 2, sticky ="nsew")
        self.speechrate.grid(row = 1, columnspan = 2, sticky ="nsew")

        #pitch
        self.pitch_frame = tk.Frame(self, bg="light blue")
        self.pitch_frame.grid_rowconfigure(0, weight=2)     
        self.pitch_frame.grid_columnconfigure(0, weight=2)  
        self.pitch_frame.grid_rowconfigure(1, weight=2)     
        self.pitch_frame.grid_columnconfigure(1, weight=2)  
        self.pitch_label = tk.Label(self.pitch_frame,text= "声の高さの標準偏差", font = "遊ゴジックLight 25", bg ="light blue")
        self.pitch = tk.Label(self.pitch_frame,text= str(round(self.pitch, 1)), font = "遊ゴジックLight 23", bg ="light cyan")
        
        self.pitch_frame.place(relx = 0.75, rely = 0.58, relwidth = 0.45, relheight = 0.08, anchor = "center")
        self.pitch_label.grid(row = 0, columnspan = 2, sticky ="nsew")
        self.pitch.grid(row = 1, columnspan = 2, sticky ="nsew")

        #ピッチのグラフ
        self.f = Figure(figsize = (5, 5), dpi = 100)
        self.a = self.f.add_subplot(111)
        self.a.plot(self.pitch_data)
        self.a.axes.set_xlim([0,180])
        self.a.set_xlabel("時間[s]", fontsize = 18)
        self.a.set_ylabel("声の高さ[Hz]", fontsize = 18)
        self.a.xaxis.label.set_color('blue')
        self.a.yaxis.label.set_color('blue')
        
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx = 0.5, rely = 0.8, relwidth = 1, relheight = 0.35, anchor = "center")

#フールスクリーンモードを終了する関数
def end_fullscreen(event=None):
    apps.attributes("-fullscreen", False)

#ウインドウズ閉じる関数
def quit(event=None):
    apps.destroy()

apps = App()
apps.configure(bg="white")
apps.attributes("-fullscreen", True) #フールスクリーンモード
apps.bind("<Escape>", quit)     #escキーを押すとウインドウズ閉じる
apps.bind("<Tab>", end_fullscreen)  #tabキーを押すとフールスクリーンモードを終了
apps.mainloop()