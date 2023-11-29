# Get filteredSample and envelopes from bancpass_filter.py
from bandpass_filter import filterBank, edges, sampleFreq, envelopes, recFilteredSample
import numpy as np
import matplotlib.pyplot as plt
import math
import sounddevice as sd
import math

# Task 10
res = []
for i in range(len(filterBank)):
    centralFreq = math.sqrt(edges[i]*edges[i+1])
    
    t = np.arange(len(envelopes[i]))/sampleFreq
    cosSignal = np.cos(2*math.pi*centralFreq*t)

    envelope = np.squeeze(envelopes[i])
    
    # Task 11
    modulatedSignal = cosSignal * envelope
    res.append(modulatedSignal)

# Task 12
compositeSignal = np.sum(res, axis=0)

compositeSignal /= np.max(np.abs(compositeSignal))

# Task 13
sd.play(compositeSignal, sampleFreq)
sd.wait()






    


