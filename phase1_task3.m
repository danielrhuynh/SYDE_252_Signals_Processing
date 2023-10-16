[sample1_mono, Fs] = signals_processing("sample1.mp3");
[sample3_mono, Fs] = signals_processing("sample3.mp3");
[sample4_mono, Fs] = signals_processing("sample4.mp3");

% 3.4
% Write to audio file
audiowrite('output1.mp3', sample1_mono, Fs);
audiowrite('output3.mp3', sample3_mono, Fs);
audiowrite('output4.mp3', sample4_mono, Fs);