[sample_1_mono, Fs] = signals_processing("sample_1.mp3");

% 3.4
% Write to audio file
audiowrite('output.mp3', sample_1_mono, Fs);