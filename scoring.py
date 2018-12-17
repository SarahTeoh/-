#プレゼンテーション採点、コメントするプログラム
import numpy as np

#ベクトルのコサイン類似度を計算
def cos_sim(speechrate, pitch):
    v1 = np.array([300, 30])     #理想な値の行列[話速度(字/秒), ピッチの標準偏差(Hz)]
    v2 = np.array([speechrate, pitch])     #ユーザの話速度とピッチの行列
    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) #0から1の値
    #print("{:.1f}".format(similarity*100))
    return "{:.1f}".format(similarity*100)
    

def speechRateComment(speechrate):
    if 250 <= speechrate <= 300:
        rate_comment = "いいですね！あなたはちょうどのスピードで話しています！"
    elif 200<= speechrate < 250:
        rate_comment = "もう少し速く話しましょう!"
    else:
        rate_comment = "この話スピードだと聴衆は寝ちゃいます!"
    return rate_comment    

def speechRateFinalComment(speechrate):
    if 250 <= speechrate <= 300:
        rate_comment = "いいですね！あなたはちょうどのスピードで話しています！"
    elif 200<= speechrate < 250:
        rate_comment = "もう少し速く話しましょう!"
    else:
        rate_comment = "この話スピードだと聴衆は寝ちゃいます!"
    return rate_comment    

def pitchComment(hensa):
    if hensa < 25 :
        pitch_comment = "もっと抑揚をつけて話した方がいいです" 
    else:
        pitch_comment = "プレゼンの話し方がうまいです！"
    return pitch_comment

