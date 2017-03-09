from mlearning import mLearning

# Import bid depending on backtesting or forwardtesting, as forwardtesting requires broker communication
class orderCompute(object):
    def __init__(self, object):
        self.bid = 'current bid'
        self.etc = 'etc'
    # Returns list to act on. 0 = short, 1 = long, 2 = opened/inactive   
    def pendingMatrix(bid, last_position, sr_levels): #last_position tells which sr level bid touched last
            pM = [0]*len(sr_levels)
            for i in range(len(sr_levels)):
                if sr_levels[i] == last_position: # 2 assumes order has been placed
                    pM[i] = 2
                elif bid >= sr_levels[i]:
                    pM[i] = 1
                    
    class updatePending(bid_, symbol_, date_, quantile_, n_samples_): #(self) replace
      
        sr_levels = mLearning.importSupportResistance(symbol_, date_, quantile_, n_samples_) #(self) replace
        to_pending = orderCompute.pendingMatrix(bid_, last_position_, sr_levels)
        
    class bidAct(params):
        
        sr_levels = mLearning.importSupportResistance(symbol_, date_, quantile_, n_samples_) #(self) replace
        to_pending = orderCompute.pendingMatrix(bid_, last_position_, sr_levels)
        
        for i in range(len(to_pending)):
            if bid_ == sr_levels[i] and to_pending[i] != 2:
                fromclass.openfunction(to_pending[i])
            