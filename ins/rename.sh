#!/bin/bash

for file in *mincnts1.fak; do
    # Perform the desired operation on each file
    mv "$file" "${file%mincnt1.fak}rebin1.fak"
done