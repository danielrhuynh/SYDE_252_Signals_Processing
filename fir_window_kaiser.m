% filter from phase 2
function Hd = fir_window_kaiser(low,high)

% All frequency values are in Hz.
Fs = 16000;  % Sampling Frequency
disp("------");
disp("Difference:");
high-low
taps    = 5;       % Order
Fc1  = low;      % First Cutoff Frequency
Fc2  = high;      % Second Cutoff Frequency
flag = 'scale';  % Sampling Flag
Beta = 0.9;      % Window Parameter
% Create the window vector for the design algorithm.
win = kaiser(taps+1, Beta);

% Calculate the coefficients using the FIR1 function.
b  = fir1(taps, [Fc1 Fc2]/(Fs/2), 'bandpass', win);
Hd = dfilt.dffir(b);

% [EOF]
