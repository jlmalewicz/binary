cpd /xs
lmod relxill ../relxill/.
model phabs*cflux*zashift*relxilllpCp + phabs*cflux*zashift*relxilllpCp
# 1 :    nH
0.03
# 1 :    Emin, Emax, lg10Flux
2
10
-13.19
# 1 :    Redshift
0.023
# 1 :    Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
30
0.99
-1
51.29
10
0
2
2.576
15
1
60
1
1.0
0
2
1
1
1
# 2 :    nH
0.03
# 2 :    Emin, Emax, lg10Flux
2
10
-13.20
# 2 :    Redshift
-0.027
# 2 :    Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
30
0.99
-1
54.31
10
0
2
2.851
15
1
60
1
1.0
0
2
1
1
1
setp co LA T Binary z=1.0 log10(M/Msun)=9 nH=3e20
pl eemod
save model ../model_binary_phabs_logm9_z1.0.xcm