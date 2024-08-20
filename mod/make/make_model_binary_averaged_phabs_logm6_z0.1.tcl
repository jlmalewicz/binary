cpd /xs
lmod relxill /home/jlmalewicz/Work/relxill/.
model const*phabs*(cflux*(zashift*relxilllpCp + zashift*relxilllpCp + zashift*relxilllpCp +zashift*relxilllpCp) + cflux*(zashift*relxilllpCp + zashift*relxilllpCp + zashift*relxilllpCp + zashift*relxilllpCp))
# const
0.25
# phabs
0.03
# 1 :     Emin, Emax,lg10Flux
2
10
-13.88
# 1)0 :   Redshift
-0.001
# 1)0 :   Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
# 1)90 :  Redshift
0.023
# 1)90 :  Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
# 1)180 : Redshift
-0.001
# 1)180 : Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
# 1)270 : Redshift
-0.024
# 1)270 : Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
# 2 :     Emin, Emax,lg10Flux
2
10
-13.89
# 2)0 :   Redshift
-0.001
# 2)0 :   Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
# 2)90 :  Redshift
-0.027
# 2)90 :  Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
# 2)180 : Redshift
-0.001
# 2)180 : Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
# 2)270 : Redshift
0.026
# 2)270 : Incl, a, Rin, Rout, h, beta, gamma, logxi, logN, Afe, kTe, refl_frac, z, iongrad_index, iongrad_type, switch_returnrad, switch_reflfrac_boost, norm
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
0.1
0
2
1
1
1
setp co LA T Binary z=0.1 log10(M/Msun)=6 averaged 0,90,180,270, abs nH=3e20
pl eemod
save model ../model_binary_averaged_phabs_logm6_z0.1.xcm