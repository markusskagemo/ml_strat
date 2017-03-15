from mlearning import mLearning
import datetime
import calendar
from bisect import bisect_left

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
    
    # Returns value in list closest to input number_. Requires sorted list
    def takeClosest(list_, number_):
        if len(list_) > 0:
            pos = bisect_left(list_, number_)
            if pos == 0:
                return list_[0]
            if pos == len(list_):
                return list_[-1]
            before = list_[pos - 1]
            after = list_[pos]
            if after - number_ < number_ - before:
               return after
            else:
               return before
        else:
            return 0
        
    def getLastDate(date):
        # Thanks to Arnaldo P. Figueira
        def weekDay(year, month, day):
            offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
            afterFeb = 1
            if month > 2: afterFeb = 0
            aux = year - 1700 - afterFeb
            # dayOfWeek for 1700/1/1 = 5, Friday
            dayOfWeek  = 5
            # Partial sum of days betweem current date and 1700/1/1
            dayOfWeek += (aux + afterFeb) * 365                  
            # Leap year correction    
            dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400     
            # Sum monthly and day offsets
            dayOfWeek += offset[month - 1] + (day - 1)               
            dayOfWeek %= 7
            #
            #print(dayOfWeek)
            #
            return int(round(dayOfWeek, 0))
        
        date = str(date).strip("(),'")
        datesplit = date.split('-')
        #if datesplit[2] != '00':
        prior_date = '{}-{}-{}'.format(datesplit[0], datesplit[1], str(int(datesplit[2])-1).zfill(2))

        datesplit = prior_date.split('-')
        if weekDay(int(datesplit[0]), int(datesplit[1]), int(datesplit[2])) == 0:
            prior_date = '{}-{}-{}'.format(datesplit[0], datesplit[1], str(int(datesplit[2])-2).zfill(2))
            datesplit = prior_date.split('-')
        if weekDay(int(datesplit[0]), int(datesplit[1]), int(datesplit[2])) == 6:
            prior_date = '{}-{}-{}'.format(datesplit[0], datesplit[1], str(int(datesplit[2])-1).zfill(2))
            print(prior_date)

        datesplit = prior_date.split('-')
        if datesplit[2] == '00': 
            if datesplit[1] != '1':
                if int(datesplit[1])-1 != 2:
                    if int(datesplit[2]) % 2 == 0:
                        prior_date = '{}-{}-{}'.format(datesplit[0], str(int(datesplit[1])-1).zfill(2), '30')
                    else:
                        prior_date = '{}-{}-{}'.format(datesplit[0], str(int(datesplit[1])-1).zfill(2), '31')
                else:
                    prior_date = '{}-{}-{}'.format(datesplit[0], str(int(datesplit[1])-1).zfill(2), '28')
            else:
                prior_date = '{}-{}-{}'.format(str(int(datesplit[0])-1), '12', '31')
        
        return str(prior_date)
    
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
        # Compute date
        print(self.date)
        prior_date = orderCompute.getLastDate(self.date)
        print(prior_date)
        sr_levels = mLearning.importSupportResistance(self.symbol, prior_date, self.quantile, self.n_samples)

        return sr_levels
    
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