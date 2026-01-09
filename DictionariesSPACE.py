#DL Paper values, same as __init__ values for TestSpace
DL_Paper = {
    "test_name": "DL_Paper",
    "F_f": 1.0,
}

##Shobe Paper TL
TL_Paper = {
    "soil_depth": 100,
    "v_s": 5.0,
    "K_sed": 0.01,
    "K_br": 0.0001,

    "F_f": 0.,
    "test_name": "TL_Paper"
}

##reduce sed to 5
TL_Paper5 = {
    "soil_depth": 100,
    "v_s": 5.0,
    "K_sed": 0.01,
    "K_br": 0.0001,

    "F_f": 0.,
    "test_name": "TL_Paper5"
}

# Shobe Paper Mixed Bedrock
MB_Paper = {
    "v_s": 5.0,  ##K based DL
    "K_sed": 0.01,  ##K based MB
    "K_br": 0.005,  ##K based TL
    "F_f": 0.,
    "test_name": "MB_Paper"  ##
}

###########Values from calculated space notes######################################################

# Mixed, Ks = kd
MB_Notes = {
    "K_sed": 1E-5,
    "K_br": 1E-5,
    "test_name": "MB_Notes",
    "soil_depth": 1.,
    "F_f": 0.,
}

# DL, Kt > Kd means Kbr < Ksed
DL_Notes = {
    "K_sed": 1E-4,
    "K_br": 1E-5,
    "test_name": "DL_Notes",
    "soil_depth": 0.,
    "F_f": 0.,
}

# Making TL from just increasing V
TL_NotesV = {
    "K_sed": 1E-4,
    "K_br": 1E-5,
    "test_name": "TL_NotesV",
    "v_s": 5,
    "soil_depth": 2.,

    "F_f": 0.,
}


# TL, Kt < Kd means Kbr > Ksed
TL_Notes = {
    "K_sed": 1E-5,
    "K_br": 1E-4,
    "test_name": "TL_Notes",
    "soil_depth": 2.,
    "F_f": 0.,
}

# TL, Kt << Kd means Kbr >> Ksed
TL_Notes2 = {
    "K_sed": 1E-5,
    "K_br": 1E-3,
    "test_name": "TL_Notes2",
    "soil_depth": 5.,
    "F_f": 0.,
}
# NOTES WITH K VALUES *100

###########Values from calculated space notes######################################################

# Mixed, Ks = kd
MB_Notes_Large = {
    "K_sed": 1E-3,
    "K_br": 1E-3,
    "test_name": "MB_Notes_Large",
    "soil_depth": 1.,
    "F_f": 0.,
}

# DL, Kt > Kd means Kbr < Ksed
DL_Notes_Large = {
    "K_sed": 1E-2,
    "K_br": 1E-3,
    "test_name": "DL_Notes_Large",
    "soil_depth": 0.,
    "F_f": 0.0,
}

# DL, Kt > Kd means Kbr < Ksed
TL_NotesV_Large = {
    "K_sed": 1E-2,
    "K_br": 1E-3,
    "test_name": "TL_NotesV_Large",
    "v_s": 5.,
    "soil_depth": 0.,
    "F_f": 0.0,
}

# Ff = 1
DL_NotesF_Large = {
    "K_sed": 1E-2,
    "K_br": 1E-3,
    "test_name": "DL_NotesF_Large",
    "soil_depth": 0.,
    "F_f": 1.0,
}
#way lower Kbr
DL_Notes2_Large = {
    "K_sed": 1E-2,
    "K_br": 1E-5,
    "test_name": "DL_Notes2_Large",
    "soil_depth": 0.,
    "F_f": 0.0,
}
# TL, Kt < Kd means Kbr > Ksed
TL_Notes_Large = {
    "K_sed": 1E-3,
    "K_br": 1E-2,
    "test_name": "TL_Notes_Large",
    "soil_depth": 2.,
    "F_f": 0.,
}

# TL, Kt << Kd means Kbr >> Ksed
TL_Notes2_Large = {
    "K_sed": 1E-3,
    "K_br": 1E-1,
    "test_name": "TL_Notes2_Large",
    "soil_depth": 5.,
    "F_f": 0.,
}

# 100m sediment
TL_Notes_100 = {
    "K_sed": 1E-3,
    "K_br": 1E-2,
    "test_name": "TL_Notes_100",
    "soil_depth": 100.,
    "F_f": 0.,
}

#MB, Small kbr, ksed, H values for debugging
#bug only occurs for sets of parameters that include some combination of high H*, high v_s, high Kr, and high Ks
#K_s=0.002, K_r=0.001, H*=0.1, and v_s=5.0
# TL, Kt << Kd means Kbr >> Ksed
MB_small = {

    "K_sed": 0.002,
    "K_br": 0.001,
    "test_name": "MB_small",
    "soil_depth": 1,
    "v_s": 1.0,
    "F_f": 0.,
}

DL_small = {
    "K_sed": 0.02,
    "K_br": 0.001,
    "test_name": "DL_small",
    "soil_depth": 0,
    "v_s": 1.0,
    "F_f": 0.,
}

TL_small = {
    "K_sed": 0.00002,
    "K_br": 0.001,
    "test_name": "TL_small",
    "soil_depth": 1.,
    "v_s": 1.0,
    "F_f": 0.,
}

# V = 5, but changing Ks so that kt/kb (Ks/V/Kb) stays the same as notes large


# DL, Kt > Kd means Kbr < Ksed
DL_V5 = {
    "K_sed": 5E-2,
    "K_br": 1E-3,
    "test_name": "DL_V5",
    "soil_depth": 0.,
    "F_f": 0.0,
    "v_s": 5.,
}

# TL, Kt < Kd means Kbr > Ksed
TL_V5 = {
    "K_sed": 5E-3,
    "K_br": 1E-2,
    "test_name": "TL_V5",
    "soil_depth": 2.,
    "F_f": 0.,
    "v_s": 5.,
}

# Mixed, Ks = kd
MB_V5 = {
    "K_sed": 5E-3,
    "K_br": 1E-3,
    "test_name": "MB_V5",
    "soil_depth": 1.,
    "F_f": 0.,
    "v_s": 5.,
}