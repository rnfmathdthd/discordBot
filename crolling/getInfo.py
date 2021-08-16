from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql

# 쿠팡 api
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

def getPageListString(url):
    data = requests.get(url, headers = headers)
    return data.content

def getProductsInfo(string):

    info = []

    # 브랜드 이름
    bsObj = BeautifulSoup(string, "html.parser")
    div = bsObj.find("div", {"class":"prdFlag"})
    ptag = div.find("p", {"class":"brandName"})
    brand = ptag.find('a').getText()
    print("brand :", brand)
    info.append(brand)

    # 상품 이름
    div = bsObj.find("div", {"class": "prdName"})
    name = div.find('h2').getText()
    name = name.strip()
    print("name :", name)
    info.append(name)
    
    # 상품 가격
    li = bsObj.find("li", {"class": "priceArea"})
    cur_price = li.find('span').getText()
    cur_price = cur_price.strip()
    cur_price = int(cur_price)
    print("cur_price :", cur_price)
    info.append(cur_price)

    # 할인 상품 가격
    dl = bsObj.find("dl", {"class": "Price"})
    sale_price = dl.find('span').getText()
    sale_price = sale_price.strip()
    sale_price = int(sale_price)
    print("sale_price :", sale_price)
    info.append(sale_price)

    # 상품 평점
    try:
        div = bsObj.find("div", {"class": "gradeMark"})
        # 형변환 필요
        jumsu = div.find("div", {"class": "gmL"}).getText()
        jumsu = float(jumsu)
        info.append(jumsu)
        print("jumsu :", jumsu)
        print(info)
        return info
    except Exception:
        print("null 포인트")
        info.append(0)
        return info


