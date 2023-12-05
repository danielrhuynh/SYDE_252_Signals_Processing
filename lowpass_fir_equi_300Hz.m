function Hd = lowpass_fir_equi_300Hz

% All frequency values are in Hz.
Fs = 16000;  % Sampling Frequency
N     = 8;               % Order
Fc    = 7000;             % Cutoff Frequency
slope = 0;               % Stopband Slope
Dstop = 0.0001;          % Stopband Attenuation
Dpass = 0.057501127785;  % Passband Ripple

% Calculate the coefficients using the FIRCEQRIP function.
b  = firceqrip(N, Fc/(Fs/2), [Dpass, Dstop], 'slope', slope);
Hd = dfilt.dffir(b);

% [EOF]
