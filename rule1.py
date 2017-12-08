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
endCode = 3600
step = 100

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

            datelist = [20171129000000,20171130000000,20171201000000]
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

            for i, val in enumerate(infolist):
                for date in datelist:
                    if date == val[0]:
                        SubInfoDic[date] = val


            if len(SubInfoDic) == len(datelist):
                rule11 = 1
                for date in datelist:
                    val = SubInfoDic[date]
                    if val[LastClose] > val[Open] or val[Open] >  val[Close]:
                        rule11 = 0

                if rule11 == 1:
                    print("-----------%s rull 1-1---------------" % (code))
                    for date in datelist:
                        val = SubInfoDic[date]

                        print("%d %5d %5d %5d %d" % (val[0], val[LastClose], val[Open], val[Close], val[Amount]))



    # for date in datelist:
    #     for info in infolist:
    #         for i, val in enumerate(infolist):
    #             if date == val[0]:
    #                 SubInfo[date] = val[info]

    # if Close[datelist[0]] < Open[datelist[0]] or Close[datelist[1]] < Open[datelist[1]] or Close[datelist[2]] < Open[datelist[2]]:
    #     flag = 0
    #     tmpStr = "Close < Open flag = 0"
    #     print tmpStr
    #
    # if flag == 1 and len(tmpStr) > 0:
    #     print str(count)+" "+code+" success"
    # else:
    #     print str(count)+" "+code+" false"

    # print SubInfo
    # for i, val in enumerate(infolist):
    #     date = val[0]
    #     if date != date1 and date != date2 and date != date3:
    #         continue
    #     LastClose = val[1]
    #     Open = val[2]
    #     Close = val[3]
    #     Amount[date] = val[6]
    #     # tmpStr.append(" LastClose %5d Open %5d Amount d\n" % (LastClose, Open, Amount))
    #     s = "date %s LastClose %5d Open %5d Close %5d Amount %d\n" % (date, LastClose, Open,Close, Amount[date])
    #     tmpStr += s
    #     # print("LastClose %d Open %d Amount %d" % (LastClose,Open,Amount))
    #     if Open >= LastClose and Close >= Open:
    #     # if Open >= LastClose :
    #         a=0
    #     else:
    #         flag = 0
    #
    # if Amount.has_key(date3) and Amount.has_key(date2) and Amount.has_key(date1):
    #     if Amount[date3] > Amount[date2] or Amount[date2] > Amount[date1]:
    #         print str(Amount[date3]) + " " +str(Amount[date2]) + " " + str(Amount[date1]) + " " + "flag=0"
    #         flag = 0
    #     # else:
    #         # print str(Amount[date3]) + " " + str(Amount[date2]) + " " + str(Amount[date1])
    # # else:
    #     # flag = 0
