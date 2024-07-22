#!/bin/bash



for filename in *z1.0logm6*ed.fak; do
    # Perform the desired operation on each file
    grppha infile="$filename" outfile="${filename%.fak}_rebin20.fak" chatter=0 comm="group min 20 & exit"
done