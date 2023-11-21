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

# def running_mean(x, windowSize):
#    cumsum = np.cumsum(np.insert(x, 0, 0)) 
#    return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize 

def lowpass(data: np.ndarray, cutoff: float, sample_rate: float, poles: int = 5):
    sos = butter(poles, cutoff, 'lowpass', fs=sample_rate, output='sos')
    filtered_data = sosfiltfilt(sos, data)
    return filtered_data





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

samplePath = "../samples/sample1.mp3"

# Using MATLAB's python engine to preprocess
s = eng.genpath('../api')
d = eng.genpath('../samples')
eng.addpath(s,nargout=0)
eng.addpath(d,nargout=0)
[monoSignal, sampleFreq] = eng.signals_processing(samplePath, nargout=2)

filteredSample = [lfilter(bandpassFilter, [1.0], monoSignal) for bandpassFilter in filterBank]

t = np.arange(len(monoSignal)) / sampleFreq

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
    plt.plot(t, monoSignal, label="Original Signal")
    plt.plot(t, filteredSignal, label=f"Bank {i+1}")
    plt.title(f'Original Signal vs Band {i+1}: {edges[i]:.0f} - {edges[i+1]:.0f} Hz')
    plt.xlabel("Time [seconds]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
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
# print("Playing composite signal...")
# sd.play(compositeSignal, sampleFreq)
# sd.wait()

eng.quit()