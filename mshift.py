import sys
import csv
import numpy as np
import pandas as pd
import json
from sklearn.cluster import MeanShift, estimate_bandwidth

def main(train_):
    dataFrame = pd.read_csv(train_, parse_dates=[0], index_col=0, names=['Date_Time', 'Rate'], date_parser=lambda x: pd.to_datetime(x, format="%Y.%m.%d %H:%M:%S")) 
    
    grouped_data = dataFrame.dropna()
    #ticks_data = grouped_data['Rate'].resample('M30').ohlc()
    ticks_data = grouped_data
    sell_data = grouped_data.as_matrix(columns=['Rate'])
    
    bandwidth = estimate_bandwidth(sell_data, quantile=0.1, n_samples=200) # Greater quantile greater sample size. estimate_bandwidth for faster MeanShift processing
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, n_jobs=-2) # Bin seeding for increased processing speed but fewer seeds, n_jobs=-2 for all but one active cpu core
    ms.fit(ticks_data)
    
    ml_results = []
    for k in range(len(np.unique(ms.labels_))):
        members = ms.labels_ == k
        values = sell_data[members, 0]
        #print(values)
        ml_results.append(min(values))
        ml_results.append(max(values))
    
    rnd_ml_results = [round(elem, 4) for elem in ml_results]
    rnd_ml_results = list(set(rnd_ml_results))
    
    
    #ticks_data.reset_index().to_csv('ticks.csv', date_format='iso', orient='index') # export ml support resisistance
    with open('clustering_return/ml_results.csv', 'w') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(rnd_ml_results)
        
        #f.write(json.dumps(rnd_ml_results))
        #ml_results.to_csv(path_or_buf='ml_results.csv')

    print("cmd python -m http.server | at 0.0.0.0:8000/chart.html")

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print('mshift.py <inputfile.csv>')
        sys.exit(2)
    #main("data/tickdump/2017.03.02.csv" '''sys.argv[1]''')
    main("C:\\Users\\Markus\\Documents\\GitHub\\ml_strat\\data\\tickdump\\" + sys.argv[1])