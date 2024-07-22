These are response matrices for the LEMA instrument on STROBE-X, with 60 concentrators.

The redistribution matrix is provided by lema_2017-08-11.rmf.
This is the same for any instrument configuration.

The ancillary response file (ARF) contains the effective area vs energy.

For this distribution, we provide lema_60_2023-11-16.arf
This configuration has 60 concentrator units for a total area at 1.5 keV of 1.6 m^2

Lastly, we provide the file lema_nxb_plus_cxb.bkg,
which contains an estimated background spectrum for the LEMA.
This background includes particle backgrounds using a flat spectrum at a rate of 
0.01 cts/sec/keV, as well as a cosmic X-ray background (that comes through the optics)
based on the work of Gupta et al. 2009 (ApJ, 707, 644).

Limitations:

(1) Particle background:

(a) The spectrum is assumed flat (i.e. constant counts/sec/keV)

(b) The spectrum is scaled from an assumed NICER spectrum, without
accounting for the different orbit

(2) Cosmic background:

(a) Includes background from unresolved extragalactic point sources
(AGN), Milky Way Halo (MWH), and Local Hot Bubble (LHB), but not Solar
Wind Charge Exchange

(b) With a small FoV, there can be cosmic variance in the AGN component

(c) The MWH+LHB component is an *average*, *high Galactic latitude*
spectrum, and is not applicable to low latitudes or regions of
enhanced emission (North Polar Spur, etc.).


You should assume there are systematic errors in the background estimation of 
something like 1%. 

Please report any questions or problems with these files!

-- Zaven Arzoumanian <zaven.arzoumanian-1@nasa.gov>
