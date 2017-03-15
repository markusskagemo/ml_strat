from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from ordercompute import orderCompute

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt

class SRStrategy(bt.Strategy):
    '''
    params = (
        (''),
    )
    '''
    
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s %s, %s' % (dt.isoformat(), self.msP.time, txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        
        self.fromdate = datetime.datetime(2016, 3, 2)
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.isImported = False
        self.x = -1
        self.target = 100
        self.stop = 100
        self.levelhistory = [0]*3
        self.opendate = self.data.datetime.date()
        self.ordertype = None
        
        class mshiftParams(): # > Pass msP as function instead?
            pass
        self.msP = mshiftParams()
        self.msP.time = self.data.datetime.time(0).isoformat()
        self.msP.date = str(self.fromdate).split(' ')[0]
        self.msP.symbol = 'EURUSD'
        self.msP.quantile = 0.15
        self.msP.n_samples = 500

        self.srlevels = orderCompute(self.msP).newSR()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        '''
        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.4f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.4f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
        
            self.bar_executed = len(self)
        '''
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
        if ((self.dataclose[-1] <= closestlevel <= self.dataclose[0] or 
            self.dataclose[-1] >= closestlevel >= self.dataclose[0]) and 
            self.levelhistory[0] != closestlevel):
            # remove last
            self.levelhistory.pop(2)
            # append first
            self.levelhistory.insert(0, closestlevel)
        
        # Check if we are in the market
        if not self.position or self.opendate != self.data.datetime.date():
            if self.data.datetime.time() > datetime.time(0, 10):
                if closestlevel != max(self.srlevels):
                    # > Get OHLC, in this case L
                    if self.levelhistory[1] >= self.levelhistory[0] and self.dataclose[0] <= self.levelhistory[0]:
                        self.log('BUY CREATE, %.4f' % self.dataclose[0])
                        self.target = self.srlevels[self.srlevels.index(closestlevel)+1]
                        self.stop = self.dataclose[0] - (self.target - self.dataclose[0])
                        self.opendate = self.data.datetime.date()
                        self.order = self.buy()
                        self.ordertype = 'Buy'
                elif closestlevel != min(self.srlevels):
                    if self.levelhistory[1] <= self.levelhistory[0] and self.dataclose[0] >= self.levelhistory[0]:
                        self.log('SELL CREATE, %.4f' % self.dataclose[0])
                        self.target = self.srlevels[self.srlevels.index(closestlevel)-1]
                        self.stop = self.dataclose[0] + (self.dataclose[0] - self.target)
                        self.opendate = self.data.datetime.date()
                        self.order = self.sell()
                        self.ordertype = 'Sell'
        else:
            # > Close 'types' of orders, not every order over/under a threshold.
            # > Ex. only one self.ordertype active /zone, but multiple orders of different direction open simultaniously.
            if self.ordertype == 'Buy':
                if self.dataclose[0] >= self.target or self.dataclose[0] <= self.stop: #or 
                    self.log('POSITION CLOSE, %.4f' % self.dataclose[0])
                    self.order = self.close()
            elif self.ordertype == 'Sell':
                if self.dataclose[0] <= self.target or self.dataclose[0] >= self.stop:
                    self.log('POSITION CLOSE, %.4f' % self.dataclose[0])
                    self.order = self.close()
                    
if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(SRStrategy)
    #strats = cerebro.optstrategy(SRStrategy)

    #modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')
    datapath = 'data/tickdump/EURUSD_20160301-20170301.csv' #YHOO1617.csv'
    
    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2016, 3, 2),
        todate=datetime.datetime(2016, 12, 31),
        timeframe=bt.TimeFrame.Minutes,
        dtformat='%d.%m.%Y %H:%M:%S.000')

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    print('Starting Portfolio Value: %.4f' % cerebro.broker.getvalue())
    
    cerebro.addsizer(bt.sizers.FixedSize, stake=10000)
    cerebro.broker.setcommission(commission=0.001)
    
    # Run over everything
    cerebro.run()
    cerebro.plot()

    # Print out the final result
    print('Final Portfolio Value: %.4f' % cerebro.broker.getvalue())