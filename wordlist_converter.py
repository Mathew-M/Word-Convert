from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import time
import sqlite3


# weblioによる意味データと発音記号の取得
def online_converter(target):  # target=単語が格納されたcsvファイル
    words = pd.read_csv(target, dtype=str)
    # print(words)
    # print(words["word"])
    for n in range(len(words)):
        # print(words.at[n, 'word'])
        words.at[n, 'word'] = str(words.at[n, 'word']).split()[0]  # 簡易意味データが単語リストに付属していた場合のみ
        print(words.at[n, 'word'])
        url = 'https://ejje.weblio.jp/content/'+str(words.at[n, 'word'])
        header = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"}
        respond = requests.get(url, headers=header)
        respond.raise_for_status()
        soup = BeautifulSoup(respond.text, 'html.parser')
        words.at[n, 'mean'] = soup.find(class_='content-explanation ej').text
        words.at[n, 'pron'] = soup.find(class_='phoneticEjjeDesc').text
        sleep_time = np.random.uniform(3, 5)
        time.sleep(sleep_time)

    words.to_csv(path_or_buf='online/'+target, index=False)


# 無料辞書データベースejdict(https://github.com/kujirahand/EJDict)を用いたオフラインでの意味取得 同階層にdjdict.sqlite3が必要
def offline_converter(target):  # target=単語が格納されたcsvファイル
    def amend(del_list, subject):
        for n in range(len(del_list)):
            subject = subject.replace(del_list[n], '')
        return subject

    words = pd.read_csv('target', dtype=str)
    con = sqlite3.connect('ejdict.sqlite3')
    cur = con.cursor()

    for n in range(len(words)):
        words.at[n, 'word'] = str(words.at[n, 'word']).split()[0]
        word = str(words.at[n, 'word'])
        words.at[n, 'mean'] = amend("""`'"[]()""", str(list(cur.execute("SELECT mean FROM items WHERE word = ?", (word,)))).replace(",", "、"))
        # words.at[n, 'frequency'] = str(list(cur.execute("SELECT level FROM items WHERE word = ?", (word,))))

    con.close()
    words.to_csv(path_or_buf='offline/'+target, index=False)

# 単語の順番をランダムに変換
def random(target):  # target=単語が格納されたcsvファイル
    data = pd.read_csv('target')
    randomed = data.sample(frac=1)
    randomed.to_csv(path_or_buf='random/'+target, index=False)