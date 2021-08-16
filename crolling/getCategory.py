from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql

# 쿠팡 api
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def getPageListString(url):
    data = requests.get(url, headers = headers)
    return data.content

def getProductsCategory(string):

    bsObj = BeautifulSoup(string, "html.parser")
    div = bsObj.find("div", {"class":"locationArea"})  #아이템 리스트부분 추출
    lis = div.findAll("li", {"class":"tit"}) #각 아이템 추출
    list = []
    cnt = 0
    for item in lis[1:]:
        if cnt < 2:
            cate = item.find("a").getText()
            print("category : ", cate)
            list.append(cate)
    return list
