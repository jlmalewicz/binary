set xs_return_result 1

gets stdin mission
gets stdin texp

gets stdin logm
gets stdin z
gets stdin averaged
gets stdin phabs
gets stdin rebin

if {$averaged eq "y"} {
    set optional_a "(averaged)"
} else {
    set optional_a ""
}

if {$phabs eq "y"} {
    set optional_p "nH=3e20"
} else {
    set optional_p ""
}

if {$rebin eq "n"} {
    set optional_r ""
} else {
    set optional_r " (rebin $rebin)"
}

if {$mission eq "athena"} {
    mo phabs*relxill
    #       1: nH [10^22]
    0.03 -1
    #       2: Index1
    3 -1
    #       3: Index2
    3 -1
    #       4: Rbr
    15 -1
    #       5: a
    0.998
    #       6: Incl [deg]
    30 -1
    #       7: Rin
    -1 -1
    #       8: Rout
    400 -1
    #       9: z
    $z -1
    #      10: gamma
    2
    #      11: logxi
    3.1
    #      12: Afe
    1
    #      13: Ecut [keV]
    300 -1
    #      14: refl_frac
    3
    #      15: norm
    1
} else {
    mo const*phabs*relxill
    #       1: const
    1 -1
    #       2: nH [10^22]
    0.03 -1
    #       3: Index1
    3 -1
    #       4: Index2
    3 -1
    #       5: Rbr
    15 -1
    #       6: a
    0.998
    #       7: Incl [deg]
    30 -1
    #       8: Rin
    -1 -1
    #       9: Rout
    400 -1
    #      10: z
    $z -1
    #      11: gamma
    2
    #      12: logxi
    3.1
    #      13: Afe
    1
    #      14: Ecut [keV]
    300 -1
    #      15: refl_frac
    3
    #      16: norm
    1
    #      17: constant (for spectrum #2)
    1
    #   18-32: =spectrum #1
    =p2
    =p3
    =p4
    =p5
    =p6
    =p7
    =p8
    =p9
    =p10
    =p11
    =p12
    =p13
    =p14
    =p15
    =p16

    thaw 17
}

setp co LA T $mission t=$texp ks || z=$z log10(M/Msun)=$logm $optional_a || $optional_p $optional_r
query y
fit
pl ld del