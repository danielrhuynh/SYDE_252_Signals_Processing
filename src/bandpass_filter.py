import numpy as np
from scipy.signal import firwin, lfilter, sosfilt, tf2zpk, zpk2sos
from scipy.io import wavfile
import matplotlib.pyplot  as plt
import matlab.engine
import sounddevice as sd

"""
Background:
    We are using a FIR Filter for the following reasons:
    Linear phase response: preserves the time-domain characteristics of input.
        This is important for a cochlear implant since phase linearity
        is critical for accurate sound reproduction, particularly for speech
        comprehension.
    Frequency Selection:
        FIR filters have a very sharp cutoff which is suitable for seperating speech into different
        frequency bands.
    Group Delay:
        This makes sure that all frequency components of a sound signal are delayed by the same time.
        FIR filters have a bit more of a delay especially FIR filters with a high order (taps).
        This needs to be balanced against frequency selection.

    FIR's in a real scenario:
        require more computational resources which kills battery.
        FIR's provide a sharp cutoff which introduces more delay into a system
        (talking to someone where their voice is delayed would suck kind of like when the sound of
        a video is delayed from the video).
    This isn't a real scenario though and we want the best possible results.
    A Bessel filter is a nice second choice.
"""

eng = matlab.engine.start_matlab()

# This is the sampling frequency we had from Phase 1
fs = 16000  

# Specified in Phase 2
lowFreq = 100
highFreq = 8000

# Chosen from lectures
NFrequencyBands = 8

# Create the edges of the frequency bands
edges = []

for i in np.arange(lowFreq, highFreq, (highFreq-lowFreq)/(NFrequencyBands+1)):
    edges.append(i)

filterBank = []

for i in range(NFrequencyBands):
    lowCutoff = edges[i]
    highCutoff = edges[i+1]

    # This is the order for the FIR filter
    taps = 101

    bandpassFilter = firwin(numtaps=taps, cutoff=[lowCutoff, highCutoff], fs=fs)
    z, p, a = tf2zpk(bandpassFilter, [1.0])
    sos = zpk2sos(z, p, a)
    filterBank.append(sos)

# samplePath = "sample1.mp3"

# Using MATLAB's python enginer
# s = eng.genpath('api')
# d = eng.genpath('resources')
# eng.addpath(s,nargout=0)
# eng.addpath(d,nargout=0)
# monoSignal, sampleFreq = eng.signals_processing(samplePath)

PATH = "./resources/output4.wav"
sampleFreq, signal = wavfile.read(PATH)

filteredSample = [sosfilt(bandpassFilter, signal) for bandpassFilter in filterBank]

t = np.arange(len(signal)) / sampleFreq

# Original Signal
plt.plot(t, signal)
plt.title("Original Signal")
plt.xlabel("Time [seconds]")
plt.ylabel("Amplitude")
plt.grid(True)

# Plot filtered signals
plt.figure(figsize=(12, 6))
for i, filteredSignal in enumerate(filteredSample):
    plt.plot(t, filteredSignal)
    plt.title(f'Band {i+1}: {edges[i]:.1f} - {edges[i+1]:.1f} Hz')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

compositeSignal = np.sum(filteredSample, axis=0)

# Normalizing signal to avoid clipping
compositeSignal /= np.max(np.abs(compositeSignal))
                         
# Playing the composite signal
print("Playing composite signal...")
sd.play(compositeSignal, sampleFreq)
sd.wait()

eng.quit()