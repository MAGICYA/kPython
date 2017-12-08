# -- coding: utf-8 --
import sys
import json
import urllib
import urllib2
import pandas as pd
import re
import kcommon

def rule4(code,infolist):
    if len(infolist)<=0:
        return 0
    ministFlag = -1
    LastAmount = 0
    LastVol = 0
    AmountList = []
    for index, item in enumerate(infolist):
        if item[kcommon.stdate] == 20171201000000:
            if item[kcommon.stopen] > item[kcommon.stclose]:
                return 0
            LastAmount = item[kcommon.stamount]
            LastVol = item[kcommon.stvol]
    for index, item in enumerate(infolist):
        if item[kcommon.stdate] > 20170901000000:
            AmountList.append(item[kcommon.stamount])
    if len(AmountList) <= 0 or LastAmount == 0 or LastVol < 100000000:
        return 0
    if min(AmountList) != LastAmount:
        return 0
    print "---------------" + code + " success -------------- LastAmount" + str(LastAmount)
    # print AmountList
    return 1


reload(sys)
sys.setdefaultencoding('utf8')
load_dict = {}

beginCode = 0
endCode = 3000
step = 100

totalNum = 0;
resList = [];
for i in range(beginCode,endCode):
    if i%100 == 0:
        subBeginCode = i
        subEndCode = subBeginCode + step
        filename = "stockListInfo" + str(subBeginCode)+"-"+str(subEndCode)+".json"
        with open(filename,'r') as load_f:
            load_dict = json.load(load_f)

        for code in load_dict:
            text = load_dict[code].encode('unicode-escape').decode('string_escape')
            count = 0
            flag = 1
            user_obj = eval(text)
            res = rule4(code,user_obj['Data'][0])
            if res==1:
                resList.append(code)
                totalNum += 1

print "totalNum = " + str(totalNum)
file_object = open('res-rule4.csv', 'w+a')#用w模式打开一个已存在文件时，原有内容会被清空
file_object.write(str(resList))
file_object.close();
