import matplotlib.pyplot as plt
import numpy as np
import bin.accretion_definitions as accdef


fixed_lambda_value = 0.1


q = np.logspace(-2, 0, num=50)
M = 1e7 #Msun


fig, [[ax1a, ax1b], [ax2a, ax2b]] = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10,7))
ax1a_xi = ax1a.twinx()
ax1b_xi = ax1b.twinx()
ax2a_xi = ax2a.twinx()
ax2b_xi = ax2b.twinx()

for fixed_lambda in ['total', 'secondary']:
    
    Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2 = accdef.get_all_mdot(fixed_lambda, fixed_lambda_value, q, M)
    
    xi_1 = np.ones_like(q)
    xi_2 = np.ones_like(q)

    if fixed_lambda == 'total':
        for i in np.arange(len(q)):
            xi_1[i] = accdef.get_xi(height=10, spin=0.99, lambda_edd=lambda_1[i])
            xi_2[i] = accdef.get_xi(height=10, spin=0.99, lambda_edd=lambda_2[i])
        ax1,ax1_xi,ax2,ax2_xi = ax1a,ax1a_xi,ax2a,ax2a_xi

    elif fixed_lambda == 'secondary':
        xi_2 = xi_2 * accdef.get_xi(height=10, spin=0.99, lambda_edd=lambda_2[0])
        for i in np.arange(len(q)):
            xi_1[i] = accdef.get_xi(height=10, spin=0.99, lambda_edd=lambda_1[i])
        ax1,ax1_xi,ax2,ax2_xi = ax1b,ax1b_xi,ax2b,ax2b_xi

    ax1.plot(q, lambda_1, label = r'$\lambda_1$', c = 'blue')
    ax1.set_yscale('log')
    ax1.set_ylim(5e-4,11)
    ax1_xi.plot(q, np.log10(xi_1), label = r'log$_{10}$ $\xi_1$', c = 'blue', ls = '--')
    ax1_xi.set_ylim(-5,10)

    ax2.plot(q, lambda_2, label = r'$\lambda_2$', c = 'red')
    ax2.set_yscale('log')
    ax2.set_ylim(5e-4,11)
    ax2_xi.plot(q, np.log10(xi_2), label = r'log$_{10}$ $\xi_2$', c = 'red', ls = '--')
    ax2_xi.set_ylim(-5,10)
    


for ax in (ax2a,ax2b):
    ax.set(xlabel=r"Mass ratio $q$ $[m_2/m_1]$")
for ax in (ax1a,ax2a):
    ax.set(ylabel=r"Eddington ratio $\lambda$")
    ax.legend(loc='lower right')
for ax in (ax1b_xi,ax2b_xi):
    ax.set(ylabel='Ionization')
    ax.legend(loc='lower right')



ax1a.set_title(r"(a) fix $\dot{M}$ = "+str(fixed_lambda_value)+r"$\dot{M}_{\rm Edd}$")
ax1b.set_title(r"(b) fix $\dot{m}_2$ = "+str(fixed_lambda_value)+r"$\dot{m}_{2,{\rm Edd}}$")

plt.tight_layout()
plt.show()