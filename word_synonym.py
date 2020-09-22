import requests
from bs4 import BeautifulSoup
import time

header_ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"} # UserAgent書き換え指定

# Merriam Webster Dictionary による類義語の取得
def synonym(word):
    url2 = "https://www.merriam-webster.com/thesaurus/" + str(word)  # こっから類義語の取得
    res2 = requests.get(url2, headers=header_ua)
    soup2 = BeautifulSoup(res2.text, "html.parser")
    syn = soup2.select(
        "#thesaurus-entry-1 > div.vg > div > span > div > span.thes-list.syn-list > div.thes-list-content.synonyms_list > ul")
    time.sleep(3)

    try:  # 類義語の抽出
        dsyn = str(syn[0].text).split(", ")
        dsynedit = [u.replace('\n', '') for u in dsyn]
        return dsynedit

    except IndexError:
        try:  # precariousなどの例外単語の抽出
            syn = soup2.select(
                "#thesaurus-entry-1 > div.vg > div > span > div > span.thes-list.sim-list > div.thes-list-content.synonyms_list")
            dsyn = str(syn[0].text).split(", ")
            dsynedit = [u.replace('\n', '') for u in dsyn]
            return dsynedit

        except IndexError:
            return 0



if __name__ == "__main__":
    line1 = input("what word do you want to search?:")
    print("synonym:", end="")
    print(synonym(line1))
