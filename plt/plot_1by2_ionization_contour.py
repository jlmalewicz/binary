'''
2 contour plots of logxi for both 1 and 2
as a function of mass ratio (q) and at what value 
we have set the limiting Eddington ratio
'''

import matplotlib.pyplot as plt
import numpy as np
import accretion_definitions as acc
import matplotlib.colors as colors

fixed_lambda_value = np.logspace(-2,0,50)

q = np.logspace(-1.58, 0, num=50)
# Farris+2014 uses values of q between 0.026 and 1
M = 1e7 #Msun

Q,L = np.meshgrid(q, fixed_lambda_value)

fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(12,5), layout='constrained')

Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = acc.get_all_mdot('total', L, Q, M)
    

xi_1 = np.ones_like(Q)
xi_2 = np.ones_like(Q)

for i in np.arange(len(q)):
    for j in np.arange(len(q)):
        xi_1[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i,j]))
        xi_2[i,j] = acc.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[i,j]))
        
CS1 = ax1.contourf(Q, L, np.log10(xi_1), levels=15, extend='max')
CS2 = ax2.contourf(Q, L, np.log10(xi_2), CS1.levels, extend='max')
cb2=fig.colorbar(CS2, ax=ax2)
    
    
ls = [0.5, 0.5, 0.5, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05]
qs = [0.2, 0.5, 0.9, 0.2, 0.5, 0.9,  0.2,  0.5,  0.9]
ss = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']




for ax in [ax1,ax2]:
    for l,q,s in zip(ls,qs,ss):
        ax.text(q, l, s,color='k', fontsize = 14, ha='center',va='center',bbox=dict(boxstyle="circle", fc='w', linewidth=0, alpha=0.5))
    ax.set_yscale('log')
    ax.set_xlabel(r"Mass ratio ($q = m_2/m_1$)", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
ax1.set_ylabel(r'Total Eddington ratio ($\lambda_{\rm tot}$)', fontsize=12)

ax1.set_title(r'Peak ionization (log $\xi_1$)')
ax2.set_title(r'Peak ionization (log $\xi_2$)')

plt.show()