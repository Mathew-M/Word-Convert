import requests
from bs4 import BeautifulSoup
import time

header_ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"} # UserAgent書き換え指定

# Oxforf Learners Dictionary による品詞、発音記号、定義の取得
def etoe (x, word):
    word_info = []
    url = "https://www.oxfordlearnersdictionaries.com/us/definition/english/" + str(word) + "_" + str(x)
    res = requests.get(url, headers=header_ua)
    soup = BeautifulSoup(res.text, "html.parser")

    hins = soup.select(".pos") #品詞を取得
    # print(hins[0].text)
    word_info.append(hins[0].text)

    pron = soup.select(".phon") #発音記号を取得
    # print(pron[1].text)
    word_info.append(pron[1].text)

    meaning = soup.select(".def") #定義を取得(品詞ごとに)
    for n in range(len(meaning)):
        # print(str(n + 1) + ": " + str(meaning[n].text))
        word_info.append(str(n+1)+". "+str(meaning[n].text))
    time.sleep(3)
    return(word_info)





def etoefin (x, y, word): #tear, second など違う語源で同じスペルの単語がある場合の例外処理
    word_info = []
    url = "https://www.oxfordlearnersdictionaries.com/us/definition/english/" + str(word) + str(x) + "_" + str(y)
    res = requests.get(url, headers=header_ua)
    soup = BeautifulSoup(res.text, "html.parser")

    hins = soup.select(".pos")
    # print(hins[0].text)
    word_info.append(hins[0].text)

    pron = soup.select(".phon")
    # print(pron[1].text)
    word_info.append(pron[1].text)

    meaning = soup.select(".def")
    for n in range(len(meaning)):
        # print(str(n + 1) + ": " + str(meaning[n].text))
        word_info.append(str(n+1)+". "+str(meaning[n].text))
    time.sleep(3)
    return(word_info)
    



def word_info(word):
    try:
        for s in range(1, 6): #通常の場合はこれだけで大丈夫 (1, 6)にしてtry-exceptで受けてるけど
            return etoe(s, word)
    except IndexError:
        try:
            for t in range(1, 5):
                for u in range(1, 6):
                    return etoefin(t, u, word)
        except IndexError:
            try:
                for t in range(2, 5):
                    for u in range(1, 6):
                        return etoefin(t, u, word)
            except IndexError:
                try:
                    for t in range(3, 5):
                        for u in range(1, 6):
                            return etoefin(t, u, word)
                except IndexError:
                    try:
                        for t in range(4, 5):
                            for u in range(1, 6):
                                return etoefin(t, u, word)
                    except IndexError:
                        return "fin"

if __name__ == "__main__":
    word = input("what word do you want to search?:")
    print(word_info(word))

"""メモ（要素の指定と削除オア置換）
import re
while soup.find(href=re.compile("https://www.oxfordlearnersdictionaries.com/us/definition/english/" + str(word))) != None:
    soup.find(href=re.compile("https://www.oxfordlearnersdictionaries.com/us/definition/english/" + str(word))).replace_with(word) or .decompose()"""


