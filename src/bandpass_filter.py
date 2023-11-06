import sys
import numpy as np
import scipy
from scipy.signal import firwin, lfilter
import matlab.engine

eng = matlab.engine.start_matlab()

fs = 16000
low_freq = 100
high_freq = 8000

N = 12

edges = np.linspace(low_freq, high_freq, N+1)

# Da bank
filters = []



eng.quit()