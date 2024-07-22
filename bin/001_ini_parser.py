import configparser
import definitions as eq
import accretion_definitions as acc
import numpy as np
import json

Msun = 1.989e30 #kg
c    = 299792458 #m/s

config = configparser.ConfigParser()
config.read('000_params.ini')

params   = config['parameters']
flags    = config['flags']
settings = config['settings']
xspec    = config['xspec']

##############
# PARAMETERS #
##############


q = float(params['q'])
M = float(params['M']) * Msun
sep   = float(params['sep'])   * eq.grav_radius(M)
incl  = float(params['incl'])  * np.pi/180
phase = float(params['phase']) * np.pi/180
spin1, spin2     = float(params['spin1']),   float(params['spin2'])
height1, height2 = float(params['height1']), float(params['height2'])
lambda_tot = float(params['lambda_tot'])


m1 = M / (1+q)
m2 = q * m1

rin1, rin2 = eq.rms_real_units(spin1, m1), eq.rms_real_units(spin2, m2)
rg1, rg2   = eq.grav_radius(m1), eq.grav_radius(m2)

_,_,_, lambda_1, _, lambda_2 = acc.get_all_mdot('total', lambda_tot, q, M)



#############
# COMPUTING #
#############


# outer radius
if flags['truncate'] == 'pichardo':
    rout1, rout2 = eq.truncated_rout(sep, q)
elif flags['truncate'] == 'roche':
    rout1, rout2 = eq.roche_lobe(sep,q)
else:
    raise Exception("Error with truncate flag")


# relative norms: mass accretion
if flags['norm_relative_mdot']:
    mdot1, mdot2 = 1, acc.relative_accretion(q)
else:
    mdot1, mdot2 = 1, 1
# relative norms: emitting area
if flags['norm_relative_area']:
    area1, area2 = eq.relative_area(rin = [rin1, rin2], rout = [rout1, rout2])
else:
    area1, area2 = 1, 1

# Ionization
xi_1 = acc.get_xi(height1,spin1,loglambda_edd=np.log10(lambda_1), relxill_bound=True )
xi_2 = acc.get_xi(height1,spin2,loglambda_edd=np.log10(lambda_2), relxill_bound=True )

# radial doppler
v1, v2 = eq.velocities(M, mass_ratio=q, sep=sep)
z1, z2 = eq.redshift(v1, phase, incl), eq.redshift(v2, phase, incl)

#############
# UTILITIES #
#############

# plot color scheme
if settings['colors']   == 'brp':
    colors            = ['blue', 'red', 'purple']
elif settings['colors'] == 'cold':
    colors            = ['#96C3CE', '#82D173', '#4C6663']
elif settings['colors'] == 'warm':
    colors            = ['#EFC11A', '#FF8966', '#63372C']
elif settings['colors'] == 'magma':
    colors            = ['#FF8762', '#862984','#160f3b']
elif settings['colors'] == 'pastel':
    colors            = ['#DA674D', '#1AAD85','k']
elif settings['colors'] == 'primary':
    colors            = ['#FFBB19', '#E81034','#3209C2']
else:
    raise Exception("Error with colors settings")

# filenames
if settings['filename'] == 'default':
    q_str = '{:.1f}'.format(q)
    l_tot_str = '{:.2f}'.format(lambda_tot)

    phase_str = ''
    if not phase == 0 :
        phase_str = '_phase_{:.0f}'.format(phase/(np.pi/180))

    focus_str = ''
    if settings['focus'] == 'feka' :
        focus_str = 'feka_'

    filename = focus_str+'q_'+q_str+'_l_total_'+l_tot_str+phase_str
else:
    filename = settings['filename']





#############
# SAVE DATA #
#############


data = {
        "total mass"  : M, #kg
        "mass ratio"  : q,
        "height"      : [height1, height2], #rg
        "mass"        : [m1, m2], #kg
        "rg"          : [rg1, rg2], #m
        "spin"        : [spin1, spin2],
        "rin"         : [rin1, rin2],
        "rout"        : [rout1, rout2],
        "area"        : [area1, area2],
        "mdot"        : [mdot1, mdot2],
        "logxi"       : [np.log10(xi_1), np.log10(xi_2)],
        "eddratio"    : [lambda_1, lambda_2, lambda_tot],
        "velocity"    : [v1, v2],
        "redshift"    : [z1, z2],
        "phase"       : params['phase'],

        "settings:colors"      : colors,
        "settings:filename"    : filename,
        "settings:fontsize"    : settings['fontsize'],
        "settings:linewidth"   : settings['linewidth'],
        "settings:imageloc"    : settings['imageloc'],
        "settings:savefig"     : settings['save_plot'],
        "settings:focus"       : settings['focus'],
        "settings:lim"         : [float(x) for x in list(settings["lim"].split(","))],

        "xspec:energylim"  : [float(x) for x in list(xspec["xspec_energy_lim"].split(","))],
        "xspec:instrument" : xspec["instrument"]

        }

with open('dat_'+filename+'.json', 'w') as f:
    json.dump(data, f, indent = 4)
    print('Data saved successfully to '+filename)