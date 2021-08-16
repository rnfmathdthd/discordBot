from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymysql
import getCategory as cate
import getSumnail as imge
import getInfo as inf

# 쿠팡 api
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
coupangURL = "https://www.coupang.com/"

#mysql 연결
conn = pymysql.connect(
    user="test"
    , passwd="oracle!"
    , host="localhost"
    , db="productlistdb"
)

# 테이블 생성 존재할 경우 지우고 다시생성
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS getProduct")
cursor.execute("CREATE TABLE getProduct ("
               "prod_brand varchar(100)"
               ", prod_name varchar(250)"
               ", prod_price varchar(30)"
               ", prod_sale varchar(100)"
               ", prod_score float"
               ", prod_reviews int"
               ", prod_category1 varchar(30)"
               ", prod_category2 varchar(30)"
               ", prod_sumnail varchar(250)"
               ")"
               )
page_num = 2
page_count = "#pageCount="
url = "http://www.e-himart.co.kr/app/display/showDisplayCategory?dispNo=1011010000"

def getPageListString(url):
    data = requests.get(url, headers = headers)
    return data.content

def getPageString(url):
    data = requests.get(url, headers = headers)
    return data.content

def getProducts(string):

    bsObj = BeautifulSoup(string, "html.parser")
    ul = bsObj.find("ul", {"class":"thumnailType thumnailS"})  #아이템 리스트부분 추출
    lis = ul.findAll("li") #각 아이템 추출

    for item in lis:

        # url
        a = item.find("a", {"class": "prdLink"})
        url = a.get('href')
        print("\nurl:", url)

        prodUrl = "https://www.e-himart.co.kr/" + url
        getProductPage = getPageString(prodUrl)

        category = cate.getProductsCategory(getProductPage)
        sumnail = imge.getProductsSumnail(getProductPage)
        info = inf.getProductsInfo(getProductPage)
        #getDescription = des.getProductsDescription(getProductPage)

        # 리뷰수
        try:
            review = item.find('span', {"class" : "ratingTotal"}).find('em').getText()
            print("리뷰 수 : ", review)
        except Exception:
            review = 0
            print("리뷰 수 : ", review)

        # info[0] : 브랜드 이름
        # info[1] : 상품 이름
        # info[2] : 상품 가격
        # info[3] : 할인 상품 가격
        # info[4] : 상품 평점

        # category[0] : 카테고리 1
        # category[1] : 카테고리 2

        # insert 문때 담을 변수들을 담는 리스트 생성
        tempList = [(info[0], info[1], info[2], info[3], info[4]
            , review
            , category[0], category[1]
            , sumnail)]
        # results.extend(tempList)

        sql = "INSERT INTO getProduct(" \
              "prod_brand, prod_name, prod_price, prod_sale," \
              "prod_score, prod_reviews, prod_category1, prod_category2, prod_sumnail" \
              ") VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.executemany(sql, tempList)
        except Exception:
            continue
        #INSERT INTO customers(name, address) VALUES( % s, % s)" 참고

    print(len(lis))
    return []

results = []

for i in range(3):
    print(url)
    if i == 0:
        pageString = getPageListString(url)
        productList = getProducts(pageString)
        url += page_count
        url += str(page_num)
    else:
        page_num += 1
        url = url.replace(url[-1], str(page_num))
        pageString = getPageListString(url)
        productList = getProducts(pageString)

# data = pd.DataFrame(results)
# data.columns = ['product_url', 'product_name', 'product_img', 'product_price']
# data.to_csv('상품리스트.csv', encoding='utf-8')
#print(productList)///////////////

conn.commit()
conn.close()