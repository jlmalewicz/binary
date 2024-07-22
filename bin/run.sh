#!/bin/bash

export HEADAS=~/work/heasoft-6.33.2/x86_64-pc-linux-gnu-libc2.35
source $HEADAS/headas-init.sh

cd bin
python3 001_ini_parser.py
python3 002_relxill_wrapper.py

cd ..
mv dat_* ../dat/.