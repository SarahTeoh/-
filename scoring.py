#プレゼンテーション採点、コメントするプログラム
import numpy as np

#ベクトルのコサイン類似度を計算
def cos_sim(speechrate, pitch):
    v1 = np.array([300, 10])     #理想な値の行列[話速度(字/秒), ピッチの標準偏差(Hz)]
    v2 = np.array([speechrate, pitch])     #ユーザの話速度とピッチの行列
    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) #0から1の値
    print(similarity)
    print("{:.1f}".format(similarity*100))
    return "{:.1f}".format(similarity*100)
    

def speechRateComment(speechrate):
    if 250 <= speechrate <= 300:
        rate_comment = "いいね！あなたはちょうどのスピードで話しています！"
    elif 200<= speechrate < 250:
        rate_comment = "もっと速いスピードで話しましょう"
    else:
        rate_comment = "この話速度だと聴衆は寝ちゃいますよ"
    return rate_comment    


