# Binary Black Hole X-ray spectra

## TL;DR

```
bash bin/run.sh
```

## What's in it

- `bin` -> has files to run the binary models
- `dat` -> data files
- `ins` -> instrument response
- `ion` -> ionization gradient
- `mod` -> `tcl` files to make binary models into xspec, `xcm` = model files
- `plt` -> plotting scripts



to compile the ion C files:
```
gcc -o xivsrad xivsrad.c complex.c -lm
```
or
```
gcc -o xivsedd xivsedd.c complex.c -lm
```

