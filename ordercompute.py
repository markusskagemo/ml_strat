from mlearning import mLearning
import datetime
import calendar

# Import bid depending on backtesting or forwardtesting, as forwardtesting requires broker communication
class orderCompute(object):
    def __init__(self, object):
        #self.bid = object.bid
        self.time = object.time
        #self.date = 
        self.date = object.date
        #self.etc = 'etc'
        #self.lp = object.lp
        #self.ltp = object.ltp
        self.symbol = object.symbol
        self.quantile = object.quantile
        self.n_samples = object.n_samples
    
    #---#
    
    def getLastDate(date):
        date = str(date).strip("(),'")
        datesplit = date.split('-')
        prior_date = '{}-{}-{}'.format(datesplit[0], datesplit[1], str(int(datesplit[2])-1).zfill(2))
        if datesplit[2] == '00': 
            if date.month != 1:
                prior_date = date.replace(day = calendar.monthrange(date.year, int(date.month)-1)[1])
            elif date.month == 1:
                prior_date = date.replace(day = 31, year = int(date.year)-1)
        
        return prior_date
    
    # Returns list to act on. 0 = short, 1 = long, 2 = opened/inactive   
    def pendingMatrix(bid, latest_position, sr_levels): # latest_position tells which sr level bid touched last
            pM = [0]*len(sr_levels)
            print('---------')
            for i in range(len(sr_levels)): # sr_levels)):
                print(sr_levels[i])
                if sr_levels[i] == latest_position: # 2 assumes order has been placed
                    pM[i] = 2
                elif bid >= sr_levels[i]:
                    pM[i] = 1
            return pM
                    
    def newSR(self):
        # Compute date = current date - 1
        print(self.date)
        prior_date = orderCompute.getLastDate(self.date)
        print(prior_date)
        #datesplit = self.date.split('-')
        #prior_date = '{}-{}-{}'.format(datesplit[0], datesplit[1], str(int(datesplit[2])-1).zfill(2))
        #calculated = False
        #if calculated == False: #self.time.hour()*60 + self.time.minute() < 60 and calculated == False:
        sr_levels = mLearning.importSupportResistance(self.symbol, prior_date, self.quantile, self.n_samples)
        #self.calculated = True
        return sr_levels
    '''
        if self.time.hour() == 1:
            self.calculated == False
        return 0
    '''
    #---#
    
    def updatePending(self): #(self) replace
        time = self.time
        bid = self.bid
        latest_position = self.lp
        latest_to_pending = self.ltp
        
        sr_levels = orderCompute.newSR(self)
        if latest_position != latest_to_pending:
            to_pending = orderCompute.pendingMatrix(bid, latest_position, sr_levels)
            latest_to_pending = latest_position = self.lp # Redundant?
        
        #
        print("\n---------")
        for i in range(len(to_pending)):
            print(to_pending[i])
        #
    
    def bidAct(self):
        symbol = self.symbol
        bid = self.bid
        time = self.time
        last_position = self.lp
        latest_to_pending = self.ltp
        
        sr_levels = orderCompute.newSR(self)
        if latest_position != latest_to_pending:
            to_pending = orderCompute.pendingMatrix(bid, latest_position, sr_levels)
            latest_to_pending = latest_position = self.lp # Redundant?
        
        #
        
        #
        for i in range(len(to_pending)):
            if bid_ == sr_levels[i] and to_pending[i] != 2:
                fromclass.openfunction(to_pending[i]) # openfunction incorporates redundancy test
                

'''                
def main(object):
    orderCompute(object).updatePending()


if __name__ == "__main__":
    class to_self():
        pass
    ts = to_self()
    ts.time = datetime.time
    ts.bid = 1.1060
    ts.lp = 1.1083
    ts.ltp = 1.1059
    ts.symbol = 'EURUSD'
    ts.quantile = 0.1
    ts.n_samples = 2000
    
    main(ts)

    # objetct has no attribute etcetcetc error
    
'''        