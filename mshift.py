import sys
import os
import csv
import numpy as np
import pandas as pd
#import json
from sklearn.cluster import MeanShift, estimate_bandwidth

def main(input_train_, quantile_, n_samples_):
    #dataFrame = pd.read_csv(train_, parse_dates=[0], index_col=0, names=['Date_Time', 'Rate'], date_parser=lambda x: pd.to_datetime(x, format="%Y.%m.%d %H:%M:%S")) 
    # Import data
    train_ = "C:\\Users\\" + os.getlogin() +"\\Documents\\GitHub\\ml_strat\\data\\tickdump\\" + input_train_    
    dataFrame = pd.read_csv(train_, names=['Rate'])
    grouped_data = dataFrame.dropna()
    ticks_data = grouped_data
    sell_data = grouped_data.as_matrix(columns=['Rate'])
    
    # Calculate bandwidth and fit data
    bandwidth = estimate_bandwidth(sell_data, quantile=float(quantile_), n_samples=int(n_samples_)) # Greater quantile greater sample size. estimate_bandwidth for faster MeanShift processing
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, n_jobs=-2) # Bin seeding for increased processing speed but fewer seeds, n_jobs=-2 for all but one active cpu core
    ms.fit(ticks_data)
    
    # Append maximas of all clusters to S/R array
    ml_results = []
    for k in range(len(np.unique(ms.labels_))):
        members = ms.labels_ == k
        values = sell_data[members, 0]
        #print(values)
        ml_results.append(min(values))
        ml_results.append(max(values))
    
    # Remove duplicates and clean floats
    rnd_ml_results = [round(elem, 4) for elem in ml_results]
    rnd_ml_results = list(set(rnd_ml_results))

    # Export S/R levels to git directory
    with open('data/clustering_return/ml_results_' + input_train_, 'w') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(rnd_ml_results)

    print("ml_strat/clustering_return/<return_file.csv>")

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print('python mshift.py <inputfile.csv>, <quantile>, <n_samples>')
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], sys.argv[3])