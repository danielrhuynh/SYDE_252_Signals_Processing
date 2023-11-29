# Get filteredSample and envelopes from bancpass_filter.py
from bandpass_filter import filterBank, edges, filteredSample, envelopes, recFilteredSample, fs
import numpy as np
import matplotlib.pyplot as plt
import math

res = []
# Task 10
for i in range(len(filterBank)):
    centralFreq = math.sqrt(edges[i]*edges[i+1])
    
    t = np.arange(len(recFilteredSample[i]))/fs
    cosSignal = np.cos(2*math.pi*centralFreq*t)
    
    # Task 11
    modulatedSignal = cosSignal * recFilteredSample[i]
    res.append(modulatedSignal)

compositeSignal = np.sum(res, axis=0)

compositeSignal /= np.max(np.abs(compositeSignal))

plt.plot(compositeSignal)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Composite Signal')
plt.show()






    


