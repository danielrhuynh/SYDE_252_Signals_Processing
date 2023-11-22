import numpy as np

from scipy.signal import firwin, lfilter, butter

import matplotlib.pyplot  as plt
import matlab.engine
import sounddevice as sd

# def butter_lowpass_filter(data, cutoff, fs, order):
#     normal_cutoff = cutoff / nyq
#     # Get the filter coefficients 
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     y = filtfilt(b, a, data)
#     return 5

def running_mean(x, windowSize):
   cumsum = np.cumsum(np.insert(x, 0, 0)) 
   return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize 

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
    filterBank.append(firCoeffs)

samplePath = "../samples/sample1.mp3"

# Using MATLAB's python engine to preprocess
s = eng.genpath('../api')
d = eng.genpath('../samples')
eng.addpath(s,nargout=0)
eng.addpath(d,nargout=0)
[monoSignal, sampleFreq] = eng.signals_processing(samplePath, nargout=2)

filteredSample = [lfilter(bandpassFilter, [1.0], monoSignal) for bandpassFilter in filterBank]

t = np.arange(len(monoSignal)) / sampleFreq

# Original Signal
# plt.plot(t, monoSignal)
# plt.title("Original Signal")
# plt.xlabel("Time [seconds]")
# plt.ylabel("Amplitude")
# plt.grid(True)
# plt.show()

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
# recFilteredSample = [abs(sample) for sample in filteredSample]

# # Plot rectified signals all in the same figure
# # fig, axes = plt.subplots(3, 4, figsize=(12, 8))
# # axes = axes.flatten()
# # for i, rectifiedSample in enumerate(recFilteredSample):
# #     row, col = divmod(i, 4) 
# #     axes[i].plot(t, rectifiedSample)
# #     axes[i].set_title(f'Rectified Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
# #     axes[i].set_xlabel("Time [seconds]")
# #     axes[i].set_ylabel("Amplitude")
# #     axes[i].grid(True)
# # plt.tight_layout()
# # plt.show()

# # Cutoff frequency for the lowpass filter
# cutOffFrequency = 400.0
# freqRatio = cutOffFrequency / fs
# N = int(np.sqrt(0.196201 + freqRatio**2) / freqRatio)
# print(N)
# #filtered = running_mean(recFilteredSample[0], N)
# #filtered = [running_mean(signal, N) for signal in recFilteredSample]

# # Filter requirements.
# cutoff = 400      # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hz
# nyq = 0.5 * fs  # Nyquist Frequency
# order = 2       # sin wave can be approx represented as quadratic
# n = int(t * fs) # total number of samples
# y = butter_lowpass_filter(recFilteredSample[0], cutoff, fs, order)
# print(N)
# plt.plot(t, monoSignal)
# plt.title("Original Signal")
# plt.xlabel("Time [seconds]")
# plt.ylabel("Amplitude")
# plt.grid(True)
# plt.show()
# print(N)
#envelopes = [lowpass_filter(rectifiedSignal, cutOffFrequency, sampleFreq) for rectifiedSignal in recFilteredSample]

# Plot original rectified signals and their envelopes
# for i, (rectifiedSignal, filtered) in enumerate(zip(recFilteredSample, filtered)):
#     # Create a single subplot
#     fig, ax = plt.subplots(figsize=(10, 6))
#     # Plot rectified signal
#     ax.plot(t, rectifiedSignal, label='Rectified Signal')
#     ax.set_title(f'Rectified Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
#     ax.set_xlabel("Time [seconds]")
#     ax.set_ylabel("Amplitude")
#     ax.grid(True)
#     # Plot envelope on the same subplot
#     ax.plot(t, filtered, color='orange', label='Envelope')
#     ax.legend() 
#     plt.tight_layout()
#     plt.show()

compositeSignal = np.sum(filteredSample, axis=0)

# Normalizing signal to avoid clipping
compositeSignal /= np.max(np.abs(compositeSignal))
                         
# Playing the composite signal
print("Playing composite signal...")
sd.play(compositeSignal, sampleFreq)
sd.wait()

eng.quit()