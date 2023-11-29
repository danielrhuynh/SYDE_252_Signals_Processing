# Phase 3 Background
## Overview
One again, we're setting up a background.md file to report research briefs and facilitate knowledge transfer  
I'll update this file with cool stuff that I find and I recommend that you all do the same!  
*-Dan*
## Signal Exploration Tips
* Try playing each channel individually, taking note of which channels sound the best on which samples.  
For example, I found that the first channel is typically the **best channel** to sample from, that means that we 
should expand this channel out (weight it more heavily) when redistributing our filter.  
* More on this, I found that the l**ower frequency channels** typically sound better than the higher frequency channels, you can play around  
with this yourself just by listening to different channels in 'res' within synthesized_adio.py.  
* I think **12 is wayyyy too many channels**. Reducing to something like 3 (based off of the amount of channels I thought were the best through systematic  
experimentation) sounds better when you create a composite signal. Good luck justifying this... but systematic experimentation is always valid lol.   
* I think the channel distribution and the numebr of channels that we have will make the biggest difference. Already modifying this myself  
leads to much, much better results than what we had previously (we started with 12 channels). That being said, I don't think changer the specific  
type of filter that we use will make a huge difference but it's worth trying out just to see.  
* Try filters that have less group delay to reduce interference.  
* There is a decent amount of noise (as expected), what is causing this? Is this cumulative noise? Is this ringing caused by the  
filtering process? Might be worth investigating.  