import os # operation system package for standard operation system commands
import fnmatch # package for finding specific files
import numpy as np # numeric package for all math operation
from sklearn.mixture import GaussianMixture as GMM # package for GMM
import pickle # loading data object library (like mat in matlab)


origin_path = "C:\\DataSemg" # the main folder of the data
test_path = "C:\\DataSemg\\TEST" # the main folder of the test data

subfolders = ["EX1", "EX2"] # subfolders for each execise

names = ['scapola_good', 'scapola_bad', 'trapz_good', 'trapz_bad']  # names of the recognition

'''
function for prediction
'''
def run_predict():
    results = [] # creating empty array
    for sf in subfolders: # loop over each subfolder
        gmms = []  # creating empty array
        srcDir = os.path.join(origin_path, sf) # concatinate main folder to subfolder
        '''
        loading gmm models
        '''
        for i in range(len(names)):
            with open(os.path.join(srcDir, names[i] + ".pkl"), "rb") as f:
                gmms.append(pickle.load(f))
        res = np.zeros(2) # create array of zeros
        cnt = np.zeros(2) # create array of zeros
        srcDirTest = os.path.join(test_path, sf) # concatinate main folder to subfolder
        for root, dirnames, filenames in os.walk(srcDirTest): # loop over tree folder
            for filename in fnmatch.filter(filenames, "*_feature.npy"): # loop over files in folder
                dataFile = os.path.join(root, filename) # concatinate full path to specific file
                data = np.load(dataFile)  # load the data from the numeric file

                '''
                calculate logLikelihood on scapola gmms
                '''
                if "scapola" in dataFile:
                    likelihood = []
                    for gmm in gmms[:2]:
                        likelihood.append(gmm.score(data))


                    winner = np.argmax(likelihood) # winner is the with the maximum likelihood

                    '''
                    check if the recognition is right
                    '''
                    if names[int(winner)] in dataFile:
                        res[0] += 1
                    cnt[0] += 1

                    '''
                    calculate logLikelihood on scapola gmms
                    '''
                elif "trapz" in dataFile:
                    likelihood = []
                    for gmm in gmms[2:]:
                        likelihood.append(gmm.score(data))

                    winner = np.argmax(likelihood) + 2 # winner is the with the maximum likelihood

                    '''
                    check if the recognition is right
                    '''
                    if names[int(winner)] in dataFile:
                        res[1] += 1
                    cnt[1] += 1

        res[0] = res[0] / float(cnt[0])
        res[1] = res[1] / float(cnt[1])
        print("%s:\n\tscapola -> %.2f%%" % (sf, res[0] * 100.0)) # printing the scapola results
        print("%s:\n\ttrapz -> %.2f%%" % (sf, res[1] * 100.0))  # printing the trapz results

        results.append(res[0])
        results.append(res[1])

    return results


run_predict()

