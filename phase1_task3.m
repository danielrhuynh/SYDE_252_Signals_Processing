% 3.1
filename = 'test.wav';
[y, Fs] = audioread(filename); % Where y and Fs are the audio data and sampling frequency respectively

% 3.2
% y is a matrix where each column is a channel and each row is a sample
[numRows, numChannels] = size(y);

if numChannels > 1
    monoSignal = sum(y, 2); % Sums columns along the second dimension (1st axis)
else
    monoSignal = y;
end

% 3.3
sound(monoSignal, Fs);

% 3.4
t = (0:(length(y) - 1)) / Fs;  % Time vector in seconds
plot(t, y);
xlabel('Time (s)');
ylabel('Amplitude');
title('Audio Waveform of test.wav');