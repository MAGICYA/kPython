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
    for u in mongo.my_set.find({"code":code,"date":{'$gte':20171201}}):
        lists.append(u)
    # print "============r6============="
    res = kRules.r8(code,lists)
