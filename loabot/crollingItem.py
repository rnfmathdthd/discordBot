import discord, asyncio, os
import re
from discord.ext import commands
from bs4 import BeautifulSoup
import pandas as pd
import requests
import traceback
import pymysql

def getProducts(string):

    result = []

    #캐릭터 정보 리스트 출력
    bsObj = BeautifulSoup(string, "html.parser")
    divs = bsObj.findAll("span", {"class": "text-theme-0 tfs14"})  # 아이템 리스트부분 추출

    for i in range(len(divs)):
        span = divs[i].getText()
        span = span.strip()
        if (i == 2):
            chara_class = span
            result.append(chara_class)
            print(span)
        if (i == 3):
            chara_award = span
            result.append(chara_award)
            print(span)
        if (i == 4):
            chara_fight = span
            result.append(chara_fight)
            print(span)
        if (i == 5):
            chara_item_lv = span
            chara_item_lv = chara_item_lv.replace(",", "")
            result.append(chara_item_lv)
            print(span)
    
    #아이템 리스트 출력
    bsObj = BeautifulSoup(string, "html.parser")
    divs = bsObj.findAll("div", {"class":"media pt-0 pb-0 mp"})  #아이템 리스트부분 추출

    for i in range(12): # 머리부터 팔찌까지 출력
        item = divs[i].getText()
        item = item.strip()
        item = item[4:]
        item = item.strip()
        if(item == ""): item = "없음"
        result.append(item)
        print(item)

    # 기습의 대가 , 절실한 구원 등 특성 2개
    bsObj = BeautifulSoup(string, "html.parser")
    divs = bsObj.findAll("div", {"class":"media p-0 m-0"})  #아이템 리스트부분 추출

    for i in range(2): #특성 2개만 출력
        special = divs[i].getText()
        special = special.strip()
        special = special.replace("  ", " ")
        result.append(special)
        print(special)

    return result
