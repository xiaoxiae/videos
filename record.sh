#!/bin/bash

# a simple script for recording a sentence and playing it back
arecord -vv -fdat $1.wav
sox $1.wav a.wav noisered record.noise-profile 0.3
sox a.wav b.wav trim 0.5 -0.5
rm $1.wav
rm a.wav
mv b.wav $1.wav
