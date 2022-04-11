#zhuojinjun

from iFinDPy import *
import time  
import datetime  
import numpy as np
import pandas as pd
from math import log,sqrt,exp
from scipy import stats

thsLogin = THS_iFinDLogin('username','password')
# '''
def bsm_call_value(s0,k,t,r,sigma):
    d1 = ( log( s0/k ) + ( r + 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    d2 = ( log( s0/k ) + ( r - 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    value = ( s0*stats.norm.cdf( d1,0.,1. ) - k*exp( -r*t )*stats.norm.cdf( d2,0.,1 ))
    return value
def bsm_put_value(s0,k,t,r,sigma):
    d1 = ( log( s0/k ) + ( r + 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    d2 = ( log( s0/k ) + ( r - 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    value = -( s0*stats.norm.cdf( -d1,0.,1. ) + k*exp( -r*t )*stats.norm.cdf( -d2,0.,1 ))
    return value
def bsm_vega(s0,k,t,r,sigma):
    d1 = log( s0/k ) + ( r + 0.5*sigma**2 )*t/( sigma*sqrt(t) )
    vega = s0*stats.norm.cdf(d1,0.,1.)*sqrt(t)
    return vega
#牛顿迭代法求波动率 
def bsm_call_imp_vol_newton(s0, k, t, r, c0, sigma_est, it = 100):    
    for i in range(it):
        sigma_est -= ((bsm_call_value(s0, k, t, r, sigma_est) - c0)/ 
                    bsm_vega(s0, k, t, r, sigma_est))
    return sigma_est
def bsm_put_imp_vol_newton(s0, k, t, r, c0, sigma_est, it = 100):    
    for i in range(it):
        sigma_est -= ((bsm_put_value(s0, k, t, r, sigma_est) - c0)/ 
                    bsm_vega(s0, k, t, r, sigma_est))
    return sigma_est
def CALDOM(date1,date2):  
    d1=time.strptime(date1,"%Y-%m-%d %H:%M")        
    d2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")  
    D1=datetime.datetime(d1[0],d1[1],d1[2])       
    D2=datetime.datetime(d2[0],d2[1],d2[2])
    DOM1=(D2-D1).days
    if DOM1>35 or DOM1<8:
        DOM = 1000
        return DOM
    else: 
        return DOM1
def c_delta(s0,k,t,r,sigma):
    d1 = ( log( s0/k ) + ( r + 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    delta =stats.norm.cdf( d1,0.,1. ) 
    #print('cvalue',value)
    return delta
def p_delta(s0,k,t,r,sigma):
    d1 = ( log( s0/k ) + ( r + 0.5*sigma**2 )*t )/( sigma*sqrt(t) )
    delta = stats.norm.cdf( d1,0.,1. ) - 1.0
    #print('cvalue',value)
    return delta

class DataDownload:
    def __init__(self):
        pass
    def option(self,contract1,begintime1,endtime1,contract2,begintime2,endtime2,name,k,ti,multi,callOrPut):
        stock = THS_HighFrequenceSequence(contract1,'open;high;low;close','CPS:no,baseDate:1900-10-10,MaxPoints:500000,Fill:Previous,Interval:60',begintime1,endtime1,True)
        stockData = THS_Trans2DataFrame(stock)
        optioncontrast = THS_HighFrequenceSequence(contract2,'open;high;low;close','CPS:no,baseDate:1900-10-10,MaxPoints:500000,Fill:0.001,Interval:60',begintime2,endtime2,True)
        thsData = THS_Trans2DataFrame(optioncontrast)
        DOM=[]
        for i in range(thsData.shape[0]):
            DOM.append(CALDOM(thsData.time[i],ti))
        thsData.insert(6,'DOM',DOM)
        sss= stockData['close'].astype(float)
        price = thsData['close'].astype(float)
        dofm = thsData['DOM']/365
        vol=[]
        sigma_init=1
        for i in range(thsData.shape[0]):
            if price[i]>9.0 or dofm[i]>2.7:
                vol.append(10)
            else:
                if callOrPut == "认购":
                    # print(sss[i],k,dofm[i],0.02,price[i])
                    dd=bsm_call_imp_vol_newton(sss[i],k,dofm[i],0.02,price[i],sigma_init,it=100)
                    if dd>0.01 and dd <1:
                        vol.append(dd)
                    else:
                        ii=i-1
                        if vol[ii] < 5.0:
                            vol.append(vol[ii])
                        else:
                            if sss[i] < k : # 虚值合约
                                vol.append(0.2)
                            else:
                                vol.append(0.01)
                elif callOrPut == "认沽":
                    dd=bsm_put_imp_vol_newton(sss[i],k,dofm[i],0.02,price[i],sigma_init,it=100)
                    if dd>0.01 and dd <1:
                        vol.append(dd)
                    else:
                        ii=i-1
                        if vol[ii] < 5.0:
                            vol.append(vol[ii])
                        else:
                            if sss[i] > k : # 虚值合约
                                vol.append(0.2)
                            else:
                                vol.append(0.01)
                        
                        # vol.append(0.01)
                else:
                    print("wrong in calculating vol")
                #vol.append(bsm_call_imp_vol_dichotomy(sss[i],k,dofm[i],0.02,price[i]))
        thsData.insert(7,'vol',vol)
        voll = thsData['vol']
        if callOrPut == "认购":
            cdelta=[]
            for i in range(thsData.shape[0]):
                cdelta.append(c_delta(sss[i],k,dofm[i],0.02,voll[i])*sss[i]*multi)
            thsData.insert(8,'deltacash',cdelta) 
            deltazhi=[]
            for i in range(thsData.shape[0]):
                deltazhi.append(c_delta(sss[i],k,dofm[i],0.02,voll[i]))
            thsData.insert(9,'delta',deltazhi)
        elif callOrPut == "认沽":
            pdelta=[]
            for i in range(thsData.shape[0]):
                pdelta.append(p_delta(sss[i],k,dofm[i],0.02,voll[i])*sss[i]*multi)
            thsData.insert(8,'deltacash',pdelta) 
            deltazhi=[]
            for i in range(thsData.shape[0]):
                deltazhi.append(p_delta(sss[i],k,dofm[i],0.02,voll[i]))
            thsData.insert(9,'delta',deltazhi)  
        else:
            print("wrong in calculating delta")
        thsData.to_csv(name)

    #二分法求波动率
    # def bsm_call_imp_vol_dichotomy(s0,k,t,r,c):
    #     c_est = 0
    #     top = 1  #波动率上限
    #     floor = 0  #波动率下限
    #     sigma = ( floor + top )/2 #波动率初始值
    #     while abs( c - c_est ) > 1e-5:
    #         c_est = bsm_call_value(s0,k,t,r,sigma) 
    #         #根据价格判断波动率是被低估还是高估，并对波动率做修正
    #         if c - c_est > 0: #f(x)>0
    #             floor = sigma
    #             sigma = ( sigma + top )/2
    #         else:
    #             top = sigma
    #             sigma = ( sigma + floor )/2
    #     return sigma 

# '''
optiondata=DataDownload()

df = pd.read_excel('basicInfo.xlsx')
for i in range(len(df)):
    opt_code = str(df.iloc[i]['期权代码'])
    callOrPut = str(df.iloc[i]['认购/认沽'])
    strike = df.iloc[i]['行权价']
    due_date = str(df.iloc[0]['到期日']) 
    units = df.iloc[i]['合约单位']


    # print("'510050.OF','2015-02-09 09:30:00','2021-11-30 15:00:00','%s.SH','2015-02-09 09:30:00','2021-11-30 15:00:00','%s.csv',%d,'%s',%d,%s" %(opt_code,opt_code,strike,due_date,units,callOrPut))
    optiondata.option('510300.OF','2022-02-09 09:30:00','2022-03-10 15:00:00','%s.SH'%(opt_code),'2022-02-09 09:30:00','2022-03-10 15:00:00','%s.csv'%(opt_code),strike,'%s'%(due_date),units,'%s'%(callOrPut))

# thsLogout = THS_iFinDLogout()