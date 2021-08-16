import time

import discord, asyncio, os
from discord.ext import commands
from bs4 import BeautifulSoup
import pandas as pd
import requests
import traceback
import pymysql
import crollingItem as addChara
from datetime import datetime

client = discord.Client()

client = commands.Bot(command_prefix='!')

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
url = "https://loawa.com/char/"
itemPiece = ['클래스', '칭호', '전투레벨', '아이템레벨', '머리', '어깨', '상의', '하의', '장갑', '무기', '목걸이', '귀걸이1', '귀걸이2', '반지1', '반지2', '팔찌', '특성1', '특성2']
charaStat = ['닉네임','클래스', '칭호', '전투레벨', '아이템레벨', '머리', '어깨', '상의', '하의', '장갑', '무기', '목걸이', '귀걸이1', '귀걸이2', '반지1', '반지2', '팔찌', '특성1', '특성2','갱신일자', '계정주인']
todayResult = ['성과가 없으시네요', '오늘은 적당히 하셨네요', '정말 좃폐인 같으세요 그만좀 하면 안될까요?']
RoaList = []

#mysql 연결
conn = pymysql.connect(
    user="test"
    , passwd="oracle!"
    , host="localhost"
    , db="productlistdb"
)

def getPageString(url):
    data = requests.get(url, headers = headers)
    return data.content

# 테이블 생성 존재할 경우 지우고 다시생성
cursor = conn.cursor()

print('완료')


@client.command(name='캐릭터등록')
@commands.is_owner()
async def online(ctx):

    list = []
    embed = discord.Embed(title="등록할 캐릭터 닉네임을 입력하세요", color=0x4432a8)
    await ctx.send(embed=embed)

    try:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        # 캐릭터 닉네임 입력받기
        msg = await client.wait_for("message", check=check)
        charaName = msg.content
        charaName = charaName.strip()

        sql = "select * from lostark_chara_info where chara_name = %s"
        cursor.execute(sql, charaName)
        result = cursor.fetchall()

        if len(result) != 0:
            # 캐릭터 주인 입력받기
            embed = discord.Embed(title="이미 등록되어있는 캐릭터입니다.", color=0xFF1493)
            await ctx.send(embed=embed)
            return

        print(charaName)
        charaUrl = url + charaName
        pageString = getPageString(charaUrl)
        list = addChara.getProducts(pageString)

        print(len(list))
        print(len(itemPiece))

        # 캐릭터 정보 출력
        embed = discord.Embed(title=str(charaName) + "의 정보", color=0x4432a8)
        for i in range(len(list)):
            embed.add_field(name=str(itemPiece[i]) + "  ", value=str(list[i]) + "\n")
        # embed.add_field(name="출처 : 로아와", value="\n")
        await ctx.send(embed=embed)

        # 캐릭터 주인 입력받기
        embed = discord.Embed(title="해당 캐릭터의 주인은 누구입니까?", color=0x4432a8)
        await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await client.wait_for("message", check=check)
        charaOwner = msg.content

        embed = discord.Embed(title=charaOwner + "의 " + charaName, color=0xFF1493)
        await ctx.send(embed=embed)
        list.append(charaName)
        list.append(charaOwner)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 년월일시분초
        list.append(now)

        tempListInsert = [(
            list[0], list[1], list[2], list[3], list[4]
            , list[5], list[6], list[7], list[8], list[9]
            , list[10], list[11], list[12], list[13], list[14]
            , list[15], list[16], list[17], list[18], list[19], list[20] )]

        sql = "INSERT INTO lostark_chara_info (" \
              "chara_class, chara_award, chara_fight, chara_item_lv, chara_head, chara_shoulder, chara_top, chara_bottom" \
              ", chara_glove, chara_weapon, chara_neck, chara_earing_one, chara_earing_two, chara_ring_one, chara_ring_two" \
              ", chara_arm, chara_special_one, chara_special_two, chara_name, chara_owner, chara_mod_date) " \
              "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"

        cursor.executemany(sql, tempListInsert)

    except:
        embed = discord.Embed(title="해당 캐릭터가 존재하지 않습니다!!", color=0xFF1493)
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title=charaOwner + "의 캐릭터 " + charaName + "이(가) 정상적으로 등록 되었습니다.", color=0x4432a8)
    await ctx.send(embed=embed)
    conn.commit()

@client.command(name='캐릭터목록')
@commands.is_owner()
async def online(ctx):

    embed = discord.Embed(title="누구?", color=0x4432a8)
    await ctx.send(embed=embed)

    try:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        # 캐릭터 닉네임 입력받기
        msg = await client.wait_for("message", check=check)
        charaOwner = msg.content
        charaOwner = charaOwner.strip()

        sql = "select * from lostark_chara_info where chara_owner = %s";
        cursor.execute(sql, charaOwner)
        result = cursor.fetchall()
        print(result)

        if len(result) == 0:
            # 캐릭터 주인 입력받기
            embed = discord.Embed(title="아무것도 없습니다.", color=0xFF1493)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title=charaOwner + "의 캐릭터 목록", color=0xFF1493)
        for ddd in result:
            embed.add_field(name=str(ddd[0]) + "  ", value="직업 : " + str(ddd[1]) + "\n칭호 : " + str(ddd[2]) + "\n전투레벨 : " + str(ddd[3]) + "\n아이템레벨 : " + str(ddd[4]) + "\t\n")
        await ctx.send(embed=embed)

    except:
        embed = discord.Embed(title="오류발생", color=0xFF1493)
        await ctx.send(embed=embed)

@client.command(name='캐릭터삭제')
@commands.is_owner()
async def online(ctx):

    embed = discord.Embed(title="누구?", color=0x4432a8)
    await ctx.send(embed=embed)

    try:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        # 캐릭터 닉네임 입력받기
        msg = await client.wait_for("message", check=check)
        charaOwner = msg.content
        charaOwner = charaOwner.strip()

        sql = "select * from lostark_chara_info where chara_owner = %s";
        cursor.execute(sql, charaOwner)
        result = cursor.fetchall()
        print(result)

        if len(result) == 0:
            # 캐릭터 주인 입력받기
            embed = discord.Embed(title="아무것도 없습니다.", color=0xFF1493)
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title=charaOwner + "의 캐릭터 목록", color=0xFF1493)
        for ddd in result:
            embed.add_field(name=str(ddd[0]) + "  ", value="-----", inline=False)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="무엇을 삭제할토끼?", color=0xFF1493)
        await ctx.send(embed=embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        # 캐릭터 닉네임 입력받기
        msg = await client.wait_for("message", check=check)
        charaName = msg.content
        charaName = charaName.strip()

        sql = "select * from lostark_chara_info where chara_owner = %s";
        cursor.execute(sql, charaName)

        if len(result) == 0:
            embed = discord.Embed(title="없는걸 입력했거나 오타입니다.", color=0xFF1493)
            await ctx.send(embed=embed)
            return

        sql = "delete from lostark_chara_info where chara_name = %s"
        cursor.execute(sql, charaName)

    except:
        embed = discord.Embed(title="오류발생", color=0xFF1493)
        await ctx.send(embed=embed)

    conn.commit()

@client.command(name='성과')
@commands.is_owner()
async def online(ctx):

    modifiedList = []
    currentList = []

    embed = discord.Embed(title="누구?", color=0x4432a8)
    await ctx.send(embed=embed)

    try:
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
            # 캐릭터 닉네임 입력받기

        msg = await client.wait_for("message", check=check)
        charaOwner = msg.content
        charaOwner = charaOwner.strip()

        embed = discord.Embed(title="잠시만 기다려 주십시오...", color=0x4432a8)
        await ctx.send(embed=embed)

        sql = "select * from lostark_chara_info where chara_owner = %s";
        cursor.execute(sql, charaOwner)
        result = cursor.fetchall()
        print(result)
        print(len(result))

        getColumnCount = "SELECT COUNT(*) FROM information_schema.columns WHERE table_name='lostark_chara_info'"
        cursor.execute(getColumnCount)
        col = cursor.fetchone()
        col = col[0]

        if len(result) == 0:
            embed = discord.Embed(title=charaOwner + "의 캐릭터가 없습니다.", color=0xFF1493)
            await ctx.send(embed=embed)
            return

        # 기존 캐릭터 정보
        for item in result:
            modifiedcol = []
            for i in range(col):
                modifiedcol.append(item[i])
            modifiedList.append(modifiedcol)
        print(modifiedList)

        # 현재 캐릭터 정보
        for item in result:
            charaName = item[0]
            charaUrl = url + charaName
            pageString = getPageString(charaUrl)
            list = []
            list.append(charaName)
            list.extend(addChara.getProducts(pageString))
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 년월일시분초
            list.append(now)
            list.append(charaOwner)
            currentList.append(list)

        print(currentList[1][4])

        updateGap = str(datetime.strptime(currentList[0][19], '%Y-%m-%d %H:%M:%S') - modifiedList[0][19])
        updateGap = updateGap.replace("days" , "일")
        updateGap = updateGap[:-3]
        updateGap = updateGap.replace(":", " 시간  ")
        updateGap = updateGap + "  분"

        embed = discord.Embed(title=charaOwner + " 의  " +
                                    updateGap
                                    + "  만의 성과", color=0xFF1493)
        for i in range(len(modifiedList)):
            embed.add_field(name="------------------------------------------------------------------", value="-", inline=False)
            embed.add_field(name=str(modifiedList[i][0]) + "  ", value=str(modifiedList[i][1]), inline=False)
            for j in range(col):
                if modifiedList[i][j] != currentList[i][j]:
                    if int(modifiedList[i][3]) == int(currentList[i][3]) and j == 3:
                        continue
                    if round(float(modifiedList[i][4]), 1) == round(float(currentList[i][4]), 1) and j == 4:
                        continue
                    if j == 19: continue
                    print(modifiedList[i][j])
                    embed.add_field(name=str(charaStat[j]) + "  ", value=str(modifiedList[i][j]) + " ==> " + str(currentList[i][j]), inline=False)
        await ctx.send(embed=embed)

        print(currentList)

        for i in range(len(modifiedList)):
            tempListUpdate = [(
                currentList[i][2], currentList[i][3], currentList[i][4], currentList[i][5], currentList[i][6]
                , currentList[i][7], currentList[i][8], currentList[i][9], currentList[i][10], currentList[i][11]
                , currentList[i][12], currentList[i][13], currentList[i][14], currentList[i][15], currentList[i][16]
                , currentList[i][17], currentList[i][18], currentList[i][19], currentList[i][0])]

            sql = "UPDATE lostark_chara_info SET " \
                  "chara_award=%s, " \
                  "chara_fight=%s, " \
                  "chara_item_lv=%s, " \
                  "chara_head=%s, " \
                  "chara_shoulder=%s, " \
                  "chara_top=%s, " \
                  "chara_bottom=%s, " \
                  "chara_glove=%s, " \
                  "chara_weapon=%s, " \
                  "chara_neck=%s, " \
                  "chara_earing_one=%s, " \
                  "chara_earing_two=%s, " \
                  "chara_ring_one=%s, " \
                  "chara_ring_two=%s,  " \
                  "chara_arm=%s,  " \
                  "chara_special_one=%s,  " \
                  "chara_special_two=%s,  " \
                  "chara_mod_date=%s  " \
                  "WHERE chara_name = %s"

            cursor.executemany(sql, tempListUpdate)

    except:
        embed = discord.Embed(title="오류발생", color=0xFF1493)
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(title=charaOwner + "의 캐릭터리스트 갱신 완료", color=0xFF1493)
    await ctx.send(embed=embed)
    conn.commit()


@client.event
async def on_command_error(ctx, error):
    tb = traceback.format_exception(type(error), error, error.__traceback__)
    err = [line.rstrip() for line in tb]
    errstr = '\n'.join(err)
    if isinstance(error, commands.NotOwner):
        await ctx.send('봇 주인만 사용 가능한 명령어입니다')
    else:
        print(errstr)

client.run('토큰번호') #토큰

conn.commit()
conn.close()
