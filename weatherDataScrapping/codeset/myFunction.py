#!/usr/bin/env python
# coding: utf-8

# In[2]:
import datetime as dt

def todayInfo():
    todayIs = dt.datetime.now()
        
    year = str(todayIs.year)
    if len(str(todayIs.month)) != 1:
        month = str(todayIs.month)
    else:
        month = "0" + str(todayIs.month)
    day = str(todayIs.day)
    
    return year + month + day


# In[3]:


def timeInfo():
    timeIs = dt.datetime.now()
    
    if (timeIs.hour) < 4:
        hours = "0200"
    elif (timeIs.hour) < 7:
        hours = "0500"
    elif (timeIs.hour) < 10:
        hours = "0800"
    elif (timeIs.hour) < 13:
        hours = "1100"
    elif (timeIs.hour) < 16:
        hours = "1400"
    elif (timeIs.hour) < 19:
        hours = "1700"
    elif (timeIs.hour) < 22:
        hours = "2000"
    else:
        hours = "2300"
        
    return hours


# In[12]:


def convertColName(targetList):

    newList = []
    
    for i in range(0, len(targetList)):

        if targetList[i] == "TMP":
            newList.append("1시간 기온 (단위 : ℃)")
        elif targetList[i] == "POP":
            newList.append("강수확률 (단위 : %)")
        elif targetList[i] == "PTY":
            newList.append("강수형태")
        elif targetList[i] == "PCP":
            newList.append("시간 당 강수량 (단위 : mm)")
        elif targetList[i] == "REH":
            newList.append("습도 (단위 : %)")
        elif targetList[i] == "SNO":
            newList.append("시간 당 적설량 (단위 : cm)")
        elif targetList[i] == "SKY":
            newList.append("하늘상태")
        elif targetList[i] == "TMN":
            newList.append("일 최저기온 (단위 : ℃)")
        elif targetList[i] == "TMX":
            newList.append("일 최고기온 (단위 : ℃)")
        elif targetList[i] == "UUU":
            newList.append("풍속/동서성분 (단위 : m/s)")
        elif targetList[i] == "VVV":
            newList.append("풍속/남북성분 (단위 : m/s)")
        elif targetList[i] == "WAV":
            newList.append("파고 (단위 : M)")
        elif targetList[i] == "VEC":
            newList.append("풍향 (단위 : deg)")
        elif targetList[i] == "WSD":
            newList.append("풍속 (단위 : m/s)")
        else:
            pass
        
    return newList

