'''
This script compares the behaviour of eddington ratio and mass accretion 
rate for BH binaries depending on whether we limit the rate of accretion 
on the (a) whole system, or (b) the secondary BH
'''

import numpy as np
import matplotlib.pyplot as plt
import accretion_definitions as acc

##########
# uncomment for the plots you want
##########
plot = 'edd'
#plot = 'm_dot'
#plot = 'mass'
###########

M = 1e7 #Msun

q = np.linspace(0.01,1, num = 100)

m1 = M / (1+q)
m2 = q * M / (1+q)

f = acc.relative_accretion(q)

# (a) fix lambda tot = 10%

a_lambda_tot = 0.02 * np.ones_like(q)
a_M_dot = a_lambda_tot * 3/1e8 * M

a_m1_dot = a_M_dot / (1+f)
a_lambda_1 = a_m1_dot / (3/1e8 * m1)


a_m2_dot = f * a_M_dot / (1+f)
a_lambda_2 = a_m2_dot / (3/1e8 * m2)


# (b) fix lambda_2 = 10%

b_lambda_2 = 0.5 * np.ones_like(q)
b_m2_dot = b_lambda_2 * 3/1e8 * m2

b_m1_dot = b_m2_dot / f
b_lambda_1 = b_m1_dot / (3/1e8 * m1)

b_M_dot = b_m2_dot + b_m1_dot
b_lambda_tot = b_M_dot / (3/1e8 * M)


if plot == 'edd': 
    fig1, (axa, axb) = plt.subplots(1,2)

    axa.plot(q, a_lambda_1, label = r'$m_1$', c='blue')
    axa.plot(q, a_lambda_2, label = r'$m_2$', c = 'red')
    axa.plot(q, a_lambda_tot, label = r'$M = m_1 + m_2$', c = 'purple')

    axa.plot(q, np.ones_like(q), '--', c = 'grey')

    axa.set_yscale('log')

    axa.set_title(r'Eddington ratio if $\lambda_{\rm tot}$ is fixed')
    axa.set_xlabel(r"$q$ $[m_2/m_1]$")
    axa.set_ylabel(r"Eddington ratio $\lambda = \dot{m}/\dot{m}_{\rm Edd}$")
    axa.legend(loc = 'best')


    axb.plot(q, b_lambda_1, label = r'$m_1$', c='blue')
    axb.plot(q, b_lambda_2, label = r'$m_2$', c = 'red')
    axb.plot(q, b_lambda_tot, label = r'$M = m_1 + m_2$', c = 'purple')

    axb.plot(q, np.ones_like(q), '--', c = 'grey')

    axb.set_title(r'Eddington ratio if $\lambda_{2}$ is fixed')
    axb.set_yscale('log')
    axb.set_xlabel(r"$q$ $[m_2/m_1]$")
    axb.legend(loc = 'best')

    plt.show()

elif plot == 'm_dot':
    fig1, (axa, axb) = plt.subplots(1,2)

    axa.plot(q, a_m1_dot, label = r'$m_1$', c='blue')
    axa.plot(q, a_m2_dot, label = r'$m_2$', c = 'red')
    axa.plot(q, a_M_dot, label = r'$M = m_1 + m_2 = 10^7 M_\odot$', c = 'purple')

    axa.set_title(r'Mass accretion rates if $\lambda_{\rm tot}$ is fixed')
    axa.set_xlabel(r"$q$ $[m_2/m_1]$")
    axa.set_ylabel(r"$\dot{m}$ $[M_\odot \cdot {\rm yr}^{-1}]$")
    axa.legend(loc = 'best')


    axb.plot(q, b_m1_dot, label = r'$m_1$', c='blue')
    axb.plot(q, b_m2_dot, label = r'$m_2$', c = 'red')
    axb.plot(q, b_M_dot, label = r'$M = m_1 + m_2 = 10^7 M_\odot$', c = 'purple')

    axb.set_title(r'Mass accretion rates if $\lambda_{2}$ is fixed')
    axb.set_xlabel(r"$q$ $[m_2/m_1]$")
    axb.legend(loc = 'best')

    plt.show()

elif plot == 'mass':
    plt.plot(q, m1, label = r'$m_1$', c='blue')
    plt.plot(q, m2, label = r'$m_2$', c = 'red')
    plt.plot(q, M * np.ones_like(q), label = r'$M = m_1 + m_2 = 10^7 M_\odot$', c = 'purple')
    plt.legend(loc = 'best')

    plt.xlabel(r"$q$ $[m_2/m_1]$")
    plt.ylabel(r"Mass $[M_\odot]$")
    plt.title(r"Mass of each black hole as a function of $q$")

    plt.show()