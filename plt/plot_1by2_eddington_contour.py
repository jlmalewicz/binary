'''
2 by 2 grid contour plot of logxi for both 1 and 2
as a function of mass ratio (q) and at what value 
we have set the limiting Eddington ratio
'''

import matplotlib.pyplot as plt
import numpy as np
import accretion_definitions as acc

clabels = False

fixed_lambda_value = np.logspace(-2,0,50)

q = np.logspace(-1.58, 0, num=50)
# Farris+2014 uses values of q between 0.026 and 1
M = 1e7 #Msun

Q,L = np.meshgrid(q, fixed_lambda_value)

fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(12,5), layout='constrained')

Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = acc.get_all_mdot('total', L, Q, M)


loglambdamin=np.log10(0.01)#(min(lambda_1.min(), lambda_2.min()))
loglambdamax=np.log10(1.28)#(max(lambda_1.min(), lambda_2.max()))

lambda_levels= np.array([0.01, 0.01414214, 
                         0.02, 0.02828427, 
                         0.04, 0.05656854,
                         0.08, 0.11313708, 
                         0.16, 0.22627417,
                         0.32, 0.45254834, 
                         0.64, 0.8,
                         1.0]) 

loglambda_levels = np.asarray([np.log10(x) for x in lambda_levels])



lambda_ticks = ['{:.2g}'.format(10**x) for x in list(loglambda_levels)]

CS11 = ax1.contourf(Q, L, np.log10(lambda_1), cmap='magma', levels=loglambda_levels, vmin=-2, vmax=0, extend='both')


CS21 = ax2.contourf(Q, L, np.log10(lambda_2), cmap='magma',  levels=loglambda_levels, vmin=-2, vmax=0, extend='both')
if clabels == True:
    loglambda_levels_8 = np.asarray([np.log10(x) for x in [0.01,0.02,0.04,0.08,0.16,0.32,0.64,1.0]])
    greys_value = [1.0,0.95,0.9,0.88,0.35,0.3,0.2,0.1]
    greys = [str(gray) for gray in greys_value]
    CT1 = ax1.contour(Q, L, np.log10(lambda_1), levels = loglambda_levels_8, linewidths=1, linestyles='--', colors=greys)
    def fmt(x):
        return '{:.2g}'.format(10**x)
    ax1.clabel(CT1,colors=greys,fontsize=12,fmt=fmt,manual = [(0.7, 0.012), (0.7, 0.024), (0.7, 0.0472), (0.7, 0.0977), (0.7,0.1949), (0.7,0.3935), (0.7,0.7760)])

    CT2 = ax2.contour(Q, L, np.log10(lambda_2), levels = loglambda_levels_8, linewidths=1, linestyles='--', colors=greys)
    ax2.clabel(CT2,colors=greys,fontsize=12,fmt=fmt,manual = [(0.7, 0.012), (0.7, 0.024), (0.7, 0.0472), (0.7, 0.0977), (0.7,0.1949), (0.7,0.3935), (0.7,0.7760)])


cb2 = fig.colorbar(CS21, ax=ax2)
cb2.ax.set_yticklabels(lambda_ticks, fontsize=12)
    
    
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

ax1.set_title(r'Eddington ratio $\lambda_1$')
ax2.set_title(r'Eddington ratio $\lambda_2$')

plt.show()