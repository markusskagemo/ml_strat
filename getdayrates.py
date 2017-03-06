# -*- coding: utf-8 -*-
import subprocess
import pandas as pd
import os

class getDayRates(): # object?
    def __init__(self, symbol, day):
        self.symbol = symbol
        self.day = day
        
    def getDayRates(self):
            return_code = subprocess.call('duka {} -d {} -f {}'
                                    .format(self.symbol, self.day, 'C:/Users/' + os.getlogin()
                                    +'/Documents/GitHub/ml_strat/data/tickdump/'), shell=True)
            
            if return_code == 0:
                print("Success! Saved csv at ~/GitHub/ml_strat/data/tickdump/ \n")
            else:
                print("Faulty execution. Check parameters.")
                
    def importRates(self):
        pass #remove <-
        #df = pd.read_csv(params)
        # get bid column
        # throw everything else
        # return list for bandwidth/meanshift