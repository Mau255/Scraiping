# -*- coding: utf-8 -*-
"""11 Scraiping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EPMtGICBRaA5UvaweIgR_laabWb78g04
"""

# モジュールのインポート
!apt-get update
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
!pip install selenium

#webdriver, optionsのインポート
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
# GUIを持たない Headless モードに設定。新しいブラウザを別途使わないようにする。
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('chromedriver',options=options)

# Webサイトにアクセス
url = 'http://4travel.jp/domestic/area/kinki/kyoto/kankospot'
browser.get(url)

browser.quit()

"""###観光地名を1件取得"""

title_elem = browser.find_element_by_class_name('u_title')
title_elem.text

elem = title_elem.find_element_by_tag_name('h2')
elem.text

elem.find_element_by_tag_name('a').text

url = elem.find_element_by_tag_name('a').get_attribute('href')
url

"""###観光地名を複数取得"""

title_elems = browser.find_elements_by_class_name('u_title')
len(title_elems)

title_elems[0].text

#観光地名だけを取得
title_elem = title_elems[0]
elem = title_elem.find_element_by_tag_name('h2')
elem.text

"""###演習問題１
20個の観光地名をplaces[]というリストに格納
"""

title_elems = browser.find_elements_by_class_name('u_title')

places = []
for title_elem in title_elems:
  elem = title_elem.find_element_by_tag_name('h2')
  places.append(elem.text)

places

"""###総合評価(点数)でも同じことをやってみよう。"""

#総合評価の取得。まずは1件のみ。
evaluate_elem = browser.find_element_by_class_name('ranking_evaluateWrapper')
evaluate_elem.text

#点数のみを取得
evaluate = evaluate_elem.find_element_by_tag_name('span')
evaluate.text

#複数取得
evaluate_elems = browser.find_elements_by_class_name('ranking_evaluateWrapper')
len(evaluate_elems)

evaluate_elems[0].text

#0番目の点数だけを取得
evaluate_elem = evaluate_elems[0]
elem = evaluate_elem.find_element_by_tag_name('span')
elem.text

evaluate_elems = browser.find_elements_by_class_name('ranking_evaluateWrapper')

evaluates = []
for evaluate_elem in evaluate_elems:
  elem = evaluate_elem.find_element_by_tag_name('span')
  evaluates.append(elem.text)

evaluates

"""ちなみに、いきなり「evaluateNumber」のclass指定をしてしまうとうまく行かない。  
これは、そのclassで指定されているものが他にもあるから。  
特定の情報を取得したい場合は、その情報が所属するdivをまずは指定して、そのdivの中で、その情報をさらに指定するような形が望ましい。  
つまり、先ほどの観光地名でやった流れに沿ってやるのが良い。  
- 自分がやったのを後で修正しよう。spanで取得するのは気持ち悪い。
"""

# アクセスのタイミングを開ける
from time import sleep

# 複数個に適用
block_elems = browser.find_elements_by_class_name('u_areaListRankingBox')
# block_elem = block_elems[0]  # <- point(for文に置き換える前のポイント)

access_ranks = []
for block_elem in block_elems:
    elems = block_elem.find_element_by_class_name('evaluateNumber')
    # print(elem.text) # 確認用
    access_ranks.append(elems.text)
    print('処理中')
    # アクセスの間隔を５秒開ける
    sleep(5)

access_ranks[0], type(access_ranks[0])

# 選択肢1
com_ranks = []
for rank in access_ranks:
    com_ranks.append( float(rank) )

com_ranks, type(com_ranks[0])

"""###データの整形"""

import pandas as pd
df = pd.DataFrame()

df['観光地'] = places

df['総合評価'] = com_ranks

df

"""###条件抽出"""

df[df['総合評価'] > 4.30]

df[ (df['総合評価'] >= 4.30) & (df['総合評価'] <4.50)]

"""###CSVファイルへの出力"""

df_csv = df[ (df['総合評価'] >= 4.30) & (df['総合評価'] <4.50)]

df_csv.to_csv('celenium.csv', index=False, encoding='shift-jis')

browser.quit()

"""###BeautifulSoup4"""

!pip install beautifulsoup4

from bs4 import BeautifulSoup as bs4

import requests

url = 'https://4travel.jp/domestic/area/kinki/kyoto/kankospot'
res = requests.get(url)

soup = bs4(res.text, 'html.parser')
print(soup.prettify)

contents = soup.select('.u_title')
print(contents)

contents = soup.select('.u_title > h2 > a')
contents[0].string

"""###演習３"""

contents = soup.select('.u_title > h2 > a')

places = []
for content in contents:
  places.append(content.string)

places

"""###演習４"""

evaluates = soup.select('.is_rank > span')

com_ranks = []
for evaluate in evaluates:
  com_ranks.append(evaluate.string)

com_ranks

com_ranks[2]

import pandas as pd

df = pd.DataFrame({
    '観光地': places,
    '総合評価': com_ranks,
})

df

df.to_csv('selenium2.csv', index=False, encoding='shift-jis')

df.to_csv('selenium3.csv', index=False, encoding='Shift-JIS')

df.to_csv('selenium4.csv', index=False, encoding='UTF-8')

df.to_csv('selenium5.csv', index=False, encoding='Shift-JIS')

