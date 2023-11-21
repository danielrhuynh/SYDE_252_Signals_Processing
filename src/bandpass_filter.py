import numpy as np
from scipy.signal import firwin, lfilter, sosfilt, tf2zpk, zpk2sos, butter
import matplotlib.pyplot  as plt
import matlab.engine
import sounddevice as sd

eng = matlab.engine.start_matlab()

# This is the sampling frequency we had from Phase 1
fs = 16000

# Specified in Phase 2
lowFreq = 100

highFreq = 8000

# Chosen from lectures
NFrequencyBands = 12

# Create the edges of the frequency bands
edges = []

for i in np.arange(lowFreq, highFreq, (highFreq-lowFreq)/(NFrequencyBands)):
    edges.append(i)
edges.append(highFreq)

filterBank = []

for i in range(NFrequencyBands):
    lowCutoff = edges[i]
    highCutoff = edges[i+1]

    # Needed to modify this according to Nyquist's theorem
    if highCutoff == fs/2:
        highCutoff *= 0.999

    # This is the order for the FIR filter (odd for Type 1)
    taps = 101

    firCoeffs = firwin(numtaps=taps, cutoff=[lowCutoff, highCutoff], fs=fs)
    z, p, a = tf2zpk(firCoeffs, [1.0])
    secondOrderSections = zpk2sos(z, p, a)
    filterBank.append(secondOrderSections)

samplePath = "../samples/sample1.mp3"

# Using MATLAB's python engine to preprocess
s = eng.genpath('../api')
d = eng.genpath('../samples')
eng.addpath(s,nargout=0)
eng.addpath(d,nargout=0)
[monoSignal, sampleFreq] = eng.signals_processing(samplePath, nargout=2)

filteredSample = [sosfilt(bandpassFilter, monoSignal) for bandpassFilter in filterBank]

t = np.arange(len(monoSignal)) / sampleFreq

# Original Signal
plt.plot(t, monoSignal)
plt.title("Original Signal")
plt.xlabel("Time [seconds]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()

# Plot filtered signals
# for i, filteredSignal in enumerate(filteredSample):
#     plt.plot(t, filteredSignal)
#     plt.title(f'Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
#     plt.xlabel("Time [seconds]")
#     plt.ylabel("Amplitude")
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

# Or plot all 12 on same figure
fig, axes = plt.subplots(3, 4, figsize=(12, 8))
axes = axes.flatten()
for i, filteredSignal in enumerate(filteredSample):
    row, col = divmod(i, 4)
    axes[i].plot(t, filteredSignal)
    axes[i].set_title(f'Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
    axes[i].set_xlabel("Time [seconds]")
    axes[i].set_ylabel("Amplitude")
    axes[i].grid(True)
plt.tight_layout()
plt.show()

# Rectify each band by taking the abs value of the signal for each band
recFilteredSample = [abs(sample) for sample in filteredSample]

# Plot rectified signals all in the same figure
fig, axes = plt.subplots(3, 4, figsize=(12, 8))
axes = axes.flatten()
for i, rectifiedSample in enumerate(recFilteredSample):
    row, col = divmod(i, 4) 
    axes[i].plot(t, rectifiedSample)
    axes[i].set_title(f'Rectified Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
    axes[i].set_xlabel("Time [seconds]")
    axes[i].set_ylabel("Amplitude")
    axes[i].grid(True)
plt.tight_layout()
plt.show()

# Cutoff frequency for the lowpass filter
cutoff_frequency = 400

compositeSignal = np.sum(filteredSample, axis=0)

# Normalizing signal to avoid clipping
compositeSignal /= np.max(np.abs(compositeSignal))
                         
# Playing the composite signal
print("Playing composite signal...")
sd.play(compositeSignal, sampleFreq)
sd.wait()

eng.quit()