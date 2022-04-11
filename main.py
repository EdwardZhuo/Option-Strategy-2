#zhuojinjun
import pandas as pd
import numpy as np
import os
from position import *
 
def getDictKey(dic, value):
    keys = list(dic.keys())
    values = list(dic.values())
    idx = values.index(value)
    key = keys[idx]
    return key


data0 = pd.read_csv('C:/Users/ZJJ/Desktop/test/dataMerge.csv',header = 0,encoding='gb18030') 

numBar = data0.shape[0]
numCol = data0.shape[1]
# print(numBar)
# print(numCol)

numContracts = int((numCol-1)/5)-1
# print(numContracts)

deltacashMax = 20000.0
deltacashMin = 0.0
thresholdmax = 200000
thresholdmin = -200000
totalNum = 200

pos = position()

for i in list(range(1,numBar)):
    # 判断是否有仓位
    cc, cn, pc, pn = pos.getPosition()
    if cn - 0 < 1: # 无仓位
        contractsToBeConsiderDict = {}
        contractsToBeConsiderList = []
        for j in list(range(1,numContracts+1)):
            col = 'deltacash'+ str(j)
            deltacash = abs(data0.at[i, col])
            # print(data0.at[i, col])
            if deltacash < deltacashMax and deltacash > deltacashMin:
                contractsToBeConsiderDict[j] = data0.at[i, col]
                contractsToBeConsiderList.append(data0.at[i, col])
                # print(contractsToBeConsiderDict)
            else:
                pass
        if len(contractsToBeConsiderList) < 2:
            continue
        else:
            judgeA = 0.0
            judgeB = 0.0
            for k in contractsToBeConsiderList:
                if k > 0.0:
                    judgeA = 1.0
                else: 
                    pass
                
                if k < 0.0:
                    judgeB = 1.0
                else: 
                    pass
            if judgeA * judgeB < 0.5:
                pass
            else:
                callDeltacash = max(contractsToBeConsiderList)
                putDeltacash = min(contractsToBeConsiderList)
                callContract = getDictKey(contractsToBeConsiderDict, callDeltacash)
                putContract = getDictKey(contractsToBeConsiderDict, putDeltacash)
                # a+b = 200
                # a*buy = -b*sell
                # a+b = b(-sell/buy+1) = 200
                putNum = int(totalNum/(-putDeltacash/callDeltacash+1))
                callNum = (totalNum - putNum)
                callCol = "close" + str(callContract)
                # print(callCol)
                putCol = "close" + str(putContract)
                # print(data0.at[i, 'close2'])
                callPrice = float(data0.at[i, callCol])
                putPrice = float(data0.at[i, putCol])
                pos.openCall(str(callContract),callPrice,callNum)
                pos.openPut(str(putContract),putPrice,putNum)
    else:
        callDeltacashCol = 'deltacash'+ str(cc)
        putDeltacashCol = 'deltacash'+ str(pc)

        sumDeltacash = data0.at[i, callDeltacashCol] * cn + data0.at[i, putDeltacashCol] * pn
        
        if sumDeltacash < thresholdmax and sumDeltacash > thresholdmin:
            continue
        else:
            callCol = "close" + str(callContract)
            putCol = "close" + str(putContract)
            callPrice = data0.at[i, callCol]
            putPrice = data0.at[i, putCol]
            pos.closeCall(str(callContract),callPrice)
            pos.closePut(str(putContract),putPrice)
print(pos.getProfit())
print(pos.getLog())





                
        
    
 


