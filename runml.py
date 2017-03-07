from mlearning import mLearning

def main(symbol_, date_, quantile_, n_samples_):
    ml_results = mLearning.importSupportResistance(symbol_, date_, quantile_, n_samples_)
            
    for i in range(len(ml_results)):
        print(ml_results[i])
        
if __name__ == "__main__":
    main("USDJPY", "2017-03-06", 0.2, 2000)
    

        
