from mlearning import mLearning

def main(symbol_, date_, quantile_, n_samples_):
    ml_results = mLearning.importSupportResistance(symbol_, date_, quantile_, n_samples_)
    #print(len(ml_results))
    for i in range(len(ml_results)):
        print(ml_results[i])
        
if __name__ == "__main__":
    main("EURUSD", "2017-03-07", 0.1, 5000)
