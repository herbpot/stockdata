import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time

today = datetime.datetime.today()
today_ = str(today)
url_code = input()
url = "https://finance.naver.com/item/main.nhn?code=" + url_code

while True :
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    no_today = bs_obj.find("p", {"class": "no_today"}) # 태그 p, 속성값 no_today 찾기
    
    now_price = no_today.text
    
    print(now_price)
    print(today_)
    f = open("주식가격.txt","a")
    f.write("\n")
    f.write(today_)
    f.write("\n")
    f.write(now_price)
    

f.close()