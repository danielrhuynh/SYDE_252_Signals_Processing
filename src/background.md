# Background
This should provide some insights into my engineering decision making.  
Take these justifications and find more resources to back them up!  
This is meant to just be a scratch pad for me to logic my way through my decision making process!  
## We are using a FIR Filter for the following reasons:
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
**where:**  
* y[n] is the output of the filter at time n  
* x[n] is the inpout signal  
* b_i are coeffs  
* N is the order of the filter  

```
FIR filters have coefficients which are found using the firwin function in scipy  
These things are very stable since all poles are at the origin in the z-plane and  
can easily be designed to be linear in phase.  This preserves the shape of a filtered signal.  
See above more more notes.  

Scipy specifically uses the windowing method which truncates the ideal filter  
of infinite duration to a finite length. This generally introduces ripples (bad)  
We apply a window function to the truncated impulse response which smooths the impulse  
response near its end to 0. The result of windowing to the ideal truncated impulse response  
are the FIR coefficients.
```

### Lets Talk More about Windowing
Here I use a kaiser window because it gives me more control over the trade-off between the main-lobe width  
and side lobe level [docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.windows.kaiser.html).  

Please look into what these concepts are and briefly state them in the report.  
[Kaiser Window](https://en.wikipedia.org/wiki/Kaiser_window)  
**Briefly though:**  
Main Lobe:
* The central or highest peak in the frequency response. This is the frequency where the filter has the biggest effect.  
* This controls resolution, narrowing allows for more precise distinction between frequencies.  
Side Lobe:
* Frequencies that unintentionally affect the signal. These can be problematic as undesired frequencies can leak into the signal.  
* A narrower main lobe often comes at the expense of a larger side lobe. Beta controls this trade off.  Lower beta values  
    result in a narrower main lobe which allows some side lobe noise and results in lower attenuation. Our signal was attenuated to a magnitude of almost  
    4x previously so through systematic experimentation we bias beta towards lower attenuation since a small amount of side lobe leakage is fine.

**Resources:**
[Lobes]()

### More on FIRs Specific to this Project
```
Alright, so what I found out by messing around (say systematic experimentation in the report)  
is that introducing a higher filter order increases sharpness meaning you can more sharply  
transition from the passband to the stopband but will increase attenuation (lowers the magnitude a lot)  
At the filter order we had before (really any order greater than 5) we attenuate way too much removing  
much of the signal. At higher orders, the phase frequency response also becomes non-linear which is not good (look up why  
but basically this introduces group delay which introduces distortion). I changed the filter order to 3 which attenuates much  less and filters out an appropriate amount of noise as viewed by the  generated graph.
```

**Lets talk about the difference between even and odd orders and overshooting:**  
```
Even taps are not symmetrical since they don't have a middle tap to center themselves around.  
This leads to unpredictable behaviour since the group delay tends to be a non-integer and a non-linear  
phase response which eliminates a major advantage of a FIR filter.
Odd taps are symmetrical and are more stable and predictable due to the ensured linear phase response.  
This means that the filter introduces a constant delay across all signals.  
Even taps lead to overshooting at higher passbands which is undesirable because it leads to distortion and deviates  
from the original signal.

BIG MISCONCEPTION:  
The number of taps is NOT the order.  
The number of taps = order + 1 since we need to account for the coeff on the x^0 term.
```

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
## lfilter
    This applies a linear digital filter (FIR filter) to a signal along one-dimension.  
[Docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.lfilter.html)  
[Maybe try looking around this book for FIR filters](https://flylib.com/books/en/2.729.1/chapter_five_finite_impulse_response_filters.html)  
[Learn more about using convolution to apply filters](https://ccrma.stanford.edu/~jos/fp/Convolution_Representation_FIR_Filters.html)
[Even more stuff about convolution](https://scipy-cookbook.readthedocs.io/items/ApplyFIRFilter.html)

    This implements a linear, time-invariant filter given by:
$$ H(z) = \frac{B(z)}{A(z)} = \frac{\sum_{i=0}^{M} b[i] z^{-i}}{\sum_{i=0}^{N} a[i] z^{-i}} $$
    Where B and A are polynomial coefficients. You use convolution to apply a filter  
    the impulse response in this case is the sequence of FIR coefficients and x(t) is the signal.

### Conclusion
Hopefully this provides enough context to understand the filter code.  
***Of course feel free to reach out if you need help!***