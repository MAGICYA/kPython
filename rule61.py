# -- coding: utf-8 --
import sys
import json
import urllib
import urllib2
import pandas as pd
import re
import kcommon

def rule5(code,infolist):

    if len(infolist)<=0:
        return -1

    beginDate = 20171010000000
    endDate = 20171206000000
    priseP = 10
    amountP = 0.05
    ministFlag = -1
    LastAmount = 0
    LastVol = 0
    priceList = []

    subList = []
    dateList = []
    faultList = []
    for index, item in enumerate(infolist):
        theDate = item[kcommon.stdate]
        if float(theDate) > float(beginDate) and float(theDate) < float(endDate):
            subList.append(item)

    if len(subList) < 4:
        return -1
    for index, item in enumerate(subList):
        if index < len(subList) - 3:
            d1  = subList[index][kcommon.stdate]
            po1 = float(subList[index][kcommon.stopen])
            pc1 = float(subList[index][kcommon.stclose])
            am1 = float(subList[index][kcommon.stamount])

            if float(d1) <= 20171130000000:
                continue
            d2  = subList[index+1][kcommon.stdate]
            po2 = float(subList[index+1][kcommon.stopen])
            pc2 = float(subList[index+1][kcommon.stclose])
            am2 = float(subList[index+1][kcommon.stamount])

            d3  = subList[index+2][kcommon.stdate]
            po3 = float(subList[index+2][kcommon.stopen])
            pc3 = float(subList[index+2][kcommon.stclose])
            am3 = float(subList[index+2][kcommon.stamount])

            d4  = subList[index+3][kcommon.stdate]
            po4 = float(subList[index+3][kcommon.stopen])
            pc4 = float(subList[index+3][kcommon.stclose])
            am4 = float(subList[index+3][kcommon.stamount])

            # d5  = subList[index+4][kcommon.stdate]
            # po5 = float(subList[index+4][kcommon.stopen])
            # pc5 = float(subList[index+4][kcommon.stclose])
            # am5 = float(subList[index+4][kcommon.stamount])
            #
            # d6  = subList[index+5][kcommon.stdate]
            # po6 = float(subList[index+5][kcommon.stopen])
            # pc6 = float(subList[index+5][kcommon.stclose])
            # am6 = float(subList[index+5][kcommon.stamount])
            #
            # d7  = subList[index+6][kcommon.stdate]
            # po7 = float(subList[index+6][kcommon.stopen])
            # pc7 = float(subList[index+6][kcommon.stclose])
            # am7 = float(subList[index+6][kcommon.stamount])
            # rule6规则
            # 条件
            # 成交量1 < 成交量2*0.9  成交量2*0.9 > 成交量3 成交量3*0.9 > 成交量4
            # 成交价2 跌
            # 成交价3 跌
            # 结果 成交价4 不跌

            # rule611 成交量1 < 成交量2*0.7  成交量2*0.9 > 成交量3 成交量3*0.9 > 成交量4
            rule611 = (am1 < am2*0.7 and am2*0.9 > am3 and am3*0.9 > am4) and 1 or 0
            # # rule612 am3,am4的平均值 小于 am2
            # rule612 = (am3+ am4)/2 < am2*0.5 and True or False
            #
            # # rule621 第1日涨
            # rule621 = pc1 - po1>0 and 1 or 0
            # # rule622 第2日涨
            # rule622 = pc2 - po2>0 and 1 or 0
            # # rule623 第3日跌
            # rule623 = pc3 - po3<0 and 1 or 0
            # # rule624 第4日跌
            # rule624 = pc4 - po4<0 and 1 or 0
            # # rule625 第5日涨
            # rule625 = pc5 - po5> 0 and True or False
            # # rule626 第5日涨幅超过0.01
            # rule626 = (pc5 - po5)/po5 > 0.01 and True or False
            # # rule627 第6日涨幅超过0.01
            # rule627 = (pc6 - po6)/po6 > 0.01 and True or False
            # # rule628 第7日涨幅超过0.01
            # rule628 = (pc7 - po7)/po7 > 0.01 and True or False
            # rule629 第2日均值大于第一日开盘价
            rule629 = (po2 + pc2)/2 > po1*1.1 and True or False

            if rule611 and rule629:
                dateList.append(subList[index][kcommon.stdate])

    if len(dateList) < 1:
        return -1
    print "---------------" + code + " success4"
    print "raise " + str(dateList)

reload(sys)
sys.setdefaultencoding('utf8')
load_dict = {}

beginCode = 0
endCode = 3600
step = 100

totalNum = 0;
falseNum = 0
resList = "";
for i in range(beginCode,endCode):
    if i%100 == 0:
        subBeginCode = i
        subEndCode = subBeginCode + step
        filename = "stockListInfo" + str(subBeginCode)+"-"+str(subEndCode)+".json"
        with open(filename,'r') as load_f:
            load_dict = json.load(load_f)

        for code in load_dict:
            text = load_dict[code].encode('unicode-escape').decode('string_escape')
            user_obj = eval(text)
            res = rule5(code,user_obj['Data'][0])
            if res==1:
                tmps = "\'"+code+"\',"
                resList += tmps
                totalNum += 1
            elif res!=-1:
                falseNum += 1
print "总概率 = " + str(float(totalNum)/(totalNum+falseNum))
print str(resList)







# standadAmount = 0.0
# for index, item in enumerate(subList):
#     standadAmount += item[kcommon.stamount]
# standadAmount = standadAmount/len(subList)
# print "---------------" + code + " begin4--------------"
# # print "standadAmount " + str(standadAmount)
# flag = 1
# for index, item in enumerate(subList):
#     Close = item[kcommon.stclose]
#     Open = item[kcommon.stopen]
#     Amount = item[kcommon.stamount]
#     priceIncrease = (Close - Open)
#     amountIncrease = (Amount-standadAmount)/float(standadAmount)
#     if abs(priceIncrease) > priseP:
#         flag = 0
#     # if abs(amountIncrease) > amountP:
#     #     flag = 0
#     print item
#     print("pi   %-12.3f ai    %-12.3f flag   %-5f" % (float(abs(priceIncrease)),float(abs(amountIncrease)),float(flag)))
#     print("Open %-12.3f Close %-12.3f Amount %-10f" % (Open,Close,Amount))
#     if flag == 0:
#         break;
