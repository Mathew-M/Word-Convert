import gensim
import smart_open

print(__file__)

model = gensim.models.KeyedVectors.load_word2vec_format("./model.bin", binary=True)

# positive wordsを選択
posi_list = [
    "良い", "すばらしい", "幸せ", "健康", "最高", "大好き", "素敵", "心地よい", "麗しい", "美しい", "神", "かわいい", "かっこいい", "きれい", "おいしい", "うまい",
    "強い", "才能", "圧倒的", "優良", "最善", "効率的", "正しい", "勝つ", "傑作", "一番", "卓越", "超絶", "高級", "優しい", "望ましい", "純粋"
]

# negative wordsを選択
nega_list = [
    "悪い", "殺人", "憎悪", "不幸", "悪質", "嫌悪", "侮蔑", "よこしま", "あくどい", "ひどい", "最低", "まずい", "冷酷", "腹黒", "凶悪", "残酷", "無残", "邪悪",
    "まずい", "気持ち悪い", "最悪", "ブス", "難しい", "毒", "死亡", "疲労", "卑劣", "嫌い", "暴れる", "狂う", "悪魔", "不正"
]


# positive/negative wordsとの類似度を利用した単語の意味のネガポジ分析
def posi_nega_score(x):
    posi = []
    for i in posi_list:
        try:
            n = model.similarity(i, x) # posi wordsとの類似度を判定
            posi.append(n)
        except:
            continue
    try:
        posi_mean = sum(posi) / len(posi)
    except:
        posi_mean = 0

    nega = []
    for i in nega_list:
        try:
            n = model.similarity(i, x) # nega wordsとの類似度を判定
            nega.append(n)
        except:
            continue
    try:
        nega_mean = sum(nega) / len(nega)
    except:
        nega_mean = 0
    return x, posi_mean, -nega_mean, (posi_mean - nega_mean)*100


    return 0


print(posi_nega_score('日本'))
print(posi_nega_score('国宝'))
print(posi_nega_score('音楽'))

'''def makedic(y):

    posi_nega_score()


import pandas as pd
ddf = pd.read_csv('newnew.csv')

ddf['スコア'] = ddf['単語'].apply(lambda x: posi_nega_score(x))

import numpy as np

score = np.array(ddf['スコア'])
score_std = (score - score.min())/(score.max() - score.min())
score_scaled = score_std * (1 - (-1)) + (-1)
ddf['スコア'] = score_scaled'''

# dic化した方が計算早そう
