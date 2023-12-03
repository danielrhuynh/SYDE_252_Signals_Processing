filename = '../samples/output4.wav';
[y, Fs] = audioread(filename);

numChannels = 12;
mono_or_stereo = size(y,2);
if mono_or_stereo == 2
    y = sum(y,2); %returns a column vector containing sum of each row
end

[targetrate,samplerate] = rat(16000/Fs);
y_resampled = resample(y,targetrate,samplerate);

% Logarithmically spaced center frequencies
centerFrequencies = logspace(log10(100), log10(7900), numChannels);

filter_bank = cell(1,numChannels); % Empty cell array to contain the the signals of 22 frequency bands between 100Hz - 8kHz 

for i = 1:numChannels
    low = centerFrequencies(i); % Adjust as needed
    if i==numChannels
        high = 7999;
    else
        high = centerFrequencies(i+1); % Adjust as needed
    end 
    Hd = filterdesignfunc(low, high);
    filter_bank{i} = filter(Hd,y_resampled);
end

subplot(2,2,1)
xaxis1 = (1:length(filter_bank{1}))/Fs;
plot(xaxis1, filter_bank{1});
title('Output signal plot of lowest frequency channel')
xlabel('Time(s)')
ylabel('Amplitude')

subplot(2,2,3)
xaxis2 = (1:length(filter_bank{numChannels}))/Fs;
plot(xaxis2, filter_bank{numChannels});
title('Output signal plot of highest frequency channel')
xlabel('Time(s)')
ylabel('Amplitude')

rectified_signals = cell(1, numChannels); % Will hold rectified output signals
envelopes = cell(1,numChannels); % Will hold extracted envelopes of rectified signals

for n = 1:numChannels
    rectified_signals{n} = abs(filter_bank{n}); % Rectify signals in filter bank using the absolute function
    envelopes{n} = filter(lowpass_filter, rectified_signals{n}); % Extract the envelopes from the rectified signals using lowpass filter
end


subplot(2,2,2)
plot((0:length(envelopes{1})-1)/Fs, envelopes{1});
title('Extracted Envelope of lowest frequency channel')
xlabel('Time(s)')
ylabel('Extracted Envelope')

subplot(2,2,4)
plot((0:length(envelopes{numChannels})-1)/Fs, envelopes{numChannels});
title('Extracted Envelope of highest frequency channel')
xlabel('Time(s)')
ylabel('Extracted Envelope')


rectified_signals = cell(1, numChannels); % Will hold rectified output signals
envelopes = cell(1,numChannels); % Will hold extracted envelopes of rectified signals

% Task 10
res = cell(1, numChannels);
for i = 1:numChannels
    
    t = (0:length(envelopes{i}) - 1) / Fs;
    cosSignal = cos(2 * pi * centerFrequencies(i) * t);

    envelope = envelopes{i}';
    
    % Task 11
    modulatedSignal = cosSignal .* envelope;
    res{i} = modulatedSignal;
end

% Task 12
% compositeSignal = sum(cell2mat(res), 2);
% Combine the filtered signals into a single output
compositeSignal = sum(cat(3, filter_bank{:}), 3);


% Combine the filtered signals into a single output
filtered_signal = sum(cat(3, filter_bank{:}), 3);

% Play the filtered sound clip
sound(compositeSignal, Fs);




function Hd = lowpass_filter
Fs = 16000;  % Sampling Frequency

Fpass = 0;          % Passband Frequency - crushing higher frequencies out
Fstop = 400;        % Stopband Frequency - actual stopping point for what is allowed 
Dpass = 0.01;       % Passband Ripple
Dstop = 0.000001;   % Stopband Attenuation
dens  = 20;         % Density Factor

% Calculate the order from the parameters using FIRPMORD.
[N, Fo, Ao, W] = firpmord([Fpass, Fstop]/(Fs/2), [1 0], [Dpass, Dstop]);

% Calculate the coefficients using the FIRPM function.
b  = firpm(N, Fo, Ao, W, {dens});
Hd = dfilt.dffir(b);
end
