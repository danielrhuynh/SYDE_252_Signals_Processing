function [monoSignal, Fs] = signals_processing(filename)
    % 3.1
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
    % sound(monoSignal, Fs);

    % 3.5
    t = (0:(length(monoSignal) - 1)) / Fs;  % Time vector in sample steps (sample numbers)
    plot(t, y);
    xlabel('Time [s]');
    ylabel('Amplitude');
    title(['Audio Waveform of ', filename]);

    % 3.6
    if Fs > 16000
        monoSignal = resample(y, 16000, Fs);
        Fs = 16000;
    end

    disp(Fs);

    % 3.7
    % FREQ = 1000;
    % cosSignal = cos(2 * pi * FREQ * t);

    % sound(cosSignal, Fs);

    % plot(t, cosSignal);
    % xlabel('Time (s)');
    % ylabel('Amplitude');
    % title('Cosine Waveform (1 kHz)');

    % Zooming in
    % plot(t, cosSignal);
    % xlabel('Time [s]');
    % ylabel('Amplitude');
    % title('Zoomed-in Cosine Waveform (1 kHz) of ' + filename);
    % xlim([0, 2 / 1000]);  % Show only two cycles (2 ms)
end