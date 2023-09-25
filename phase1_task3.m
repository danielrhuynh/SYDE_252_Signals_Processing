% First Commit
filename = 'test.wav';
[y, Fs] = audioread(filename); % Where y and Fs are the audio data and sampling frequency respectively

% y is a matrix where each column is a channel and each row is a sample
[numRows, numChannels] = size(y);

if numChannels > 1
    monoSignal = sum(y, 2) % Sums columns along the second dimension (1st axis)
else
    monoSignal = y;
end

