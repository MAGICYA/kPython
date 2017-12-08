import sys
import json
import urllib
import urllib2
import pandas as pd
import re
from kMongoDB import kMongoDB
import kcommon

reload(sys)
sys.setdefaultencoding('utf8')
stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'

def saveToDB(mongo,code,infos):
    if len(infos["Data"][0])<=0:
        return
    for item in infos["Data"][0]:
        itemDic = {}
        itemDic["code"] = code.encode('unicode-escape').decode('string_escape')
        itemDic["date"] = item[kcommon.stdate]/1000000
        itemDic["lastclose"] = item[kcommon.stlastclose]
        itemDic["open"] = item[kcommon.stopen]
        itemDic["close"] = item[kcommon.stclose]
        itemDic["high"] = item[kcommon.sthigh]
        itemDic["low"] = item[kcommon.stlow]
        itemDic["volume"] = item[kcommon.stvolume]
        itemDic["amount"] = item[kcommon.stamount]
        print itemDic
        mongo.insert(itemDic)


def urlTolist(url):
    allCodeList = []
    html = urllib2.urlopen(url).read()
    html = html.decode('gbk')
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0]=='6' or item[0]=='3' or item[0]=='0':
            allCodeList.append(item)
    return allCodeList


allCodelist = urlTolist(stock_CodeUrl)

beginCode = 10
endCode = 3600
step = 100

SZCode = "szse"
SHCode = "sse"
stockCode = ""

mongo = kMongoDB()

for i in range(beginCode,endCode):
    if i%100 == 0:
        subBeginCode = i
        subEndCode = subBeginCode + step
        filename = "stockdata" + str(subBeginCode)+"-"+str(subEndCode)+".json"
        print filename
        subCodeList = allCodelist[subBeginCode:subEndCode]
        infodic = {}
        count = 0
        for code in subCodeList:
            count+=1
            if int(code)>600000:
                stockCode = SHCode
            else:
                stockCode = SZCode
            codeurl = 'http://webstock.quote.hermes.hexun.com/a/kline?code='+stockCode+code+'&start=20171207150000&number=-1&type=5&callback=callback'
            # print codeurl
            response = urllib2.urlopen(codeurl)
            s = json.loads(response.read()[9:-2])
            saveToDB(mongo,code,s)
        #     if len(s["Data"])!=0 and len(s["Data"][0])!=0:
        #         infodic[code] = s["Data"][0]
        #     else:
        #         infodic[code] = []
        # with open(filename,'a') as outfile:
        #     json.dump(infodic,outfile,ensure_ascii=False)
        #     outfile.write('\n')

        # print "=======================get " + str(count) + " info , end========================="



# for code in allCodelist:
#
#     count=count+1
#
#     if count >= 300 and count < 400:
#         a=0
#     else:
#         continue
#
#     codeurl = 'http://webstock.quote.hermes.hexun.com/a/kline?code=sse'+code+'&start=20171201150000&number=-4&type=5&callback=callback'
#     response = urllib2.urlopen(codeurl)
#     s = response.read()[9:-2]
#     # print s
#     text = json.loads(s)
#
#     flag = 1;
#     infolist = text['Data'][0]
#     if len(infolist)<=0:
#         continue;
#     # print code
#     # print infolist
#     tmpStr = ""
#     for i, val in enumerate(infolist):
#
#         date = val[0]
#
#         if date != 20171201000000 and date != 20171129000000 and date != 20171130000000:
#             continue
#         LastClose = val[1]
#         Open = val[2]
#         Close = val[3]
#         Amount = val[6]
#         # tmpStr.append(" LastClose %5d Open %5d Amount d\n" % (LastClose, Open, Amount))
#         s = "date %s LastClose %5d Open %5d Amount %d\n" % (date, LastClose, Open, Amount)
#         tmpStr += s
#         # print("LastClose %d Open %d Amount %d" % (LastClose,Open,Amount))
#         if Open >= LastClose and Close >= Open:
#         # if Open >= LastClose :
#             a=0
#         else:
#             flag = 0
#
#     arr = infolist;
#     if arr[0][6] < arr[1][6] or arr[1][6] < arr[2][6]:
#         flag = 0
#
#     if flag == 1 and len(tmpStr) > 0:
#         print str(count)+" "+code+" success"
#         print tmpStr
#     # else:
#         # print str(count)+" "+code+" false"
#         # print tmpStr



# readDic = {}
# with open("test.json",'r') as load_f:
#     all_the_text = load_f.read()
#     if len(all_the_text) > 0:
#         readDic = eval(all_the_text)
# for key in readDic:
#     infodic[key] = readDic[key]
