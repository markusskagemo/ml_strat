import sys
import numpy as np
import pandas as pd
import json
from sklearn.cluster import MeanShift, estimate_bandwidth

def main(train_):
    dataFrame = pd.read_csv(train_, parse_dates=[0], index_col=0, names=['Date_Time', 'Buy', 'Sell'], date_parser=lambda x: pd.to_datetime(x, format="%d/%m/%y %H:%M:%S"))
    
    grouped_data = dataFrame.dropna()
    ticks_data = grouped_data['Sell'].resample('24H').ohlc()
    sell_data = grouped_data.as_matrix(columns=['Sell'])
    
    bandwidth = estimate_bandwith(sell_data, quantile=0.1, n_samples=100)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit()
    
    ml_results = []
    for k in range(len(np.unique(ms.labels_))):
        members = ms.labels_ == k
        values = sell_data[members, 0]
        
        ml_results.append(min(values))
        ml_results.append(max(values))
    
    ticks_data.to_json('ticks.json', date_format='iso', orient='index')
    
    # export ml support resisistance
    with open('ml_results.json', 'w') as f:
        f.write(json.dumps(ml_results))

    print "Done. Goto 0.0.0.0:8000/chart.html"

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print 'mshift.py <inputfile.csv>'
        sys.exit(2)
    main(sys.argv[1])