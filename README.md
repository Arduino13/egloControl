# egloControl
Script for color control of EGLO Surface in my case model EFueva 300s

This script was created with help of reverese engineering of AwoX smart CONTROL application available on Google Play. For now it can only control
color of a light. 

# Usage 
```
python evoControl.py [sequenceNumber] [redIntensity] [greenIntensity] [blueIntensity] [powerOff]
```
sequenceNumber - after turning on the light every command need to have higher number than previous one, their numbers don't need to be in sequence. 
After turning off the light this counter is resetted.

redIntensity, greenIntensity, blueIntensity - number from 0 to 127

powerOff - 0 for change of color, 1 - to turn the light off

a.out is for now compiled for Raspoberry Pi, source is inside main.cpp, unfortunetly TelinkCrypto.o is soft float library for ARM, you probably need to use
crosscompiler to make it work. I used https://crosstool-ng.github.io/, which is great tool and always worked for me.
