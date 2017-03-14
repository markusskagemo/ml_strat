import os
import csv
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from getdayrates import getDayRates

class mLearning():
    #Exports cluster extremals
    def importSupportResistance(symbol_, date_, quantile_, n_samples_):
        
        # Removes values that are too close. Requires sorted list
        def cleanLevelFloats(ml_results_):
            for j in range(100):
                last_results = ml_results_
                for i in range(1, len(ml_results_)-1):
                    # 0.001 is for symbols with a normal range within <0,10>. Multiply for f.ex. USDJPY
                    if ml_results_[i] - ml_results_[i-1] < 0.001 or ml_results_[i+1] - ml_results_[i-1] < 0.001:
                        ml_results_[i] = 0
                ml_results_ = list(filter(lambda a: a != 0, ml_results_))
                if last_results == ml_results_:
                    break
            return ml_results_
        
        # Import data and convert to matrix for bandwidth
        input_train_ = getDayRates.getDayRates(symbol_, date_)
        rate_data = getDayRates.importRates(input_train_)
        bw_data = rate_data.as_matrix(columns=['bid'])
        
        # Check if S/R file already exists
        underscored_day = "{}_{}_{}".format(date_.split('-')[0], date_.split('-')[1], date_.split('-')[2])
        SRFILE = "ml_results_{}_{}_{}_{}.csv".format(symbol_, underscored_day, quantile_, n_samples_)
        SRDIR = "data/clustering_return/" + SRFILE
        SRDIR_EXT = "C:/Users/" + os.getlogin() +"/Documents/GitHub/ml_strat/" + SRDIR
        
        if os.path.isfile(SRDIR_EXT):
            print("\nS/R-levels already saved at ml_strat/clustering_return/" + SRFILE + "\nImporting...\n")
            with open(SRDIR, 'r') as f:
                reader = csv.reader(f, delimiter=' ')
                ml_results = []
                for row in reader:
                    rowstr = ' '.join(row) # Convert list to string
                    rowsplit = rowstr.split(",")
                    ml_results.append(rowsplit)
                
                ml_results_stripped = str(ml_results[0]).replace("'","").replace("[", "").replace("]", "")
                ml_results_split = ml_results_stripped.split(",")
                ml_results_floated = [float(ml_results_split[elem]) for elem in range(len(ml_results_split))]
                ml_results_sorted = sorted(ml_results_floated)
                
                print("-------------------------\n\tS/R-levels\n-------------------------")
                for i in range(len(ml_results_sorted)):
                    print(ml_results_sorted[i])
                print('\n')
                
                ml_results = cleanLevelFloats(ml_results_sorted)
                
                return ml_results
        else:
            # Calculate bandwidth and fit data
            # Greater quantile greater sample size. estimate_bandwidth for faster MeanShift processing
            bandwidth = estimate_bandwidth(bw_data, quantile=float(quantile_), n_samples=int(n_samples_)) 
            # Bin seeding for increased execution speed but fewer seeds, n_jobs=-2 for all but one active cpu core
            ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, n_jobs=-2)
            ms.fit(rate_data)
            
            # Append maximas of all clusters to S/R array
            ml_results = []
            for k in range(len(np.unique(ms.labels_))):
                members = ms.labels_ == k
                values = bw_data[members, 0]
                ml_results.append(min(values))
                ml_results.append(max(values))
            
            # Remove duplicates and clean floats
            rnd_ml_results = [round(elem, 4) for elem in ml_results]
            rnd_ml_results = list(set(rnd_ml_results))
            #rnd_ml_results = np.array(set(rnd_ml_results))            
            
            # Print levels to shell
            print("-------------------------\n\tS/R-levels\n-------------------------")
            for i in range(len(rnd_ml_results)):
                print(rnd_ml_results[i])
        
            # Export S/R levels to git directory
            with open(SRDIR, 'w') as f:
                wr = csv.writer(f, quoting=csv.QUOTE_NONE)
                wr.writerow(rnd_ml_results)

            print("\nS/R-levels saved at ml_strat/clustering_return/" + SRFILE + "\n")
            return cleanLevelFloats(sorted(rnd_ml_results))
