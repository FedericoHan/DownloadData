#like with BLPAPI, download the TIA package from GitHub and paste in the directory_
#C:\Users\cp85vc\AppData\Local\Continuum\Anaconda3\Lib\site-packages\tia
#There was a NameError when calling 'resp', 'basestring' not defined
#from C:\Users\cp85vc\AppData\Local\Continuum\Anaconda3\lib\site-packages\tia\bbg\v3api.py 
#so had to change all 'basestring' to 'str', close-re-open and then it worked :)
#examples :  http://nbviewer.jupyter.org/github/bpsmith/tia/blob/master/examples/v3api.ipynb

#version2: just removed the +str(Curncy) from bloomberg 
#version3: replaced deprecated datetools on intraday , using datetime.timedelta instead 

import blpapi
import tia.bbg.datamgr as dm
from tia.bbg import LocalTerminal

import numpy as np
import pandas as pd

#import tai  #basic tech analysis module
#this is more advanced module  but need to install whole talib._ta_lib  -->import talib
#import datetime
import datetime as dt#  --->NameError: name 'datetime' is not defined

'''just use 'pip install quandl' on c window to avoid 2 steps below, works like wonders, else:
had to install more_itertools module
had to install inflectionl.py '''

import quandl 
quandl.ApiConfig.api_key = 'eZ2QKTMzUvQ8z5R3s2bw'#'use the key you receive when you register on website'

'''you may have to go website, login, and reply to confo mail to call api.
registerd using fhan18@.....edu'''

class DownloadData(object):
    '''Use to download timeseries from either blp or quandl'''
    #can pass single 'PX_LAST', or list ['PX_LAST', 'PX_HIGH']
    def __init__(self, pair, fields, startDate, endDate, period, source):
        
        self.pair = pair #'EURUSD Curcny' or 'BOE/XUDLADD' in quandL..other pairs at https://blog.quandl.com/api-for-currency-data
        self.fields = fields  #dt.datetime(2000, 12, 1)
        self.startDate = startDate #dt.datetime.today() 
        self.endDate = endDate #datetime.date(2018, 1,14)=
        print(endDate)
        self.period = period #'DAILY', 'MONTHLY', 'YEARLY'
        self.source = source #blp or quandl
        
    def get_data_blp_historical(self, level_values):
        '''imports historical data from bbg api, converts to dataframe 
           level_values: df MultiIndex(levels=[['EURUSD Curncy'], ['PX_OPEN', 'PX_LAST', 'PX_LOW', 'PX_HIGH']], thus
           if set = 0, column header is 'EURUSD Curncy', if set = 1, column header is 'PX_LAST '''
        formattedPair = self.pair #+str(' Curncy')##removed this as what if you want a Comdty or Index?
        resp = LocalTerminal.get_historical(formattedPair, self.fields, self.startDate, self.endDate,  self.period)
        df = resp.as_frame()
        
        df.columns = df.columns.get_level_values(level_values) 
        
        return df
    
    def get_data_blp_intraday(self, daylag, minutes):
        '''imports intraday data from bbg api, converts to dataframe '''
        formattedPair = self.pair# +str(' Curncy')##removed this as what if you want a Comdty or Index?

        event = 'TRADE'
        #starting point, if BDay(-10), starts 10days ago for instance
        #datetools deprecated  delta = pd.datetools.BDay(-daylag).apply(self.endDate)
        now = dt.datetime.now()
        start = now + dt.timedelta(days = daylag)
        #endDay = datetime.date(2017,12,3)
        #end = pd.datetime.combine(endDay, datetime.time(23, 30))
        end = self.endDate
        #print(end)

        intraDayDf = LocalTerminal.get_intraday_bar(formattedPair, event, start, end, interval= minutes).as_frame()

        #f.set_index('time')  wrong
        intraDayDf = intraDayDf.set_index('time')
        return intraDayDf
    
    def blp_data_get_returns(self):
        
        df = self.get_data_blp_historical()
        df['return']= (df['PX_LAST']/(df['PX_LAST'].shift(1)) -1.0)*100
        return df
    
        
    def get_data_quandl_historical(self):
        
        #df = quandl.get(pair = self.pair)#, start_date = self.startDate, end_date = self.endDate)
        df = quandl.get(self.pair)
        #rename column from 'Value' to 'PX_LAST' for coherence
        df.columns = ['PX_LAST']
        return df
     
'''  
start = dt.datetime(2021,12,19)
end = dt.datetime.today()

test = DownloadData(['AUDUSD Curncy', 'EURUSD Curncy'], 'PX_LAST', start, end, 'DAILY', 'blp')
a0 = test.get_data_blp_historical(0)
print(a0.columns)
a1 = test.get_data_blp_historical(1)
print(a1.columns)
#b  = test.get_data_blp_intraday(-10, 60)'''

    