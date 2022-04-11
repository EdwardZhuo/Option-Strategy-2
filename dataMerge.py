#zhuojinjun

import pandas as pd
import numpy as np
import os
from position import *
 
os.chdir('C:/Users/jrqh/Desktop/test/data')
fileDir = os.getcwd()
# get all file name
CsvList = []
for root,dirs,files in os.walk(fileDir):
    for file in files:
        if os.path.splitext(file)[1] == '.csv':
            CsvList.append(file)

data = pd.DataFrame()
data0 = pd.read_csv('C:/Users/jrqh/Desktop/test/10003549.csv',usecols=[1,2,6,7,9,10])

numCsvList = len(CsvList)
for i in list(range(numCsvList)):
    datai = pd.read_csv(CsvList[i],usecols=[1,2,6,7,9,10])
    datai.rename(columns={'thscode':'thscode%s'%i,'close':'close%s'%i,'DOM':'DOM%s'%i,'deltacash':'deltacash%s'%i,'delta':'delta%s'%i}, inplace=True) 
    data0 = pd.merge(data0,datai,on='time')
data0.to_csv('ALL2.csv',index=0)


 


