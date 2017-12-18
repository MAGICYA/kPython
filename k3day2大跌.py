# -- coding: utf-8 --
import sys
import json
from kMongoDB import kMongoDB
import kRules

reload(sys)
sys.setdefaultencoding('utf8')
# 加载数据
mongo = kMongoDB()
codeList = mongo.dbfindcode()

resCodes = []
for code in codeList:
    findDic = {}
    findDic["code"] = code
    lists = []
    # lte设为最后一日+（GroupNum-1)个交易日，不然会漏掉最后几天
    for u in mongo.my_set.find({"code":code,"date":{'$gte':20171211,'$lte':20171215}}):
        lists.append(u)
    # print "============r6============="
    res = kRules.r2(code,lists)
    if len(res)>0:
        s = code + ","
        resCodes.append(s)
print len(resCodes)
# print resCodes
