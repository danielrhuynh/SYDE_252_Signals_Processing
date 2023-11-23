import numpy as np
from scipy.signal import firwin, lfilter
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

    # This is the order for the FIR filter
    taps = 3

    # Needed to modify this according to Nyquist's theorem
    if highCutoff == fs/2:
        highCutoff *= 0.999

    # Beta was decided through systematic experimentation
    firCoeffs = firwin(numtaps=taps, cutoff=[lowCutoff, highCutoff], fs=fs, pass_zero=False, window=('kaiser', 0.9))
    filterBank.append(firCoeffs)

samplePath = "../samples/sample4.mp3"

# Using MATLAB's python engine to preprocess
s = eng.genpath('../api')
d = eng.genpath('../samples')
eng.addpath(s,nargout=0)
eng.addpath(d,nargout=0)
[monoSignal, sampleFreq] = eng.signals_processing(samplePath, nargout=2)

filteredSample = [lfilter(bandpassFilter, [1.0], monoSignal) for bandpassFilter in filterBank]

t = np.arange(len(monoSignal)) / sampleFreq

# Plot filtered signals
# for i, channel in enumerate(filteredSample):
#     plt.figure()
#     plt.plot(t, monoSignal, label='Original Signal', color='blue')
#     plt.plot(t, channel, label=f'Filtered Channel {i+1}', color='red')
#     plt.title(f'Original Signal and Filtered Channel {i+1}')
#     plt.xlabel('Time [seconds]')
#     plt.ylabel('Amplitude')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# Or plot all 12 on same figure
# fig, axes = plt.subplots(3, 4, figsize=(12, 8))
# axes = axes.flatten()
# for i, filteredSignal in enumerate(filteredSample):
#     row, col = divmod(i, 4)
#     axes[i].plot(t, filteredSignal)
#     axes[i].set_title(f'Filtered Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
#     axes[i].set_xlabel("Time [seconds]")
#     axes[i].set_ylabel("Amplitude")
#     axes[i].grid(True)
# plt.tight_layout()
# plt.show()

# Task 7: Rectify each band by taking the abs value of the signal for each band
recFilteredSample = [abs(sample) for sample in filteredSample]

# Plot recFilteredSample signals
# for i, rec in enumerate(recFilteredSample):
#     plt.plot(t, rec)
#     plt.title(f'Rectified Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
#     plt.xlabel("Time [seconds]")
#     plt.ylabel("Amplitude")
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

# Plot rectified signals all in the same figure
# fig, axes = plt.subplots(3, 4, figsize=(12, 8))
# axes = axes.flatten()
# for i, rectifiedSample in enumerate(recFilteredSample):
#     row, col = divmod(i, 4) 
#     axes[i].plot(t, rectifiedSample)
#     axes[i].set_title(f'Rectified Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
#     axes[i].set_xlabel("Time [seconds]")
#     axes[i].set_ylabel("Amplitude")
#     axes[i].grid(True)
# plt.tight_layout()
# plt.show()

# Task 8: Apply lowpass filter to recFilteredSample. Coefficients found using the pyFDA GUI. Lowpass, FIR, Quiripple, Order N = 2, f_s = 1.6 kHz, f_PB = 0.4, f_SB = 0.5, A_PB = 1 [dB], A_SB = 60 [dB], W_pB = 1, W_SB = 1. 
lowpassFilterCoefficients = [0.36161567304292236, 0.6383843269570776, 0.36161567304292236] #these are the b values (the numerator coefficient vector in a 1-D sequence)

try:
    envelopes = [lfilter(lowpassFilterCoefficients, [1.0], channel) for channel in recFilteredSample]
except Exception as e:
    print(f"An error occurred: {e}")

# Plot envelope signals
# fig, axes = plt.subplots(3, 4, figsize=(12, 8))
# axes = axes.flatten()
# for i, envelope in enumerate(envelopes):
#     row, col = divmod(i, 4)
#     axes[i].plot(t, envelope)
#     axes[i].set_title(f'Filtered Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
#     axes[i].set_xlabel("Time [seconds]")
#     axes[i].set_ylabel("Amplitude")
#     axes[i].grid(True)
# plt.tight_layout()
# plt.show()

# fig, axes = plt.subplots(3, 4, figsize=(12, 8))
# axes = axes.flatten()
# for i, envelope in enumerate(envelopes):
#     row, col = divmod(i, 4) 
#     axes[i].plot(t, envelope)
#     axes[i].set_title(f'Evelope of Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
#     axes[i].set_xlabel("Time [seconds]")
#     axes[i].set_ylabel("Amplitude")
#     axes[i].grid(True)
# plt.tight_layout()
# plt.show()

# Plot a comparison of all the signals of each band
for i in range(NFrequencyBands):
    plt.figure()
    plt.plot(t, monoSignal, label='Original Signal')
    plt.plot(t, filteredSample[i], label='filteredSample')
    plt.plot(t, recFilteredSample[i], label='recFilteredSample')
    plt.plot(t, envelopes[i], label='envelope')
    plt.title(f"Band {i + 1} Comparison")
    plt.xlabel("Time [seconds]")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()

compositeSignal = np.sum(filteredSample, axis=0)

# Normalizing signal to avoid clipping
compositeSignal /= np.max(np.abs(compositeSignal))
                         
# Playing the composite signal
print("Playing composite signal...")
sd.play(compositeSignal, sampleFreq)
sd.wait()

eng.quit()