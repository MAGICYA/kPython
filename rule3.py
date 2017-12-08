import sys
import json
import urllib
import urllib2
import pandas as pd
import re

reload(sys)
sys.setdefaultencoding('utf8')
load_dict = {}

beginCode = 0
endCode = 3000
step = 100

for i in range(beginCode,endCode):
    if i%100 == 0:
        subBeginCode = i
        subEndCode = subBeginCode + step
        filename = "stockListInfo" + str(subBeginCode)+"-"+str(subEndCode)+".json"
        with open(filename,'r') as load_f:
            load_dict = json.load(load_f)

        for code in load_dict:
            # print "---------------" + code + "--------------"
            text = load_dict[code].encode('unicode-escape').decode('string_escape')
            count = 0
            flag = 1

            LastClose = 1
            Open = 2
            Close = 3
            Amount = 6
            infolist = [LastClose, Open, Close, Amount]
            user_obj = eval(text)

            infolist = user_obj['Data'][0]
            # print infolist
            if len(infolist)<=0:
                continue;
            # print key
            # print infolist
            tmpStr = ""
            SubInfoDic = {}
            tmpStr
            rule2Flag = 0
            dateArr = [];
            codeStr = "---------------" + code + "--------------"
            dateArr.append(codeStr)
            for i in range(0,len(infolist)-1):
                rate = (infolist[i][Close] - infolist[i][Open])/float(infolist[i][Open])
                if infolist[i][0] > 20171110000000 and rate > 0.03 and (infolist[i][Open]+infolist[i][Close])/2 > (infolist[i-1][Open]+infolist[i-1][Close])/2:
                    for j in range(i+4,len(infolist)):
                        subPriceflag = 1
                        for k in range(i,j):
                            if (infolist[k][Open]+infolist[k][Close])/2 < infolist[i][Open]:
                                subPriceflag = 0
                        if subPriceflag == 1:
                            if abs(infolist[i][Open] - infolist[j][Open]) < 0.02  and infolist[j][Close] > infolist[j][Open] and (infolist[j][Open]+infolist[j][Close])/2 > (infolist[j-1][Open]+infolist[j-1][Close])/2:
                                rule2Flag += 1
                                dateArr.append("- - - - ")
                                dateArr.append(infolist[i])
                                dateArr.append(infolist[j])
            if rule2Flag > 0:
                codeStr = "---------------" + code + " " + str(rule2Flag) + "--------------"
                dateArr.append(codeStr)
                for val in dateArr:
                    print val
