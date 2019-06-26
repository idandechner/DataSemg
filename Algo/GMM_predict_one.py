import os # operation system package for standard operation system commands
import fnmatch # package for finding specific files
import numpy as np # numeric package for all math operation
import pickle # loading data object library (like mat in matlab)
import sys


input_file = sys.argv[1]

ex = input('Which EX to check?\n1. EX1\n2. EX2')
tar = input('Scalopa or Trapz?\n1. Scalopa\n2. Trapz')
ex = int(ex)
tar = int(tar)
models = []
folder = None
main_folder = "C:\\DataSemg"
action = ''
if ex != 1 and ex != 2:
    print("error value for EX")
    exit(1)

if tar != 1 and tar != 2:
    print("error value for action")
    exit(1)

if ex == 1:
    folder = 'EX1'
else:
    folder = 'EX2'

if tar == 1:
    model1 = os.path.join(main_folder, folder, 'scapola_good.pkl')
    model2 = os.path.join(main_folder, folder, 'scapola_bad.pkl')
    with open(model1, "rb") as f:
        models.append(pickle.load(f))
    with open(model2, "rb") as f:
        models.append(pickle.load(f))
    action = 'scapola'

else:
    model1 = os.path.join(main_folder, folder, 'trapz_good.pkl')
    model2 = os.path.join(main_folder, folder, 'trapz_bad.pkl')
    with open(model1, "rb") as f:
        models.append(pickle.load(f))
    with open(model2, "rb") as f:
        models.append(pickle.load(f))
    action = 'trapz'

print("execise = %s, action = %s" % (folder, action))
data = np.load(input_file)

likelihood = []
for gmm in models:
    likelihood.append(gmm.score(data))

winner = np.argmax(likelihood) # winner is the with the maximum likelihood

if winner == 0:
    print("%s recognized as good with likelihood of %f" % (action, likelihood[int(winner)]))
else:
    print("%s recognized as bad with likelihood of %f" % (action, likelihood[int(winner)]))