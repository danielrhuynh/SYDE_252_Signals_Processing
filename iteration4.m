clearvars;
close all;

filename = '/Users/chelseadmytryk/Documents/MATLAB/SYDE_252_Signals_Processing/samples/sample1.mp3';
[y, Fs] = audioread(filename); % y is the signal read into MATLAB, Fs is the sampling frequency of the signal y
% y is a 2D matrix. Col 1 is the left channel and col 2 is the right channel

low = 100;
high = 7999.99;
numChannels = 10;

mono_or_stereo = size(y,2);
if mono_or_stereo == 2
    y = sum(y,2); %returns a column vector containing sum of each row
end

[targetrate,samplerate] = rat(16000/Fs);
y_resampled = resample(y,targetrate,samplerate);

filter_bank = cell(1,numChannels+1); % plus 1 for the last edge point
res = zeros(size(y));

frequencies = exp(linspace(log(100),log(7999),numChannels+1)); %logarithmic spacing

% Plot the frequencies
figure;
stem(1:numChannels+1, frequencies, 'o-', 'LineWidth', 1.5);
title('Frequency vs. Channel');
xlabel('Channel Index');
ylabel('Frequency (Hz)');
grid on;

for i = 1:(numChannels)
    low = frequencies(i);
    high = frequencies(i+1);
    Hd = filterdesignfunc(low, high);
    filter_bank{i} = filter(Hd,y_resampled);

    rectified_signal = abs(filter_bank{i});
    Hd = lowpass_filter;
    envelopes = filter(Hd, rectified_signal);

    cos_signal = cosine(16000, sqrt(low*high), envelopes);
    modulatedSignal = cos_signal.*envelopes;
    res = res + modulatedSignal;
end

% Task 12
compositeSignal = res / max(abs(res));

% Normalize the audio to the appropriate range (e.g., between -1 and 1)
compositeSignal = compositeSignal / max(abs(compositeSignal));

% Choose a file name and path for the new audio file
outputFilePath = '/Users/chelseadmytryk/Documents/MATLAB/SYDE_252_Signals_Processing/samples/optimized_iteration4_synthesized_audio1.wav';  % Specify your desired file path and name
% Write the audio to a new file
audiowrite(outputFilePath, compositeSignal, Fs);  % Specify the correct sample rate

sound(compositeSignal, 16000);


function signal = cosine(Fs, frequency, envelopes)
    duration = (length(envelopes))/Fs;
    t=0:duration;
    signal = cos(2*pi*frequency*t);
    % figure;
    % plot(t, signal);
    % title('cosine')
    % xlabel('Time(s)')
    % ylabel('Cosine Signal')
end