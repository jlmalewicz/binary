Version 2024-02-28

This directory contains response matrices and background spectra for
the HEMA instrument on STROBE-X.

There are two sets of files, each providing a redistribution matrix
(.rmf), ancillary response file (.arf) and background spectrum (.bkg).
These files can be used in XSPEC to generate simulated spectra of
sources, as observed with HEMA.  The energy resolution of HEMA
is a function of temperature and radiation dose (thus time into mission).

The ones with "300eV" in the name assume a nominal resolution of 300
eV at 6.4 keV. This is the baseline resolution requirement for HEMA
and is appropriate for all observations early in the mission. By end
of life (EOL), this is appropriate for all observations in the main Field of
Regard (FoR) covering Sun angles of 60-140 degrees (63% of the sky),
where the detectors can be kept cool enough to meet the 300 eV
requirement.

The set with "500eV" in the name assume a resolution of 500 eV at 6.4
keV. These are appropriate for observations late in the mission in the
"Extended Field of Regard (eFoR)", which at EOL covers Sun angles of
45-60 degrees and 140-180 degrees.

The contact points for questions are:

Alessandra De Rosa <alessandra.derosa@inaf.it>
Riccardo Campana <riccardo.campana@inaf.it>
Paul Ray <paul.s.ray3.civ@us.navy.mil>
