#!/bin/bash

# a simple script for recording a sentence and playing it back
arecord -vv -fdat $1.wav
sox $1.wav a.wav noisered record.noise-profile 0.3
rm $1.wav
mv a.wav $1.wav
