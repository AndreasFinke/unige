import numpy as np
import matplotlib.pyplot as plt

directory = '/rtMP'
filenames = list_files(directory, "txt")
#filenames = ['rtMP/0.txt', 'rtMP/1.txt', 'rtMP/2.txt','rtMP/3.txt','rtMP/4.txt']
likelihoods = [] #each entry a vector with the time evolution, one per file! 

for filename in filenames:
    fp = open(filename)
    lines = fp.readlines()
    data = [[float(v) for v in line.split()] for line in lines]
    data = np.array(data)
    likelihoods.append(data[:,1])
 

for lh in likelihoods:
    plt.plot(lh)
