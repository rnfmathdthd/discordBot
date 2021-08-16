from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql

# 쿠팡 api
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def getPageListString(url):
    data = requests.get(url, headers = headers)
    return data.content

def getProductsSumnail(string):

    bsObj = BeautifulSoup(string, "html.parser")
    div = bsObj.find("div", {"class":"prdImg"})
    img = div.find("img").get("src")
    print(img)
    return img