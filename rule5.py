# -- coding: utf-8 --
import sys
import json
import urllib
import urllib2
import pandas as pd
import re
import kcommon
def calcMaxPrice(beginDate,infolist):
    priceList = []
    if len(infolist)<=0:
        return 0
    for index, item in enumerate(infolist):
        theDate = item[kcommon.stdate]
        if float(theDate) < float(beginDate):
            priceList.append(item[kcommon.stopen])
            priceList.append(item[kcommon.stclose])
    if len(priceList)<=0:
        return 0
    return max(priceList)

def rule5(code,infolist):

    if len(infolist)<=0:
        return 0

    beginDate = 20171101000000
    endDate = 20171120000000
    priseP = 10
    amountP = 0.05
    ministFlag = -1
    LastAmount = 0
    LastVol = 0
    priceList = []

    subList = []
    flag = 1

    for index, item in enumerate(infolist):
        theDate = item[kcommon.stdate]
        # print float(theDate) > float(beginDate) and float(theDate) < float(endDate)
        if float(theDate) > float(beginDate) and float(theDate) < float(endDate):
            subList.append(item)
            priceList.append(item[kcommon.stopen])
            priceList.append(item[kcommon.stclose])

    if len(subList) <= 3:
        return 0
    minPrice = min(priceList)
    maxPrice = max(priceList)
    mPrice = calcMaxPrice(beginDate,infolist)
    if(mPrice <= 0):
        return 0
    thePrice = abs(maxPrice - minPrice)
    if thePrice > priseP:
        flag = 0

    if flag == 0:
        # print "---------------" + code + " fault -------------- LastAmount"
        # print("minSubPrice   %-12.3f maxSubPrice    %-12.3f thePrice    %-12.3f priseP   %-5f" % (float(abs(minPrice)),float(abs(maxPrice)),thePrice,float(priseP)))
        return 0
    print("minSubPrice   %-12.3f maxSubPrice    %-12.3f thePrice    %-12.3f priseP   %-5f" % (float(abs(minPrice)),float(abs(maxPrice)),thePrice,float(priseP)))
    print "---------------" + code + " success4 -------------- LastAmount"
    return 1


reload(sys)
sys.setdefaultencoding('utf8')
load_dict = {}

beginCode = 0
endCode = 3000
step = 100

totalNum = 0;
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

print "totalNum = " + str(totalNum)
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
