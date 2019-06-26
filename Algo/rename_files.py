import os
import sys
import fnmatch

test_path = "C:\\DataSemg\\TEST"


for root, dirnames, filenames in os.walk(test_path):
    for filename in fnmatch.filter(filenames, "*scalopa*"):
        inFile = os.path.join(root, filename)
        outFile = inFile.replace('scalopa', 'scapola')
        os.rename(inFile, outFile)


