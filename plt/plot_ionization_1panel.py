import matplotlib.pyplot as plt
import numpy as np
import subprocess
import accretion_definitions as accdef


fixed_lambda = 'total'
#fixed_lambda = 'secondary'


q = np.logspace(-2, 0, num=50)
M = 1e7 #Msun


m1 = M / (1+q)
m2 = q * M / (1+q)

f = accdef.relative_accretion(q)

if fixed_lambda == 'total':
    lambda_tot = 0.1 * np.ones_like(q)
    Mdot       = lambda_tot * (3e-8 * M)

    m1dot      = Mdot / (1+f)
    lambda_1   = m1dot / (3e-8 * m1)

    m2dot      = f * m1dot
    lambda_2   = m2dot / (3e-8 * m2)


elif fixed_lambda == 'secondary':
    lambda_2   = 0.1 * np.ones_like(q)
    m2dot      = lambda_2 * (3e-8 * m2)

    m1dot      = m2dot / f
    lambda_1   = m1dot / (3e-8 * m1)

    Mdot       = m2dot + m1dot
    lambda_tot = Mdot / (3e-8 * M)

xi_1 = np.ones_like(q)
xi_2 = np.ones_like(q)

#subprocess.run(["gcc -o xivsrad_h-a-lambda xivsrad_h-a-lambda.c complex.c", "-lm"], cwd="/home/jlmalewicz/Work/accretion/ballantyne")

if fixed_lambda == 'total':
    for i in np.arange(len(q)):
        xi_1[i] = accdef.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i]))
        xi_2[i] = accdef.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[i]))

elif fixed_lambda == 'secondary':
    xi_2 = xi_2 * accdef.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_2[0]))
    for i in np.arange(len(q)):
        xi_1[i] = accdef.get_xi(height=10, spin=0.99, loglambda_edd=np.log10(lambda_1[i]))

plt.plot(q, np.log10(xi_1), label = r'$m_1$', c='blue')
plt.plot(q, np.log10(xi_2), label = r'$m_2$', c = 'red')

#plt.yscale('log')

plt.xlabel(r"Mass ratio $q$ $[m_2/m_1]$")
plt.ylabel(r"Ionization log $\xi$")
plt.title(r"Ionization vs. mass ratio if "+fixed_lambda+r" $\lambda_{\rm Edd}$ is fixed")
plt.legend(loc = 'best')

plt.show()
        






