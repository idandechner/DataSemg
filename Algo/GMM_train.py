import os # operation system package for standard operation system commands
import fnmatch # package for finding specific files
import numpy as np # numeric package for all math operation
from sklearn.mixture import GaussianMixture as GMM # package for GMM
import pickle # saving data object library (like mat in matlab)

origin_path = "C:\\DataSemg" # the main folder of the data

subfolders = ["EX1", "EX2"] # subfolders for each execise

names = ['scapola_good', 'scapola_bad', 'trapz_good', 'trapz_bad'] # names of the recognition
for sf in subfolders: # loop over each subfolder
    data = [] # create empty array
    data_scapola_good = [] # create empty array
    data_scapola_bad = [] # create empty array
    data_trapz_good = [] # create empty array
    data_trapz_bad = [] # create empty array

    srcDir = os.path.join(origin_path, sf) # concatinate main folder to subfolder
    for root, dirnames, filenames in os.walk(srcDir): # loop over tree folder
        for filename in fnmatch.filter(filenames, "*_feature.npy"): # loop over files in folder
            dataFile = os.path.join(root, filename) # concatinate full path to specific file
            if "scapola" in root: # check if scapola in path
                if "good" in root: # check if good in scapola path
                    '''
                    Appending data for scapola_good
                    '''
                    if len(data_scapola_good) == 0:
                        data_scapola_good = np.load(dataFile)
                    else:
                        data_scapola_good = np.concatenate((data_scapola_good, np.load(dataFile)), axis=0)

                elif "bad" in root: # check if bad in scapola path
                    '''
                    Appending data for scapola_bad
                    '''
                    if len(data_scapola_bad) == 0:
                        data_scapola_bad = np.load(dataFile)
                    else:
                        data_scapola_bad = np.concatenate((data_scapola_bad, np.load(dataFile)), axis=0)
            elif "trapz" in root: # check if trapz in path
                if "good" in root: # check if good in trapz path
                    '''
                    Appending data for trapz_good
                    '''
                    if len(data_trapz_good) == 0:
                        data_trapz_good = np.load(dataFile)
                    else:
                        data_trapz_good = np.concatenate((data_trapz_good, np.load(dataFile)), axis=0)
                elif "bad" in root: # check if bad in trapz path
                    '''
                    Appending data for trapz_bad
                    '''
                    if len(data_trapz_bad) == 0:
                        data_trapz_bad = np.load(dataFile)
                    else:
                        data_trapz_bad = np.concatenate((data_trapz_bad, np.load(dataFile)), axis=0)
    '''
    Appending all data
    '''
    data.append(data_scapola_good)
    data.append(data_scapola_bad)
    data.append(data_trapz_good)
    data.append(data_trapz_bad)

    '''
    Creating GMM objects
    '''
    gmms = [GMM(n_components=64, covariance_type='diag', max_iter=1000, verbose=1),
        GMM(n_components=64, covariance_type='diag', max_iter=1000, verbose=1),
        GMM(n_components=64, covariance_type='diag', max_iter=1000, verbose=1),
        GMM(n_components=64, covariance_type='diag', max_iter=1000, verbose=1)]

    '''
    Training all GMMs and save the models into object file (like mat in matlab)
    '''
    for index, gmm in enumerate(gmms):
        gmm.fit(data[index])
        with open(os.path.join(srcDir, names[index] + ".pkl"), "wb") as f:
            pickle.dump(gmm, f)

