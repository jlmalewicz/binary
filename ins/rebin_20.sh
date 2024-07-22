#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi

# Extract the filename from the command-line argument
filename="$1"

# Perform the desired operation on the specified file
grppha infile="$filename" outfile="${filename%.fak}_rebin20.fak" chatter=0 comm="group min 20 & exit"