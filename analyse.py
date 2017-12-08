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
endCode = 100
filename = "stockListInfo" + str(beginCode)+"-"+str(endCode)+".json"

with open(filename,'r') as load_f:
    load_dict = json.load(load_f)
    # all_the_text = load_f.read()
    # # print type(all_the_text)
    #
    # user_obj = eval(all_the_text)
    # # print user_obj

for code in load_dict:

    text = load_dict[code].encode('unicode-escape').decode('string_escape')
    count = 0
    flag = 1

    user_obj = eval(text)

    infolist = user_obj['Data'][0]
    # print infolist
    if len(infolist)<=0:
        continue;
    # print key
    # print infolist
    tmpStr = ""
    for i, val in enumerate(infolist):
        date = val[0]
        if date != 20171201000000 and date != 20171129000000 and date != 20171130000000:
            continue
        LastClose = val[1]
        Open = val[2]
        Close = val[3]
        Amount = val[6]
        # tmpStr.append(" LastClose %5d Open %5d Amount d\n" % (LastClose, Open, Amount))
        s = "date %s LastClose %5d Open %5d Close %5d Amount %d\n" % (date, LastClose, Open,Close, Amount)
        tmpStr += s
        # print("LastClose %d Open %d Amount %d" % (LastClose,Open,Amount))
        if Open >= LastClose and Close >= Open:
        # if Open >= LastClose :
            a=0
        else:
            flag = 0

    # arr = infolist;
    # if arr[0][6] < arr[1][6] or arr[1][6] < arr[2][6]:
    #     flag = 0

    if flag == 1 and len(tmpStr) > 0:
        print str(count)+" "+code+" success"
        print tmpStr
    # else:
        # print str(count)+" "+code+" false"
        # print tmpStr
