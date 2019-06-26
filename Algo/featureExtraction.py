import os # operation system package for standard operation system commands
import fnmatch # package for finding specific files
import numpy as np # numeric package for all math operation
import librosa # package for data utils
import matplotlib.pyplot as plt # package for plotting


origin_path = "C:\\DataSemg" # the main folder of the data

subfolders = ["EX1", "EX2"] # subfolders for each execise

def MAV(data): # function for calculate MAV
    mav = np.mean(np.abs(data), axis=1)
    return mav

def RMS(data): # function for calculate RMS
    rms = np.sqrt(np.mean(np.abs(data ** 2), axis=1))
    return rms

def Energy(data): # function for calculate Energy
    energy = np.sum(data ** 2, axis=1)
    return energy

def ZCR(data): # function for calculate ZCR
    zcr = np.zeros(len(data))
    for i in range(len(data)):
        zcr[i] = ((data[i, :-1] * data[i, 1:]) < 0).sum()
    return zcr

def PSD(data): # function for calculate PSD
    psd = np.abs(np.fft.fft(data))[:,:25] ** 2
    return psd

def MPF(data): # function for calculate MPF
    freqs = np.fft.fftfreq(50)[:25]
    mpf = np.zeros(len(data))
    for i in range(len(data)):
        mpf[i] = np.sum(freqs * data[i]) / np.sum(data[i])
    return mpf

def MDF(data): # function for calculate MDF
    mdf = 0.5 * np.sum(data, axis=1)
    return mdf

for sf in subfolders: # loop over each subfolder
    srcDir = os.path.join(origin_path, sf) # concatinate main folder to subfolder
    for root, dirnames, filenames in os.walk(srcDir): # loop over tree folder
        for filename in fnmatch.filter(filenames, "*.npy"): # loop over files in folder
            dataFile = os.path.join(root, filename) # concatinate full path to specific file
            featureFile = dataFile[:-4] + "_feature.npy" # replacing the filename
            figureFile = featureFile.replace('npy', 'png') # replacing the extension
            data = np.load(dataFile) # load the data from the numeric file
            data_framed = librosa.util.frame(data, 50, 25).T # block fraiming
            mav = MAV(data_framed) # calculate MAV
            rms = RMS(data_framed) # calculate RMS
            energy = Energy(data_framed) # calculate Energy
            zcr = ZCR(data_framed) # calculate ZCR
            psd = PSD(data_framed) # calculate PSD
            mpf = MPF(psd) # calculate MPF
            mdf = MDF(psd) # calculate MDF
            mav = np.expand_dims(mav, 1) # expanding dimension
            rms = np.expand_dims(rms, 1) # expanding dimension
            energy = np.expand_dims(energy, 1) # expanding dimension
            zcr = np.expand_dims(zcr, 1) # expanding dimension
            mpf = np.expand_dims(mpf, 1) # expanding dimension
            mdf = np.expand_dims(mdf, 1) # expanding dimension
            feature = np.concatenate((mav, rms, energy, zcr, mpf, mdf), axis=1) # concatinate all features to one matrix
            np.save(featureFile, feature, allow_pickle=False) # saving the features matrix to numeric file
            '''
            PLOTING TO PNG FILE
            '''
            plt.figure()
            plt.subplot(7, 1, 1)
            plt.plot(data)
            plt.title('signal')
            plt.grid()
            plt.subplot(7, 1, 2)
            plt.plot(mav[:,0])
            plt.title('mav')
            plt.grid()
            plt.subplot(7, 1, 3)
            plt.plot(rms[:,0])
            plt.title('rms')
            plt.grid()
            plt.subplot(7, 1, 4)
            plt.plot(energy[:,0])
            plt.title('energy')
            plt.grid()
            plt.subplot(7, 1, 5)
            plt.plot(zcr[:,0])
            plt.title('zcr')
            plt.grid()
            plt.subplot(7, 1, 6)
            plt.plot(mpf[:,0])
            plt.title('mpf')
            plt.grid()
            plt.subplot(7, 1, 7)
            plt.plot(mdf[:,0])
            plt.title('mdf')
            plt.grid()
            plt.savefig(figureFile)
