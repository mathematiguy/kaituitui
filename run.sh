#!/bin/bash

set -ex

for design in watermelon heart duck; do
    # Inner loop
    for speed in fast slow; do  # Assuming speed 0 is fast and 10 is slow based on the typical turtle module speed settings
        for repeat in 2 3 4; do
                python kaituitui.py --savegif --width 900 --speed $speed --design $design --repeat $repeat
        done
    done
done
