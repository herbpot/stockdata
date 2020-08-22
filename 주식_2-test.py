import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

time_now = time.localtime(time.time())
H = int(time_now.tm_hour)
url_code = input()

while True :
    if(H == 16):
        url = "https://finance.naver.com/item/main.nhn?code=" + url_code
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        no_today = bs_obj.find("p", {"class": "no_today"}) # 태그 p, 속성값 no_today 찾기
        0
        now_price = no_today.text
        
        print(now_price)
        print(today_)
        f = open("주식가격.txt","w+")
        f.write("\n")
        f.write(today_)
        f.write("\n")
        f.write(now_price)
        f.close()
        
    

