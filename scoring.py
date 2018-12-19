#プレゼンテーション採点、コメントするプログラム
import numpy as np

#ベクトルのコサイン類似度を計算
def cos_sim(speechrate, pitch):
    v1 = np.array([300, 25])     #理想な値の行列[話速度(字/秒), ピッチの標準偏差(Hz)]
    v2 = np.array([speechrate, pitch])     #ユーザの話速度とピッチの行列
    dist = (np.linalg.norm(v1-v2)) #Euclidean distance
    score = 100-(dist*100/325) #300 + 25 =325 が二つのベクトル間の最長距離だから、325の時0点,距離が0の時100点 
    return int(round(score)) #スコアを整数にする

def speechRateComment(speechrate):
    which_rate = ""
    if speechrate > 300:
        rate_comment = "早口すぎます. もう少しゆっくりと話しましょう."
        which_rate = "a"
    elif 250 <= speechrate <= 300:
        rate_comment = "いいですね！あなたはちょうどのスピードで話しています！"
        which_rate = "b"
    elif 200<= speechrate < 250:
        rate_comment = "もう少し速く話しましょう!"
        which_rate = "c"
    else:
        rate_comment = "この話スピードだと聴衆は寝ちゃいますよ!"
        which_rate = "d"
    return rate_comment, which_rate

def pitchComment(hensa, which_rate):
    if hensa > 28:
        if which_rate == "b":
            pitch_comment = "ですが, イントネーションをつけすぎてしまいます！"
        else:
            pitch_comment = "また, イントネーションをつけすぎてしまいます！"
    elif 20 <= hensa <= 28: 
        if which_rate == "b":
            pitch_comment = "また, プレゼンのイントネーションをうまく使っています！"
        else:
            pitch_comment = "ですが, プレゼンのイントネーションをうまく使っています！"
    elif hensa < 20:
        if which_rate == "b":
            pitch_comment = "ですが, もっと抑揚をつけた方がいいです" 
        else:
            pitch_comment = "また, もっと抑揚をつけた方がいいです." 
    return pitch_comment


