import numpy as np

G = 6.67e-11 #Newtons kg-2 m2.
c = 299792458 #m/s
Msun = 1.989e30 #kg


def grav_radius(mass):
    return G*mass/c**2

def rms_real_units(spin, mass): #spin here is the unitless -1<a<1 value
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