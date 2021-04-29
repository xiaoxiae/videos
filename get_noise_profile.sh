#!/bin/bash

sleep 1.5
arecord -vv -d 3 -fdat noise.wav
sox noise.wav -n noiseprof record.noise-profile
rm noise.wav
