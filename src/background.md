# Background
We are using a FIR Filter for the following reasons:

### Linear phase response:
    Preserves the time-domain characteristics of input.
    This is important for a cochlear implant since phase linearity
    is critical for accurate sound reproduction, particularly for speech
    comprehension.

### Frequency Selection:
    FIR filters have a very sharp cutoff which is suitable for seperating speech into different
    frequency bands.

### Group Delay:
    This makes sure that all frequency components of a sound signal are delayed by the same time.
    FIR filters have a bit more of a delay especially FIR filters with a high order (taps).
    This needs to be balanced against frequency selection.

### FIR's in a real scenario:
    Requires more computational resources which kills battery.
    FIR's provide a sharp cutoff which introduces more delay into a system
    (talking to someone where their voice is delayed would suck kind of like when the sound of
    a video is delayed from the video).
    This isn't a real scenario though and we want the best possible results.
    A Bessel filter is a nice second choice.

# Misc information for the report
## Nyquist Frequency:
    This is the highest frequency that can be reliably measured (without introducing aliasing).  
    This is 1/2 of the sample frequency. Aliasing is a type of distortion.  
## FIR:
    FIR filters have the form y[n] = b_0x[n]+b_1x[n-1]+...+b_n-1x[n-(N-1)]  
    where:
    y[n] is the output of the filter at time n  
    x[n] is the inpout signal
    b_i are coeffs
    N is the order of the filter
    FIR filters have coefficients which are found using the firwin function in scipy
    These things are very stable since all poles are at the origin in the z-plane and  
    can easily be designed to be linear in phase.  This preserves the shape of a filtered signal.
    See above more more notes.

    Scipy specifically uses the windowing method which truncates the ideal filter  
    of infinite duration to a finite length. This generally introduces ripples (bad)  
    We apply a window function to the truncated impulse response which smooths the impulse  
    response near its end to 0. The result of windowing to the ideal truncated impulse response  
    are the FIR coefficients.
## Zero / Pole / Gain form:
    This is a way of describing an LTI system in terms of their zeros, poles and gain.  
    Zeros are the frequencies where the systems output is 0 regardless of the input. (Roots of numerator)  
    Poles are the frequencies where the systems output is theoretically infinite if purely  
    analog. (Roots of denominator)  
    Gain is a total system amplification factor.  
## Second Order Sections:
    This is a method of implementing high order filters by  
    chaining a series of second-order filters.  
    By doing so we get numerical stabillity leading to better control over  
    the filter's characteristics. This is important for high order filters where the poles  
    and zeroes are closesly spaced.  This is mainly black boxed thanks to scipy.
## Rectifying Signals:
    Process in which all the negative portions of the signal are eliminated. There are two types of rectification: half-wave and full-wave. In half-wave, only the positive portion of the signal remains, and the negative portions are clipped to zero. A full-wave rectifier inverts all the negative portions so that the entire signal has positive values.
### Conclusion
Hopefully this provides enough context to understand the filter.  
Ff course more research should be done for the report!
