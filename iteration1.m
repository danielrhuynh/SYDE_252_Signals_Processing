clearvars;
close all;

filename = ['samples/sample1.mp3'];
[f, fs] = audioread(filename); % y is the signal read into MATLAB, Fs is the sampling frequency of the signal y
% y is a 2D matrix. Col 1 is the left channel and col 2 is the right channel
y = f;
Fs = fs

numChannels = 12;
mono_or_stereo = size(y,2);
if mono_or_stereo == 2
    y = sum(y,2); %returns a column vector containing sum of each row
end

[targetrate,samplerate] = rat(16000/Fs);
y_resampled = resample(y,targetrate,samplerate);

filter_bank = cell(1,numChannels); % Empty cell array to contain the the signals of 22 frequency bands between 100Hz - 8kHz 
res = zeros(size(y));

frequencies = linspace(100,7999,numChannels+1);
figure;
stem(1:numChannels+1, frequencies, 'o-', 'LineWidth', 1.5);
xlabel('Channel Index');
ylabel('Frequency (Hz)');
grid on;

for i = 1:(numChannels)
    low = frequencies(i);
    high = frequencies(i+1);
    Hd = fir_window_kaiser(low, high);
    filter_bank{i} = filter(Hd,y_resampled);
    rectified_signal = abs(filter_bank{i});
    lowpassFilterCoefficients = [0.36161567304292236, 0.6383843269570776, 0.36161567304292236];
    envelopes = filter(lowpassFilterCoefficients, 1, rectified_signal);
    cos_signal = generate_cosine(16000, sqrt(low*high), envelopes);
    modulatedSignal = cos_signal.*envelopes;
    res = res + modulatedSignal;
end

% Task 12
compositeSignal = res / max(abs(res));

% Normalize the audio to the appropriate range (e.g., between -1 and 1)
compositeSignal = compositeSignal / max(abs(compositeSignal));

% Choose a file name and path for the new audio file
outputFilePath = 'samples/synthesized_audio4.wav';  % Specify your desired file path and name
% Write the audio to a new file
audiowrite(outputFilePath, compositeSignal, Fs);  % Specify the correct sample rate

sound(compositeSignal, 16000);


function signal = generate_cosine(Fs, frequency, envelopes)
    duration = (length(envelopes))/Fs;
    t=0:duration;
    signal = cos(2*pi*frequency*t);
    % figure;
    % plot(t, signal);
    % title('cosine')
    % xlabel('Time(s)')
    % ylabel('Cosine Signal')
end
