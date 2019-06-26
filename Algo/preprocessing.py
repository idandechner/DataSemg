import os # operation system package for standard operation system commands
from scipy.io import loadmat # library for loading mat files
import numpy as np # numeric package for all math operation
import fnmatch # package for finding specific files

origin_path = "C:\\DataSemg" # the main folder of the data

subfolders = ["EX1", "EX2"] # subfolders for each execise


for sf in subfolders: # loop over each subfolder
    srcDir = os.path.join(origin_path, sf) # concatinate main folder to subfolder
    for root, dirnames, filenames in os.walk(srcDir): # loop over tree folder
        for filename in fnmatch.filter(filenames, "*.mat"): # loop over files in folder
            matFile = os.path.join(root, filename) # concatinate full path to specific file
            out = matFile.replace('mat', 'npy') # replacing the extension
            data = loadmat(matFile)['x'][0] # load data from mat file
            data = data / 1024 # normalize the data to be between -1 to 1
            data = data - np.mean(data) # mean substaction
            np.save(out, data) # save the data to numeric file
