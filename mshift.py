import sys
#import os
import csv
import numpy as np
#import pandas as pd
from sklearn.cluster import MeanShift, estimate_bandwidth
from getdayrates import getDayRates


def main(symbol_, date_, quantile_, n_samples_):
    # Import data and convert to matrix for bandwidth
    input_train_ = getDayRates.getDayRates(symbol_, date_)
    rate_data = getDayRates.importRates(input_train_)
    bw_data = rate_data.as_matrix(columns=['bid'])
    
    # Calculate bandwidth and fit data
    bandwidth = estimate_bandwidth(bw_data, quantile=float(quantile_), n_samples=int(n_samples_)) # Greater quantile greater sample size. estimate_bandwidth for faster MeanShift processing
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, n_jobs=-2) # Bin seeding for increased processing speed but fewer seeds, n_jobs=-2 for all but one active cpu core
    ms.fit(rate_data)
    
    # Append maximas of all clusters to S/R array
    ml_results = []
    for k in range(len(np.unique(ms.labels_))):
        members = ms.labels_ == k
        values = bw_data[members, 0]
        #print(values)
        ml_results.append(min(values))
        ml_results.append(max(values))
    
    # Remove duplicates and clean floats
    rnd_ml_results = [round(elem, 4) for elem in ml_results]
    rnd_ml_results = list(set(rnd_ml_results))
    
    # Print levels to shell
    print("-------------------------\n S/R-levels\n-------------------------")
    for i in range(len(rnd_ml_results)):
        print(rnd_ml_results[i])
    #

    # Export S/R levels to git directory
    with open('data/clustering_return/ml_results_' + input_train_, 'w') as f:
        wr = csv.writer(f, quoting=csv.QUOTE_ALL)
        wr.writerow(rnd_ml_results)
        
    underscored_day = "{}_{}_{}".format(date_.split('-')[0], date_.split('-')[1], date_.split('-')[2])
    save_to = symbol_ + "_" + underscored_day + "-" + underscored_day + ".csv"
    print("\nml_strat/clustering_return/" + "ml_results_" + save_to + "\n")

if __name__ == "__main__":
    if (len(sys.argv) < 3): #is not 3):
        print('python mshift.py <YYYY-MM-DD>, <quantile>, <n_samples>')
        sys.exit(2)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])