#!/bin/bash

set -ex


for speed in fast; do
    for repeat in 2 4; do
            for design in watermelon heart duck; do
            # Construct the expected GIF filename based on current parameters
            filename="gif/${design}-${speed}-x${repeat}.gif"

            # Check if the GIF file already exists
            if [ -f "$filename" ]; then
                echo "Skipping ${filename}, already exists."
                continue  # Skip to the next iteration
            fi

            # Execute the Python script if the file does not exist
            python kaituitui.py --savegif --width 900 --speed $speed --design $design --repeat $repeat
        done
    done
done
