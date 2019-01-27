import requests
from bs4 import BeautifulSoup
import time
import os

###はてなぶろぐエントリー一覧
print("start!")
list = []
root = ""  #


def main(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')  ##lxmlを指定するほうがよい

    alink = soup.select('a')
    newLinkCheck = False;

    for i in range(len(alink)):
        if alink[i].get("class") != None:
            if 'entry-title-link' in alink[i].get('class'):
                if alink[i].get("href") not in list:
                    print('【プログラミング素人のはてなブログ】' + alink[i].getText() + ' ' + alink[i].get('href'))
                    get_contents(alink[i].get('href'))  # コンテンツ取得
                    newLinkCheck = True;
                    time.sleep(0.3)
                    list.append(alink[i].get("href"))

    return newLinkCheck


def get_contents(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')  ##lxmlを指定するほうがよい
    contents_div = soup.select('div')
    for i in range(len(contents_div)):
        if contents_div[i].get("class") != None:
            if 'entry-content' in contents_div[i].get('class'):
                page = contents_div[i]  # Full HTML
                folderName = url.replace("https://s51517765.hatenadiary.jp/entry/", "")
                folderName = folderName.replace("/", "")  # 日付でフォルダ名にする
                os.chdir(root)  # ルートディレクトリに移動
                if not os.path.exists(folderName):
                    os.mkdir(folderName)  # フォルダーを作る
                os.chdir(folderName)  # 存在しないフォルダに移動しようとするとErrorになる
                file = open(folderName + '.html', 'w', encoding='utf')  # 書き込みモードでオープンs
                file.write(str(page))
                file.close()
                try:
                    imgs = soup.find_all("img")
                    i = 0
                    for img in imgs:
                        if 'fotolife' in img['src']:
                            r = requests.get(img['src'])
                            with open(str(i) + '.jpeg', 'wb') as file:
                                file.write(r.content)
                            i += 1  # 画像に連番をつける
                except:
                    pass


if __name__ == '__main__':
    savedir = "blogSave"
    if not os.path.exists(savedir):
        os.mkdir(savedir)  # フォルダーを作る
    os.chdir(savedir)
    root = os.getcwd()  # カレントフォルダ取得
    rootUrl = 'http://s51517765.hatenadiary.jp/archive?page='
    n = 1

    cont = True
    while (cont == True):
        url = rootUrl + str(n)
        if main(url) == False:
            cont = False
            break
        n += 1
