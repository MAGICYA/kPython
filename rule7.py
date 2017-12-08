# -- coding: utf-8 --
import sys
import json
import urllib
import urllib2
import pandas as pd
import re
import kcommon
from kMongoDB import kMongoDB

def rule5(code,infolist):

    # if len(infolist)<=60:
    #     return -1

    priseP = 10
    amountP = 0.05
    ministFlag = -1
    LastAmount = 0
    LastVol = 0
    priceList = []

    subList = []
    dateList = []
    faultList = []

    for index,item in enumerate(infolist):
        if index > len(infolist)-4:
            break
        d1  = infolist[index]["date"]
        po1 = float(infolist[index]["open"])
        pc1 = float(infolist[index]["close"])
        vl1 = float(infolist[index]["volume"])

        d2  = infolist[index+1]["date"]
        po2 = float(infolist[index+1]["open"])
        pc2 = float(infolist[index+1]["close"])
        vl2 = float(infolist[index+1]["volume"])

        d3  = infolist[index+2]["date"]
        po3 = float(infolist[index+2]["open"])
        pc3 = float(infolist[index+2]["close"])
        vl3 = float(infolist[index+2]["volume"])
        # rule626 2日跌幅超过0.05
        rule71 = (pc2 - po2)/po2 < -0.07 and True or False
        # rule72 2日成交量小于前一日的1.3倍
        rule72 = vl2 < vl1*1.3 and True or False
        # rule73 3日跌幅不超过0.02
        rule73 = (pc3 - po3)/po3 > -0.02 and True or False
        # rule74 1日跌幅不超过0.02
        # rule74 = (pc1 - po1)/po1 > -0.02 and False or True
        if rule71 and rule72 and rule73:
            dateList.append(infolist[index]["date"])

    if len(dateList) <= 0:
        return 0
    # print "---------------" + code + " success4  " + str(len(dateList)) + "down" + str(len(faultList))
    print "---------------" + code + " success4"
    print " Big down " + str(dateList)
    return len(dateList)

if __name__=="__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')
    load_dict = {}

    beginCode = 0
    endCode = 3600
    step = 100

    totalNum = 0;
    falseNum = 0
    resList = "";

    mongo = kMongoDB()
    res = mongo.dbfindcode()
    for code in res:
        findDic = {}
        findDic["code"] = code
        # infos = mongo.dbfind(findDic)
        lists = mongo.dbfindlist2(code,20171205,20171208)
        res = rule5(code,lists)
        tmps = ""
        resList = ""
        totalNum = 0
        if res==1:
            tmps = "\'"+code+"\',"
            resList += tmps
            totalNum += 1
        elif res!=-1:
            falseNum += 1
    # print "总概率 = " + str(float(totalNum)/(totalNum+falseNum))
    # print str(resList)

























    #
    # for i in range(beginCode,endCode):
    #     if i%100 == 0:
    #         subBeginCode = i
    #         subEndCode = subBeginCode + step
    #         filename = "stockListInfo" + str(subBeginCode)+"-"+str(subEndCode)+".json"
    #         with open(filename,'r') as load_f:
    #             load_dict = json.load(load_f)
    #
    #         for code in load_dict:
    #             codeDic = {  }
    #             codeDic["code"] = code
    #             mongo.find(codeDic)
    #             text = load_dict[code].encode('unicode-escape').decode('string_escape')
    #             user_obj = eval(text)
    #             res = rule5(code,user_obj['Data'][0])
    #             if res==1:
    #                 tmps = "\'"+code+"\',"
    #                 resList += tmps
    #                 totalNum += 1
    #             elif res!=-1:
    #                 falseNum += 1
    # print "总概率 = " + str(float(totalNum)/(totalNum+falseNum))
    # print str(resList)
    #
    #
    #
    #
    #
    #

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
