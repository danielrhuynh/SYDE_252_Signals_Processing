[sample1_mono, Fs] = signals_processing("../resources/sample1.mp3");
[sample3_mono, Fs] = signals_processing("../resources/sample3.mp3");
[sample4_mono, Fs] = signals_processing("../resources/sample4.mp3");

% 3.4
% Write to audio file
audiowrite('../resources/output1.mp3', sample1_mono, Fs);
audiowrite('../resources/output3.mp3', sample3_mono, Fs);
audiowrite('../resources/output4.mp3', sample4_mono, Fs);