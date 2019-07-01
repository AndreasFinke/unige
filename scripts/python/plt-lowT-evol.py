import numpy as np
import matplotlib.pyplot as plt
from os import listdir 

directory = '/Users/af/Work/Cosmo/unige/scripts/python/rtMP'

def list_files(directory, extension):
    return (f for f in listdir(directory) if f.endswith('.' + extension))

filenames = list_files(directory, "txt")

#filenames = ['rtMP/0.txt', 'rtMP/1.txt', 'rtMP/2.txt','rtMP/3.txt','rtMP/4.txt']

likelihoods = [] #each entry a vector with the time evolution, one per file! 

for filename in filenames:
    fp = open(directory + "/" + filename)
    lines = fp.readlines()
    data = [[float(v) for v in line.split()] for line in lines]
    data = np.array(data)
    likelihoods.append(data[:,1])
 

for lh in likelihoods:
    plt.plot(lh)

plt.savefig("evol.pdf")
