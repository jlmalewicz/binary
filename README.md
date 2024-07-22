```
source bin/run.sh
```

to compile the ion C files:

gcc -o xivsrad xivsrad.c complex.c -lm
or
gcc -o xivsrad xivsrad.c complex.c -lm


bin -> has files to run the binary models
dat -> data files
ins -> instrument response
ion -> ionization gradient
mod -> tcl files to call binary models into xspec, xcm = model
plt -> plotting scripts
