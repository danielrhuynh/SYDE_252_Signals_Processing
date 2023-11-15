# Background
We are using a FIR Filter for the following reasons:
    Linear phase response:
        Preserves the time-domain characteristics of input.
        This is important for a cochlear implant since phase linearity
        is critical for accurate sound reproduction, particularly for speech
        comprehension.
    Frequency Selection:
        FIR filters have a very sharp cutoff which is suitable for seperating speech into different
        frequency bands.
    Group Delay:
        This makes sure that all frequency components of a sound signal are delayed by the same time.
        FIR filters have a bit more of a delay especially FIR filters with a high order (taps).
        This needs to be balanced against frequency selection.

    FIR's in a real scenario:
        require more computational resources which kills battery.
        FIR's provide a sharp cutoff which introduces more delay into a system
        (talking to someone where their voice is delayed would suck kind of like when the sound of
        a video is delayed from the video).
    This isn't a real scenario though and we want the best possible results.
    A Bessel filter is a nice second choice.