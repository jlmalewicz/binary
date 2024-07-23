'''
UTILS:
find_nearest

get_xi_from_xivsrad (obsolete)
get_xi
get_all_mdot

rms
relative_accretion
bolometric_correction (already in xivsedd.c)
'''


import pandas as pd
import numpy as np
import subprocess
from os.path import isfile

path_to_ion = '~/work/gatech/binaryspectrum/ion/'

G = 6.67e-11 #Newtons kg-2 m2.
c = 299792458 #m/s
Msun = 1.989e30 #kg


def grav_radius(mass):
    '''
    Computes gravitational radius for input mass

            Parameters:
                    M (float): Mass [kg]

            Returns:
                    grav_radius (float): Gravitational radius [m]
    '''
    return G*mass/c**2

def rms_real_units(spin, mass):
    '''
    Returns radius of marginal stability (or ISCO) for a spinning black hole

            Parameters:
                    spin (float): unitless value for spin (-1<a<1)
                    mass (float): mass of black hole [kg]

            Returns:
                    binary_sum (str): Binary string of the sum of a and b
    '''
    z1 = 1 + (1 - spin**2)**(1/3) * ((1 + spin)**(1/3) + (1 - spin)**(1/3))
    z2 = np.sqrt(3 * spin**2 + z1**2)
    r_ms = G*mass/c**2 * (3 + z2 + np.sign(-spin) * np.sqrt( (3 - z1) * (3 + z1 + 2*z2) ) )
    return r_ms

def roche_lobe(sep,mass_ratio):
    RL2 = sep * 0.49*mass_ratio**(2/3) / (0.6*mass_ratio**(2/3) + np.log(1 + mass_ratio**(1/3)))
    mass_ratio = 1/mass_ratio
    RL1 = sep * 0.49*mass_ratio**(2/3) / (0.6*mass_ratio**(2/3) + np.log(1 + mass_ratio**(1/3)))
    return RL1, RL2

def truncated_rout(sep,mass_ratio):
    RL1, RL2 = roche_lobe(sep, mass_ratio)
    Rout1 = 0.733 * (mass_ratio/(1+mass_ratio))**(0.07) * RL1
    Rout2 = 0.733 * (mass_ratio/(1+mass_ratio))**(0.07) * RL2
    return Rout1, Rout2

# ccw
def velocities(M, sep, mass_ratio):
    v = np.sqrt(G * M / sep)
    return -mass_ratio/(1+mass_ratio) * v, 1/(1+mass_ratio) * v


def redshift(velocity, phase, incl): #gets us z
    num = np.sqrt(1-(velocity/c)**2)
    den = 1 + np.sin(incl) * np.sin(phase) * velocity / c
    return num/den - 1 

def relative_area(rin, rout):
    area1 = np.pi * (rout[0]**2 - rin[0]**2)
    area2 = np.pi * (rout[1]**2 - rin[1]**2)
    return 1, area2/area1

def find_corresponding_y_lim(xx, y1, y2, y1y2, xmin, xmax):
    idx_min = np.abs(np.asarray(xx) - xmin).argmin()
    idx_max = np.abs(np.asarray(xx) - xmax).argmin()

    ymin = min([np.min(np.asarray(y1)[idx_min:idx_max]),
                np.min(np.asarray(y2)[idx_min:idx_max])])

    ymax = max(np.asarray(y1y2)[idx_min:idx_max])

    return 0.9*ymin, 1.1*ymax

def find_nearest(array1, array2, value1):
    '''
    f(x) = y
    x = array1
    y = array2

    finds y_i corresponding to a given x_i    
    '''
    array1 = np.asarray(array1)
    idx = (np.abs(array1 - value1)).argmin()
    return array2[idx]

def rms(spin): 
    '''
    spin here is the unitless -1<a<1 value
    output in units of rg
    '''
    z1 = 1 + (1 - spin**2)**(1/3) * ((1 + spin)**(1/3) + (1 - spin)**(1/3))
    z2 = np.sqrt(3 * spin**2 + z1**2)
    r_ms = (3 + z2 + np.sign(-spin) * np.sqrt( (3 - z1) * (3 + z1 + 2*z2) ) )
    return r_ms

def relative_accretion(mass_ratio, shift_to_1=True):
    '''
    From Kelley+2019
    INPUT:  q = m2/m1, 
            shift_to_1=True shifts it slightly so f(1)=1
    OUTPUT: f = m2dot/m1dot
    '''
    
    q = mass_ratio
    if shift_to_1:
        shift = 0.08680971371929458
    else:
        shift = 0
    return shift + q**(-.25) * np.exp(-0.1/q) + 50/((12*q)**3.5 + (12*q)**(-3.5))

def get_xi_from_xivsrad(height, spin, lambda_edd):
    '''
    Run xivsrad to get log(xi) at (11/9)^2 * rin
    Now obsolete
    '''
    lambda_edd = ('{:.3f}'.format(lambda_edd))

    subprocess.run([path_to_ion+"xivsrad_h-a-lambda", str(height), str(spin), str(lambda_edd)])

    rin      = rms(spin)

    filename = "xiLedd_h"+str(height)+"_a"+str(spin)+"_edd"+str(lambda_edd)+".dat"

    data     = pd.read_table(filename, names = ['r', 'xi'])
    xi_max   = find_nearest(data.r, data.xi, (11/9)**2 * rin)

    return xi_max


def get_xi(height, spin, loglambda_edd, relxill_bound=False):
    filename = path_to_ion+"ximaxvsedd_h"+str(height)+"_a"+str(spin)+".dat"

    if not isfile(filename):
        subprocess.run([path_to_ion+"xivsedd", str(height), str(spin)])
    
    data = pd.read_table(filename, names = ['loglambda', 'xi'])

    xi_max = find_nearest(data.loglambda, data.xi, loglambda_edd)

    if relxill_bound:
        if xi_max > 10**4.7:
            xi_max = 10**4.7
        elif xi_max < 1:
            xi_max = 1

    return xi_max




def get_all_mdot(fixed_lambda_tot, q, M):
    '''
    Returns m1,m2 and all mdots & lambdas for the system (1, 2, and total)

            Parameters:
                    fixed_lambda_tot (float)
                    q (float): mass ratio m2/m1 where m1>m2
                    M (float): total mass (only for mdot to be in corresponding physical unit)

            Returns:
                    m1, m2, Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2
    '''    
    f = relative_accretion(q)

    m1 = M / (1+q)
    m2 = q * M / (1+q)


    lambda_tot = fixed_lambda_tot * np.ones_like(q)
    Mdot       = lambda_tot * (3e-8 * M)

    m1dot      = Mdot / (1+f)
    lambda_1   = m1dot / (3e-8 * m1)

    m2dot      = f * m1dot
    lambda_2   = m2dot / (3e-8 * m2)

    return m1,m2,Mdot, lambda_tot, m1dot, lambda_1, m2dot, lambda_2


def bolometric_correction(func, mass=1e7, eddratio=1.0):
    '''
    Uses empirical fitting formula to output f_x, or
    the fraction of the total bolometric luminosity
    that is emitted as X-ray

    Source: Duras+2020

    INPUTS:

    -- func --
    Specify whether to use Eddington ratio ('eddratio'),
    or black hole mass in M_sun ('mass')

    -- mass --
    in M_sun

    -- eddratio --

    OUTPUTS:

    -- fx --
    Bolometric flux / X-ray flux
    fx * Lbol = Lx
    '''
    if func == 'mass':
        temp = np.log10(mass)
        a = 16.75
        b = 9.22
        c = 26.14
    elif func == 'eddratio':
        temp = eddratio
        a = 7.51
        b = 0.05
        c = 0.61
    else:
        print("func can only be mass or eddratio")
    
    kx = a * (1 + (temp/b)**c) # type: ignore
    
    return 1/kx


