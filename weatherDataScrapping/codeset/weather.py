#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 라이브러리 선언
import requests
import bs4
import pandas as pd
import os
from datetime import datetime as dt
from lxml import html
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote

baseUrl = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
inApiKey = "txTdKQwpVPsjw4+Ft28LtAJwIUQVgGgpTkA8yS30WrDnbOuAn6M46TJUySvewlPJhxqQptIEPLONoz+EZuK0lw=="
inBaseDate = str(dt.now())[:10].replace("-", "")
inBaseTime = str(dt.now())[11:13] + "00"
inNumRows = "290"
inPageNum = "1"
inNx = "58"
inNy = "126"

queryParams = '?' + urlencode(
    {
        quote_plus('ServiceKey') : inApiKey,
        quote_plus('numOfRows') : inNumRows,
        quote_plus('pageNo') : inPageNum,
        quote_plus('base_date') : inBaseDate,
        quote_plus('base_time') : inBaseTime,
        quote_plus('nx') : inNx,
        quote_plus('ny') : inNy
     }
)

# 위 변수들을 조합하여 최종적으로 접근할 Url 산출
targetUrl = baseUrl + queryParams

# 확인용 print문
# print(targetUrl)

# 현재 해당 페이지에 접근할 때 SSL 인증 실패 발생. verify 를 false 로 주어서 경고 무시
try:
    resp = requests.get(targetUrl, verify = False)
except Exception as e:
    # 에러가 발생할 경우, logs 폴더 내에 에러 로그를 담은 text 파일을 작성하도록 설정
    f = open("../logs/log-" + str(dt.now())[:19].replace(":", "-") + ".txt", mode = "w", encoding = "utf-8")
    f.write(str(e))
    f.close()
    print(e)

# resp를 xml 파싱
bs = bs4.BeautifulSoup(resp.text, "lxml-xml")

# 파싱한 결과물을 items 태그로 좁힘
itemsTag = bs.find("items")

# items 태그로 좁힌 것들 중 item 태그를 가진 것들을 전부 list 형태로 추출
itemTag = itemsTag.findAll("item")

# 추출한 itemTag 확인용 print문
# for i in range(len(itemTag)):
#     print(i, itemTag[i])
# len(itemTag)

# 카테고리 값과 예보의 결과값, 결과값들을 다시 모을 리스트를 선언
totalFcstList = []
categoryList = []
fcstValueList = []

# 각각의 내용물만 받을 수 있도록 반복문 실행
for i in range(0, len(itemTag)):
    # 칼럼명이 될 category 들을 categoryList 에 받음
    # 조건1. categoryList 에 같은 이름의 category가 존재할 경우 무시
    # 조건2. 만약 걸린 category 이름이 TMN, TMX 일 경우, 아래쪽에서 처리하니 continue 로 다음 반복으로 이동
    if (itemTag[i].category.text not in categoryList):
        categoryList.append(itemTag[i].category.text)
        if itemTag[i].category.text in ("TMN", "TMX"):
            continue
    
    # 각 예보의 value를 추출하여 예보 결과값을 담을 fcstValueList에 추가
    fcstValueList.append(itemTag[i].fcstValue.text)
    
    # 시간 당 예보의 결과는 기본 12개이기에, fcstValueList가 12일 때 조건문 발생
    # 조건1. 다음 인덱스의 카테고리가 TMN, TMX일 경우, 그 시간대의 예보는 13개 요소로 구성됨.
        # 조건1-1. 요소가 13개일 경우, 13번째 카테고리가 TMN, TMX 중 어느 것인지 파악하여 추가
        # 조건1-2. 인덱스가 289, 즉 Num of Rows - 1 rhk 같아지면 out of Range 발생하니 그 이전까지만 걸리도록 조건에 추가
        # 조건1-3. 모든 추가작업이 완료되면 전체 값을 담는 리스트에 append 후 fcstValueLIst는 초기화
    if (len(fcstValueList) == 12):
        if (i < 289) and (itemTag[i + 1].category.text in ("TMN", "TMX")):
            fcstValueList.insert(0, itemTag[i].fcstDate.text)
            fcstValueList.insert(1, itemTag[i].fcstTime.text)
            if itemTag[i + 1].category.text == "TMN":
                fcstValueList.append(itemTag[i + 1].fcstValue.text)
                fcstValueList.append("")
            else:
                fcstValueList.append("")
                fcstValueList.append(itemTag[i + 1].fcstValue.text)
            totalFcstList.append(fcstValueList)
            fcstValueList = []
            
        # 조건2. 요소가 12개일 경우, 특별한 작업 없이 바로 길이만 맞추어서 totalFcstList 에 append 후 초기화
        else:
            fcstValueList.insert(0, itemTag[i].fcstDate.text)
            fcstValueList.insert(1, itemTag[i].fcstTime.text)
            fcstValueList.append("")
            fcstValueList.append("")
            totalFcstList.append(fcstValueList)
            fcstValueList = []

# 반복문 결과 확인용 print문

# print(categoryList)  # 추출한 카테고리명 확인용
# for i in range(0, len(totalFcstList)):
#     print(totalFcstList[i])      # 1일치 단기예보의 각 시간별 데이터 확인용
#     print(len(totalFcstList[i])) # 1일치 단기예보의 각 시간별 데이터의 길이 확인용

# convertColName 함수를 이용하여 category명을 전부 의미하는 내용으로 변환
# nameList = mf.convertColName(categoryList)

# 위 이름 변환 코드의 미사용으로 인하여 임시로 아래 코드로 대체. 추후에 nameList 를 전부 categoryList로 수정 필요.
nameList = categoryList.copy()

# 확인용 print문
# print(nameList)

# 칼럼명 2개를 가장 앞에 추가해주면 되는 것들이기에 insert로 별도 추가
nameList.insert(0, "FCSTDATE")
nameList.insert(1, "FCSTTIME")

# 하나의 행으로 만들기 위하여 새로 리스트 선언 후, 값들이 들은 fcstValueList를 append
rawList = []

# 경로 상에 weather.csv 가 존재하는지의 여부에 따라서 취할 행동 변화. 없으면 write, 있으면 append
for i in range(len(totalFcstList)):
    rawList.append(totalFcstList[i])
    if not os.path.exists("../dataset/weather.csv"):
        outputData = pd.DataFrame(rawList, columns = nameList)
        outputData.to_csv("../dataset/weather.csv", index = False, mode = "w", encoding = "ms949")
        rawList = []
    else:
        outputData = pd.DataFrame(rawList)
        outputData.to_csv("../dataset/weather.csv", index = False, mode = "a", header = False, encoding = "ms949")
        rawList = []

