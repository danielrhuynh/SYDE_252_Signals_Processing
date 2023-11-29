from bandpass_filter import filterBank, edges, sampleFreq, envelopes, samplePath
import numpy as np
import math
import sounddevice as sd
from scipy.io.wavfile import write

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

fileName = samplePath.split('/')[-1].split('.')[0]

# Task 13
write(f"../samples/synthesized{fileName}.mp3", int(sampleFreq), compositeSignal)

print("Playing synthesized audio...")
sd.play(compositeSignal, sampleFreq)
sd.wait()
print("Done!")