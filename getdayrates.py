# -*- coding: utf-8 -*-
import subprocess
import pandas as pd
import os

class getDayRates():
    def getDayRates(symbol_, day_):
        underscored_day = "{}_{}_{}".format(day_.split('-')[0], day_.split('-')[1], day_.split('-')[2])
        RATEFILE = "{}-{}-{}.csv".format(symbol_, underscored_day, underscored_day)
        RATEDIR =  "C:/Users/" + os.getlogin() +"/Documents/GitHub/ml_strat/data/tickdump/" + RATEFILE
        
        if os.path.isfile(RATEDIR):
            return RATEFILE
        else:
            return_code = subprocess.call('duka {} -d {} -f {} --header'
                                    .format(symbol_, day_, 'C:/Users/' + os.getlogin()
                                    +'/Documents/GitHub/ml_strat/data/tickdump/'), shell=True)
        
            if return_code == 0:
                print("\n\nTicks gotten. Saved csv at ~/GitHub/ml_strat/data/tickdump/" + RATEFILE + "\n")
                return RATEFILE
            else:
                print("\nFaulty execution. Check parameters.")
                
    def importRates(input_train_):
        # get bid column
        # throw everything else
        TRAINDIR = "C:/Users/" + os.getlogin() +"/Documents/GitHub/ml_strat/data/tickdump/" + input_train_
        df = pd.read_csv(TRAINDIR,
                         header=0, 
                         usecols=['bid'],
                         names=['datetime', 'bid', 'ask', 'bidvolume', 'askvolume'])
        return df

'''
def main(input_train_):
    gdr = getDayRates()
    gdr.importRates(input_train_)

if __name__ == "__main__":
    main("EURUSD-2017_01_04-2017_01_04.csv")
'''