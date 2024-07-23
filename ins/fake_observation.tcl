set xs_return_result 1
# set folder "/home/jlm/work/gatech/binaryspectrum"
# Note that filenames cannot > 68 chars. if they are to appear in the fakeit file's RESPFILE or ANCRFILE entry
# Given that this script is already in the binaryspectrum/ins/ folder, we set:
set folder "ins/"

while {1} {
    puts -nonewline "Enter mission (strobex, hexp or athena): "
    gets stdin mission

    if {$mission eq "strobex"} {
        puts -nonewline "Enter instrument (LEMA, HEMA300, or HEMA500): "
        gets stdin instrument
        set instrument_string "${instrument}_"
        
        if {$instrument eq "LEMA"} {
            set bkg_loc "${folder}STROBE-X/LEMA60/lema_nxb_plus_cxb.bkg"
            set rmf_loc "${folder}STROBE-X/LEMA60/lema_2017-08-11.rmf"
            set arf_loc "${folder}STROBE-X/LEMA60/lema_60_2023-11-16.arf"
            break ;
        } elseif {$instrument eq "HEMA300"} {
            set bkg_loc "${folder}STROBE-X/HEMA/STROBEX_HEMA_300eV.bkg"
            set rmf_loc "${folder}STROBE-X/HEMA/STROBEX_HEMA_300eV.rmf"
            set arf_loc "${folder}STROBE-X/HEMA/STROBEX_HEMA_300eV.arf"
            break ; 
        } elseif {$instrument eq "HEMA500"} {
            set bkg_loc "${folder}STROBE-X/HEMA/STROBEX_HEMA_500eV.bkg"
            set rmf_loc "${folder}STROBE-X/HEMA/STROBEX_HEMA_500eV.rmf"
            set arf_loc "${folder}STROBE-X/HEMA/STROBEX_HEMA_500eV.arf"
            break ; 
        } else {
           puts "Invalid instrument for mission strobex." 
        }
    } elseif {$mission eq "hexp"} {
        puts -nonewline "Enter instrument (LET or HET): "
        gets stdin instrument
        set instrument_string "${instrument}_"

        if {$instrument eq "LET"} {
            set bkg_loc "${folder}HEX-P/v09_rsp_files/HEXP_LET_v09_L1_R8arcsec.bkg"
            set rmf_loc "${folder}HEX-P/v09_rsp_files/HEXP_LET_v09.rmf"
            set arf_loc "${folder}HEX-P/v09_rsp_files/HEXP_LET_v09_PSFcor.arf"
            break ;
        } elseif {$instrument eq "HET"} {
            set bkg_loc "${folder}HEX-P/v09_rsp_files/HEXP_HET_v09_x2_L1_R18arcsec_Ln25keV.bkg"
            set rmf_loc "${folder}HEX-P/v09_rsp_files/HEXP_HET_v09.rmf"
            set arf_loc "${folder}HEX-P/v09_rsp_files/HEXP_HET_v09_PSFcor_x2.arf"
            break ; 
        } else {
            puts "Invalid instrument for mission hexp."
        } 
    } elseif {$mission eq "athena"} {
        set bkg_loc "${folder}ATHENA/background.pha"
        set rmf_loc "${folder}ATHENA/athena_wfi_rmf_v20230523.rmf"
        set arf_loc "${folder}ATHENA/ancillary.arf"
        set instrument_string ""
        break ;
    } else {
        puts "Invalid mission."
    }
}

gets stdin logm
gets stdin z
gets stdin averaged
gets stdin phabs

gets stdin texp
set texps "${texp}000"

if {$averaged eq "y"} {
    set optional_a "_averaged"
    set optional_title_a "(averaged)"
} else {
    set optional_a ""
    set optional_title_a ""
}

if {$phabs eq "y"} {
    set optional_p "phabs_"
    set optional_title_p "nH=3e20"
} else {
    set optional_p ""
    set optional_title_p ""
}


set fake_file_prefix "${mission}_${instrument_string}${texp}ks_${optional_p}z${z}logm${logm}${optional_a}"
set fake_file  "${fake_file_prefix}.fak"

fakeit ${bkg_loc} & ${rmf_loc} & ${arf_loc} & y & ${fake_file_prefix} & ${fake_file} & ${texps}

setp co LA T $mission t=$texp ks || z=$z log10(M/Msun)=$logm $optional_title_a || $optional_title_p 
pl ld

mv *.fak dat/.