cpd /xs
lmod relxill ../relxill/.
model cflux*zashift*relxilllpCp + cflux*zashift*relxilllpCp
# 1 :    Emin
2
# 1 :    Emax
10
# 1 :    lg10Flux
-12.55
# 1 :    Redshift
0.023
# 1 :    Incl
30
# 1 :    a
0.99
# 1 :    Rin
-1
# 1 :    Rout
51.29
# 1 :    h
10
# 1 :    beta
0
# 1 :    gamma
2
# 1 :    logxi
2.576
# 1 :    logN
15
# 1 :    Afe
1
# 1 :    kTe
60
# 1 :    refl_frac
1
# 1 :    z
1.0
# 1 :    iongrad_index
0
# 1 :    iongrad_type
2
# 1 :    switch_returnrad
1
# 1 :    switch_reflfrac_boost
1
# 1 :    norm       ##############################
1 -1
# 2 :    Emin
2
# 2 :    Emax
10
# 2 :    lg10Flux
-12.60
# 2 :    Redshift
-0.027
# 2 :    Incl
30
# 2 :    a
0.99
# 2 :    Rin
-1
# 2 :    Rout
54.31
# 2 :    h
10
# 2 :    beta
0
# 2 :    gamma
2
# 2 :    logxi
2.851
# 2 :    logN
15
# 2 :    Afe
1
# 2 :    kTe
60
# 2 :    refl_frac
1
# 2 :    z
1.0
# 2 :    iongrad_index
0
# 2 :    iongrad_type
2
# 2 :    switch_returnrad
1
# 2 :    switch_reflfrac_boost
1
# 2 :    norm
1 -1
setp co LA T Binary z=1.0 log10(M/Msun)=9
pl eemod
save model models/model_binary_logm9_z1.0.xcm