from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from ordercompute import orderCompute

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt
import pyfolio as pf
%matplotlib inline

class SRStrategy(bt.Strategy):
    
    params = (
        ('target_q', 10),
        ('stop_q', 6),
    )
    
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s %s, %s' % (dt.isoformat(), self.msP.time, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        
        self.fromdate = datetime.datetime(2016, 3, 2) #
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.isImported = False #
        self.x = -1 #
        self.longtarget = 100 #
        self.longstop = 100 #
        self.shorttarget = 100 #
        self.shortstop = 100 #
        self.levelhistory = [0]*4 #
        self.opendate = self.data.datetime.date() #
        self.ordertype = None #
        
        class mshiftParams(): # > Pass msP as function instead?
            pass
        self.msP = mshiftParams() #
        self.msP.time = self.data.datetime.time(0).isoformat()
        self.msP.date = str(self.fromdate).split(' ')[0]
        self.msP.symbol = 'EURUSD'
        self.msP.quantile = 0.15
        self.msP.n_samples = 500

        self.srlevels = orderCompute(self.msP).newSR() #

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            '''
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
            '''
            self.bar_executed = len(self)

        # Write down: no pending order
        self.order = None
        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f\n' %
                 (trade.pnl, trade.pnlcomm))
    def next(self):
        self.msP.time = self.data.datetime.time().isoformat()
        self.msP.date = self.data.datetime.date().isoformat()
        
        # Recalibrate S/R at midnight
        if datetime.time(0, 1) < self.data.datetime.time() < datetime.time(0, 10) and self.isImported == False:
            self.srlevels = orderCompute(self.msP).newSR()
            # > Append to master array with range of entire testing period
            self.isImported = True
        if self.data.datetime.time() == datetime.time(0, 11):
            self.isImported = False
            
        # Log the closing price of the series from the reference
        #self.log('Close, %f.4' % self.dataclose[0])

        # Check if an order is pending
        if self.order:
            return
        
        #closelevel = min(srlevels, key=lambda x:abs(x-self.dataclose[0]))
        closestlevel = orderCompute.takeClosest(self.srlevels, self.dataclose[0])
        
        # Get last relevant level touch point
        # > For live, try to get open data or OHLC to reduce requests
        if ((self.datalow[0] <= closestlevel <= self.dataclose[0] or 
            self.datahigh[0] >= closestlevel >= self.dataclose[0]) and 
            self.levelhistory[0] != closestlevel):
            # remove last
            self.levelhistory.pop(3)
            # append first
            self.levelhistory.insert(0, closestlevel)
        
        # Check if we are in the market
        if (not self.position and len(self.srlevels) > 2 
            and self.dataclose[-1] != self.dataclose[0]): #or self.opendate != self.data.datetime.date():
            if (self.data.datetime.time() > datetime.time(0, 2)
                and self.ordertype == None 
                and min(self.srlevels) <= self.dataclose[0] <= max(self.srlevels)):
                
                if closestlevel != max(self.srlevels): # > redundant
                    # > Get OHLC, in this case L
                    if self.levelhistory[1] > self.levelhistory[0] and self.dataclose[0] <= self.levelhistory[0]:
                        self.longtarget = (self.dataclose[0] + 
                                         (self.srlevels[self.srlevels.index(closestlevel)+1] - self.dataclose[0])*float(self.p.target_q)/10.0)
                        self.longstop = (self.dataclose[0] - (self.srlevels[self.srlevels.index(closestlevel)+1] - 
                                                              self.dataclose[0])*float(self.p.stop_q))
                        self.opendate = self.data.datetime.date()
                        self.order = self.buy()
                        self.log('LONG CREATE, P:%.4f, T:%.4f, SL:%.4f' % (self.dataclose[0], self.longtarget, self.longstop))
                        self.ordertype = 'Long'

                if closestlevel != min(self.srlevels): # > redundant
                    if self.levelhistory[1] < self.levelhistory[0] and self.dataclose[0] >= self.levelhistory[0]:
                        self.shorttarget = (self.dataclose[0] - (self.dataclose[0] - 
                                                                self.srlevels[self.srlevels.index(closestlevel)-1])*float(self.p.target_q)/10.0)
                        self.shortstop = self.dataclose[0] + (self.dataclose[0] - self.shorttarget)*float(self.p.stop_q)/10.0
                        self.opendate = self.data.datetime.date()
                        self.order = self.sell()
                        self.log('SHORT CREATE, P:%.4f, T:%.4f, SL:%.4f' % (self.dataclose[0], self.shorttarget, self.shortstop))
                        self.ordertype = 'Short'
                
        else:
            # > Close 'types' of orders, not every order over/under a threshold.
            # > Ex. only one self.ordertype active /zone, but multiple orders of different direction open simultaniously.
            if self.ordertype == 'Long': # and not order.isbuy():
                if self.dataclose[0] >= self.longtarget or self.dataclose[0] <= self.longstop: #or 
                    self.log('LONG POSITION CLOSE, %.4f' % self.dataclose[0])
                    self.order = self.close()
                    self.ordertype = None
            elif self.ordertype == 'Short': #and not self.order.issell():
                if self.dataclose[0] <= self.shorttarget or self.dataclose[0] >= self.shortstop:
                    self.log('SHORT POSITION CLOSE, %.4f' % self.dataclose[0])
                    self.order = self.close()
                    self.ordertype = None
        # Calibrates SL and TP according to new SR-levels if trade was opened another day
        if self.opendate < self.data.datetime.date():
            if self.ordertype == 'Long':
                if closestlevel < self.dataclose[0]:
                    # Avoid index surpassing
                    if closestlevel != max(self.srlevels):
                        self.longtarget = (self.dataclose[0] + 
                                          (self.srlevels[self.srlevels.index(closestlevel)+1] - self.dataclose[0])*float(self.p.target_q)/10.0)
                    self.longstop = closestlevel
                else:
                    self.longtarget = closestlevel
                    # Avoid index surpassing
                    if closestlevel != min(self.srlevels):
                        self.longstop = self.srlevels[self.srlevels.index(closestlevel)-1]
                    else:
                        self.longstop = 2*closestlevel - self.srlevels[self.srlevels.index(closestlevel)+1]
                        
            elif self.ordertype == 'Short':
                if closestlevel > self.dataclose[0]:
                    if closestlevel != min(self.srlevels):
                        self.shorttarget = (self.dataclose[0] - 
                                           (self.dataclose[0] - self.srlevels[self.srlevels.index(closestlevel)-1])*float(self.p.target_q)/10.0)
                    self.shortstop = closestlevel
                else:
                    self.shorttarget = closestlevel
                    if closestlevel != max(self.srlevels):
                        self.shortstop = self.srlevels[self.srlevels.index(closestlevel)+1]
                    else:
                        self.shortstop = 2*closestlevel + self.srlevels[self.srlevels.index(closestlevel)-1]
    '''
    def stop(self):
        self.log('Ending Value %.2f' %
                 self.broker.getvalue(), doprint=True)
    '''   
    
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(SRStrategy)
    '''
    cerebro.optstrategy(
        SRStrategy,
        target_q=range(5, 12),
        stop_q=range(2, 7),
    )
    '''

    #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')
    datapath = 'data/tickdump/EURUSD_20160301-20170301.csv' #YHOO1617.csv'
    
    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2016, 3, 2),
        todate=datetime.datetime(2016, 3, 20),
        timeframe=bt.TimeFrame.Minutes,
        dtformat='%d.%m.%Y %H:%M:%S.000')

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.4f' % cerebro.broker.getvalue())
    
    cerebro.addsizer(bt.sizers.FixedSize, stake=90000)
    cerebro.broker.setcommission(commission=0.0)
    cerebro.addanalyzer(bt.analyzers.PyFolio)
    
    # Run over everything
    results = cerebro.run()
    #cerebro.plot()
    
    # Print out the final result
    print('Final Portfolio Value: %.4f' % cerebro.broker.getvalue())
    strat = results[0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    
    pf.create_full_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    #gross_lev=1000,#gross_lev,
    live_start_date='2016-03-17',  # This date is sample specific
    round_trips=True)
