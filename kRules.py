#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
from numpy import mean, ptp, var, std,median

# r1规则 倍量伸缩
# 成交量 d1<d2*0.9, d2*0.9>d3, d3*0.9>d4
# 成交价 d2均值>d1 open
def r1(code,infolist):
    GroupNum = 4
    resList = []
    if len(infolist) < GroupNum:
        return resList

    for index, item in enumerate(infolist):
        if index < len(infolist) - (GroupNum-1):
            dl = [""]
            pol = [0.0]
            pcl = [0.0]
            vll = [0.0]
            for i in range(index,index+GroupNum):
                dl.append(infolist[i]["date"])
                pol.append(infolist[i]["open"])
                pcl.append(infolist[i]["close"])
                vll.append(infolist[i]["volume"])
            # rule611 成交量1 < 成交量2*0.7  成交量2*0.9 > 成交量3 成交量3*0.9 > 成交量4
            rule611 = (vll[1] < vll[2]*0.7 and vll[2]*0.9 > vll[3] and vll[3]*0.9 > vll[4]) and True or False
            # rule629 第2日均值大于第一日开盘价
            rule629 = (pol[2] + pcl[2])/2 > pol[1]*1.1 and True or False
            # rule610 验证 第5日上涨5%以上
            # rate5 = (pcl[5] - pol[5])/float(pol[5])
            # res1 =  rate5 >0.05 and True or False
            # res2 =  rate5> 0 and rate5 <=0.05 and True or False
            # res3 =  rate5 <= 0 and True or False
            # rule610 验证 第5日上涨5%以上
            # rate6 = (pcl[6] - pol[6])/float(pol[6])
            # res1 =  rate6 >0.0 and True or False
            # res3 =  rate6 <= 0 and True or False
            # if rule611 and rule629 and res3:
            if rule611 and rule629:
                resList.append(dl[1])

    if len(resList)<= 0:
        return resList
    print code + " " + str(resList)
    return resList

# r2 d2大跌
# 成交价 d2跌幅超过5%, d3上涨或跌幅不超过2%
# 成交量 d2 < d1*1.3
def r2(code,infolist):
    GroupNum = 3
    lenList = len(infolist)
    resList = []
    # # 交易期小于40日的滤除
    # if lenList < 40:
    #     return resList
    if lenList < GroupNum:
        return resList
    for index,item in enumerate(infolist):
        if index < lenList - (GroupNum-1):
            dl = [""]
            pol = [0.0]
            pcl = [0.0]
            vll = [0.0]
            for i in range(index,index + GroupNum):
                dl.append(infolist[i]["date"])
                pol.append(infolist[i]["open"])
                pcl.append(infolist[i]["close"])
                vll.append(infolist[i]["volume"])
        # rule626 2日跌幅超过0.07
        rule71 = (pcl[2] - pol[2])/float(pcl[2]) < -0.05 and True or False
        # print "rule71" + rule71 + str((pcl[2] - pol[2])/float(pcl[2]))
        # rule72 2日成交量小于前一日的1.3倍
        rule72 = vll[2] < vll[1]*1.3 and True or False
        # rule73 3日跌幅不超过0.02
        rule73 = (pcl[3] - pol[3])/pol[3] > -0.02 and True or False
        # rule74 2日交易额
        rule74 = vll[3] > 1000000 and True or False
        if rule71 and rule74:
        # if rule71 :
            resList.append(dl[1])
    if len(resList)<= 0:
        return resList
    print code + " " + str(resList)
    return resList


# 多日十字星
def r3(code,infolist):

    if len(infolist)<=1:
        return 0

    pList = []
    dateList = []
    faultList = []
    faultNum = 0
    for index,item in enumerate(infolist):
        pList.append(infolist[index]["open"])
        pList.append(infolist[index]["close"])

    minP = min(pList)
    maxP = max(pList)
    absP1 = abs(maxP - minP)
    # absP2 = abs(maxP - minP)/float(minP)
    rule81 = absP1 <= 20 and True or False
    if rule81 :
        print "-- " + code +" "+ str(minP) +" "+ str(maxP) +" "+ str(absP1)
        return 1
    else:
        # print "-- " + code +" "+ str(minP) +" "+ str(maxP) +" "+ str(absP1)
        return 0

# r4 将军黄金柱
# 成交价
# 成交量
def r4(code,infolist):
    GroupNum = 3
    resList = []
    if len(infolist) < GroupNum:
        return resList
    for index,item in enumerate(infolist):
        if index > len(infolist) - GroupNum:
            break
        dl = [""]
        pol = [0.0]
        pcl = [0.0]
        vll = [0.0]
        for i in range(index,index + GroupNum):
            dl.append(infolist[i]["date"])
            pol.append(infolist[i]["open"])
            pcl.append(infolist[i]["close"])
            vll.append(infolist[i]["volume"])
        # rule626 1日上涨
        rule71 = pcl[1] - pol[1] > 10 and True or False
        # rule72 2,3日收盘价大于d1开盘价
        rule72 = pcl[2] - 5 > pol[1] and pcl[3] - 5 > pol[1] and True or False
        # rule73 2,3日量柱平均小于d1量柱
        rule73 = (vll[2]+vll[3])/2.0 < vll[1] and True or False
        if rule71 and rule72 and rule73:
            resList.append(dl[1])
    return resList

# 最近3日连续上涨
def r5(code,infolist):
    groupNum = 3
    lenList = len(infolist)
    resList = []
    if lenList < groupNum:
        return ""

    index = lenList - groupNum
    dl = [""]
    pol = [0.0]
    pcl = [0.0]
    vll = [0.0]
    for i in range(index,index + groupNum):
        dl.append(infolist[i]["date"])
        pol.append(infolist[i]["open"])
        pcl.append(infolist[i]["close"])
        vll.append(infolist[i]["volume"])
    # rule626 1日上涨
    rule71 = pcl[1] - pol[1] > 5 and True or False
    # rule72 2日上涨
    rule72 = pcl[2] - pol[2] > 5 and True or False
    # rule73 3日上涨
    rule73 = pcl[3] - pol[3] > 5 and True or False
    if rule71 and rule72 and rule73:
        # print "-- " + code
        return code
    else:
        return ""

# 近groupNum日出现infolist最小地量
def r6(code,infolist):
    groupNum = 5
    lenList = len(infolist)
    if lenList < groupNum:
        return ""
    vll = []
    subVll = []
    for index,item in enumerate(infolist):
        vll.append(item["volume"])
    minvol = min(vll)

    for index,item in enumerate(infolist):
        if index >= lenList - groupNum:
            subVll.append(item["volume"])
    minSubVol = min(subVll)
    minSubVolIndex = subVll.index(minSubVol)
    # rule61 近groupNum日最小成交量等于infolist最小成交量
    rule61 = minvol == minSubVol and True or False

    # rule62 昨日成交额大于某个值100000000
    rule62 = int(infolist[lenList-1]["amount"])>100000000  and True or False

    if rule61 and rule62:
        print "-- " + code + " "+str(infolist[lenList-1]["amount"])
        return code
    else:
        return ""

# 近groupNum日出现infolist最小地量
def r7(code,infolist,minAmount):
    groupNum = 1
    lenList = len(infolist)
    if lenList < groupNum:
        return ""
    amount = infolist[lenList-1]
    # rule626 近groupNum日最小成交量等于infolist最小成交量
    rule71 = amount > minAmount and True or False

    if rule71 :
        print "-- " + code
        return code
    else:
        return ""

# 计算标准差
def r8(code,infolist):
    lenList = len(infolist)
    if lenList < 10:
        return ""
    vllist = []
    vllist2 = []
    amlist = []
    for index,item in enumerate(infolist):
        vllist.append(item["volume"])
        amlist.append(item["amount"])

    vlMedian = median(vllist)
    minAmount = min(amlist)

    for index,item in enumerate(vllist):
        vllist2.append(float(item/vlMedian))
    vlStd = std(vllist2)
    # if vlStd > 0 :
    if vlStd > 0 and vlStd < 0.2 and minAmount > 80000000:
    # if vlStd >= 50000000 :
        # print infolist
        print ("%s,%15.2f" % (code,vlStd))
