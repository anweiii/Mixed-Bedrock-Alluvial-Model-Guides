##########Original Jupyter Notebook Dictionary#############
TestDict = {
    "test_name": "test1",

    # landscape conditions
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "m_sp": 0.5,
    "n_sp":1,
    "rock_uplift_rate":0.0001,
    "uplift_type": "none", # "none", "linear, "block", or "ramp"
    "sp_crit": 0.0, # threshold
    "discharge_field": "surface_water__discharge", # use "water__unit_flux_in" if varying water discharge

    # grid parameters
    "node_spacing": 10,
    "num_rows": 20,
    "num_cols": 20,

    "timestep": 10.0, # timestep size (yrs) . Lower if encountering chaotic results. Can be increased for lower K values.
    "solver": "basic", # "basic" or "adaptive"
    "starting_grid":"random" # enter name of starting grid without _topo.asc

}
###############random 1D starts###########################
rand_1D_Gh10th = {
    "k_bedrock": 1E-3,
    "k_transport": 1E-2,
    "test_name": "rand_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

rand_1D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "rand_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}
rand_1D_Gh1_kd = {
    "k_bedrock": 1E-3,
    "k_transport": 1E-3,
    "test_name": "rand_1D_Gh1_kd",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}
rand_1D_Gh2 = {
    "k_bedrock": 2E-2,
    "k_transport": 1E-2,
    "test_name": "rand_1D_Gh2",
    "timestep": 3.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}
rand_1D_Gh10_kd = {
    "k_bedrock": 1E-1,
    "k_transport": 1E-2,
    "test_name": "rand_1D_Gh10_kd",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

rand_1D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "rand_1D_Gh10",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

rand_1D_Gh100 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-4,
    "test_name": "rand_1D_Gh100",
    "timestep": 3.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    #"starting_grid": "rand_1D_Gh100__block"
}
###############block 1D starts##########################


block_1D_Gh10th = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "block_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "block_ss_1D_DL_SSPM_Gh10th_6_21_t200000"
}

block_1D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "block_1D_Gh10",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "block_ss_1D_TL_SSPM_Gh10_6_21_t200000"
}
block_1D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "block_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "block_ss_1D_MB_SSPM_Gh1_6_21_t200000"
}
block_1D_Gh1_kd = {
    "k_bedrock": 1E-3,
    "k_transport": 1E-3,
    "test_name": "block_1D_Gh1_kd",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "rand_1D_Gh1_kd__block"
}

block_1D_Gh2 = {
    "k_bedrock": 2E-2,
    "k_transport": 1E-2,
    "test_name": "block_1D_Gh2",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "block_ss_1D_MB_SSPM_Gh2_6_21_t200000"
}


block_1D_Gh10_kd = {
    "k_bedrock": 1E-1,
    "k_transport": 1E-2,
    "test_name": "block_1D_Gh10_kd",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "rand_1D_Gh10_kd__block"
}

block_1D_Gh100 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-4,
    "test_name": "block_1D_Gh100",
    "timestep": 3.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "rand_1D_Gh100__block"
}

###############random 2D starts###########################
rand_2D_Gh10th = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "rand_2D_Gh10th",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}
rand_2D_Gh_1_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.003,
    "test_name": "rand_2D_Gh_1_3",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}
rand_2D_Gh_2_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0015,
    "test_name": "rand_2D_Gh_2_3",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}
rand_2D_Gh_10_kd = {
    "k_bedrock": 0.001,
    "k_transport": 0.0001,
    "test_name": "rand_2D_Gh_10_kd",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"rand_2D_Gh_10_kd__blocki"
}

rand_2D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "rand_2D_Gh1",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}
rand_2D_Gh2 = {
    "k_bedrock": 2E-2,
    "k_transport": 1E-2,
    "test_name": "rand_2D_Gh2",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}
rand_2D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "rand_2D_Gh10",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}
rand_2D_Gh100 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-4,
    "test_name": "rand_2D_Gh100",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}
###############2D starts###########################
_2D_Gh10th = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "2D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"rand_2D_Gh10th__block"
}
_2D_Gh10th_test = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "2D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 10,
    "num_cols": 10,
    #"starting_grid":"2D_Gh10th__None"
}
_2D_Gh_1_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.003,
    "test_name": "2D_Gh_1_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"rand_2D_Gh_1_3__block"
}

_2D_Gh_2_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0015,
    "test_name": "2D_Gh_2_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"rand_2D_Gh_2_3__block"
}

_2D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "2D_Gh1",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"rand_2D_Gh1__block"
}
_2D_Gh2 = {
    "k_bedrock": 2E-2,
    "k_transport": 1E-2,
    "test_name": "2D_Gh2",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"rand_2D_Gh2__block"
}

_2D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "2D_Gh10",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"rand_2D_Gh10__block"
}

_2D_Gh_10_kd = {
    "k_bedrock": 0.001,
    "k_transport": 0.0001,
    "test_name": "rand_2D_Gh_10_kd",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
}

_test2 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "2D_Gh10",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks"
}

################### Himalaya Runs ########################
####### Originally trying to get more himalaya-y parameters, but now I just want to
## have parameters to set up nice figures with uniform K_d values for the paper

him_rand_1D_Gh100th = {
    "k_bedrock": 1E-2,
    "k_transport": 1.0,
    "test_name": "him_rand_1D_Gh100th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 20,
}

him_rand_1D_Gh10th = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-1,
    "test_name": "him_rand_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 1000,
    "num_rows": 3,
    "num_cols": 100,
}
him_rand_1D_Ghthird = {
    "k_bedrock": 1E-2,
    "k_transport": 3E-2,
    "test_name": "him_rand_1D_Ghthird",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}
him_rand_1D_Ghhalf = {
    "k_bedrock": 1E-2,
    "k_transport": 2E-2,
    "test_name": "him_rand_1D_Ghhalf",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}

him_rand_1D_Ghtwothirds = {
    "k_bedrock": 1E-2,
    "k_transport": 1.5E-2,
    "test_name": "him_rand_1D_Ghtwothirds",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}

him_rand_1D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "him_rand_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}

him_rand_1D_Gh2 = {
    "k_bedrock": 1E-2,
    "k_transport": 5E-3,
    "test_name": "him_rand_1D_Gh2",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}
him_rand_1D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "him_rand_1D_Gh10",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}
him_rand_1D_Gh100 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-4,
    "test_name": "him_rand_1D_Gh100",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}


################### 2D Himalaya Runs ########################
####### Originally trying to get more himalaya-y parameters, but now I just want to
## have parameters to set up nice figures with uniform K_d values for the paper

him_rand_2D_Gh100th = {
    "k_bedrock": 1E-2,
    "k_transport": 1.0,
    "test_name": "him_rand_2D_Gh100th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
}

him_rand_2D_Gh10th = {
    "k_bedrock": 1E-1,
    "k_transport": 1E-2,
    "test_name": "him_rand_2D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
}
him_rand_2D_Ghthird = {
    "k_bedrock": 1E-2,
    "k_transport": 3E-2,
    "test_name": "him_rand_2D_Ghthird",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}
him_rand_2D_Ghhalf = {
    "k_bedrock": 1E-2,
    "k_transport": 2E-2,
    "test_name": "him_rand_2D_Ghhalf",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}

him_rand_2D_Ghtwothirds = {
    "k_bedrock": 1E-2,
    "k_transport": 1.5E-2,
    "test_name": "him_rand_2D_Ghtwothirds",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}

him_rand_2D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "him_rand_2D_Gh1",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}

him_rand_2D_Gh2 = {
    "k_bedrock": 1E-2,
    "k_transport": 5E-3,
    "test_name": "him_rand_2D_Gh2",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}
him_rand_2D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "him_rand_2D_Gh10",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}
him_rand_2D_Gh100 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-4,
    "test_name": "him_rand_2D_Gh100",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 1000,
}

#################Feb Model Tests##############################
#################Feb Model Tests##############################
#################Feb Model Tests##############################
#################Feb Model Tests##############################

feb_rand_1D_Gh100th = {
    "k_bedrock": 1E-2,
    "k_transport": 1.0,
    "test_name": "feb_rand_1D_Gh100th",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    # starting grid feb_rand_1D_Gh100th__block
}

feb_rand_1D_Gh10th = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-1,
    "test_name": "feb_rand_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}
feb_rand_1D_Ghthird = {
    "k_bedrock": 1E-2,
    "k_transport": 3E-2,
    "test_name": "feb_rand_1D_Ghthird",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}
feb_rand_1D_Ghhalf = {
    "k_bedrock": 1E-2,
    "k_transport": 2E-2,
    "test_name": "feb_rand_1D_Ghhalf",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}

feb_rand_1D_Ghtwothirds = {
    "k_bedrock": 1E-2,
    "k_transport": 1.5E-2,
    "test_name": "feb_rand_1D_Ghtwothirds",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}

feb_rand_1D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "feb_rand_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}

feb_rand_1D_Gh2 = {
    "k_bedrock": 1E-2,
    "k_transport": 5E-3,
    "test_name": "feb_rand_1D_Gh2",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}
feb_rand_1D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "feb_rand_1D_Gh10",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}
feb_rand_1D_Gh100 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-4,
    "test_name": "feb_rand_1D_Gh100",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
}


#################Feb Model Tests w starting grids##############################
feb_1D_Gh100th = {
    "k_bedrock": 1E-2,
    "k_transport": 1.0,
    "test_name": "feb_1D_Gh100th",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid":"feb_rand_1D_Gh100th__block"
    # starting grid feb_rand_1D_Gh100th__block
}

feb_1D_Gh10th = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-1,
    "test_name": "feb_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid":"feb_rand_1D_Gh10th__block"
}
feb_1D_Ghthird = {
    "k_bedrock": 1E-2,
    "k_transport": 3E-2,
    "test_name": "feb_1D_Ghthird",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid":""
}
feb_1D_Ghhalf = {
    "k_bedrock": 1E-2,
    "k_transport": 2E-2,
    "test_name": "feb_1D_Ghhalf",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid":""
}

feb_1D_Ghtwothirds = {
    "k_bedrock": 1E-2,
    "k_transport": 1.5E-2,
    "test_name": "feb_1D_Ghtwothirds",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid":""
}

feb_1D_Gh1 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-2,
    "test_name": "feb_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid":"feb_rand_1D_Gh1__block"
}

feb_1D_Gh2 = {
    "k_bedrock": 1E-2,
    "k_transport": 5E-3,
    "test_name": "feb_1D_Gh2",
    "timestep": 10.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": ""
}
feb_1D_Gh10 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-3,
    "test_name": "feb_1D_Gh10",
    "timestep": 1.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "feb_rand_1D_Gh10__block"
}
feb_1D_Gh100 = {
    "k_bedrock": 1E-2,
    "k_transport": 1E-4,
    "test_name": "feb_1D_Gh100",
    "timestep": 1.0,
    "node_spacing": 100,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid":"feb_rand_1D_Gh100__block"
}

############FINAL FIGURES#######################
################2D Random start Final Figure parameters
###############random 2D starts###########################
# kd is always 0.001
final_rand_2D_Gh100th = {
    "k_bedrock": 0.001,
    "k_transport": 0.1,
    "test_name": "final_rand_2D_Gh100th",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
    #"starting_grid":"rand_2D_Gh100th_final__ramp" # starting at 500,000yrs ramp ss
}

final_rand_2D_Gh10th = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "final_rand_2D_Gh10th",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
    #"starting_grid":"rand_2D_Gh10th_final__ramp" # starting at 500,000yrs ramp ss
}

final_rand_2D_Gh_1_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.003,
    "test_name": "final_rand_2D_Gh_1_3",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
    #"starting_grid":"rand_2D_Gh_1_3_final__ramp"  # starting at 500,000yrs ramp ss
}
final_rand_2D_Gh_2_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0015,
    "test_name": "final_rand_2D_Gh_2_3",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    #"starting_grid":"2D_goldilocks_mini"
    "starting_grid":"final_rand_2D_Gh_2_3__block" #starting at 1,000,000yrs
    #"starting_grid":"rand_2D_Gh_2_3_final__ramp" # starting at 500,000yrs ramp ss
}


final_rand_2D_Gh1 = {
    "k_bedrock": 0.001,
    "k_transport": 0.001,
    "test_name": "final_rand_2D_Gh1",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"2D_goldilocks_mini"
    #"starting_grid": "final_rand_2D_Gh1__ramp"  # starting at 1,000,000yrs ramp ss
}
final_rand_2D_Gh2 = {
    "k_bedrock": 0.001,
    "k_transport": 5E-4,
    "test_name": "final_rand_2D_Gh2",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    #"starting_grid":"2D_goldilocks_mini"
    "starting_grid":"final_rand_2D_Gh2__block" # starting at 7 million
    #"starting_grid": "final_rand_2D_Gh2__ramp"  # starting at 1,000,000yrs ramp ss
}
final_rand_2D_Gh10 = {
    "k_bedrock": 0.001,
    "k_transport": 1E-4,
    "test_name": "final_rand_2D_Gh10",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    #"starting_grid":"2D_goldilocks_mini",
    #"starting_grid":"final_rand_2D_Gh10__block" # starting at 5 million yrs
    "starting_grid":"final_rand_2D_Gh10__ramp_new" # starting at 1,000,000 yrs ramp ss
}
final_rand_2D_Gh10_high_k = {
    "k_bedrock": 0.1,
    "k_transport": 1E-2,
    "test_name": "final_rand_2D_Gh10_high_k",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    #"starting_grid":"2D_goldilocks_mini",
    #"starting_grid":"final_rand_2D_Gh10__block" # starting at 5 million yrs
    "starting_grid":"final_rand_2D_Gh10__ramp_new" # starting at 1,000,000 yrs ramp ss
}
final_rand_2D_Gh100 = {
    "k_bedrock": 0.001,
    "k_transport": 1E-5,
    "test_name": "final_rand_2D_Gh100",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    #"starting_grid":"2D_goldilocks_mini",
    #"starting_grid":"final_rand_2D_Gh100__block" # starting at 5,000,000 yrs
    "starting_grid":"final_rand_2D_Gh100__ramp", # starting at 1,000,000 yrs ramp ss
}
##############2D Final starting from block steady state#################
# kd is always 0.001
final_2D_Gh100th = {
    "k_bedrock": 0.001,
    "k_transport": 0.1,
    "test_name": "final_2D_Gh100th",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"final_rand_2D_Gh100th__block"
    #"starting_grid":"rand_2D_Gh100th_final__ramp" # starting at 500,000yrs ramp ss
}

final_2D_Gh10th = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "final_2D_Gh10th",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    #"starting_grid":"final_rand_2D_Gh10th__block"
    "starting_grid":"rand_2D_Gh10th_final__ramp" # starting at 500,000yrs ramp ss
}

final_2D_Gh_1_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.003,
    "test_name": "final_2D_Gh_1_3",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"final_rand_2D_Gh_1_3__block"
    #"starting_grid":"rand_2D_Gh_1_3_final__ramp"  # starting at 500,000yrs ramp ss
}
final_2D_Gh_2_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0015,
    "test_name": "final_2D_Gh_2_3",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"final_rand_2D_Gh_2_3__block"
    #"starting_grid":"rand_2D_Gh_2_3_final__ramp" # starting at 500,000yrs ramp ss
}


final_2D_Gh1 = {
    "k_bedrock": 0.001,
    "k_transport": 0.001,
    "test_name": "final_2D_Gh1",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"final_rand_2D_Gh1__block"
    #"starting_grid": "final_rand_2D_Gh1__ramp"  # starting at 1,000,000yrs ramp ss
}
final_2D_Gh2 = {
    "k_bedrock": 0.001,
    "k_transport": 5E-4,
    "test_name": "final_2D_Gh2",
    "timestep": 20.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"final_rand_2D_Gh2__block"
    #"starting_grid": "final_rand_2D_Gh2__ramp"  # starting at 1,000,000yrs ramp ss
}
final_2D_Gh10 = {
    "k_bedrock": 0.001,
    "k_transport": 1E-4,
    "test_name": "final_2D_Gh10",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    #"starting_grid":"final_rand_2D_Gh10__block",
    #"starting_grid": "final_rand_2D_Gh10__ramp" # starting at 2,000,000 yrs ramp ss
    #"starting_grid":"final_rand_2D_Gh10__block_test_tho" # starting at 2,000,000 yrs ramp ss
    "starting_grid":"final_2D_Gh10__block_new"
}

final_2D_Gh100 = {
    "k_bedrock": 0.001,
    "k_transport": 1E-5,
    "test_name": "final_2D_Gh100",
    "timestep": 50,
    "node_spacing": 20,
    "num_rows": 50,
    "num_cols": 50,
    "starting_grid":"final_2D_Gh100__block_7000000",
    #"starting_grid":"final_2D_Gh100__ramp_3000000", # starting at 3,000,000 yrs ramp ss
    ##"starting_grid":"final_2D_Gh100__ramp__10000000"# starting at 10,000,000 yrs ramp ss, not much better than 3
}




########### 1D FINAL Runs#######
#Kd/kt values are selected for a Keff of .005
final_rand_1D_Gh100th = {
    "k_bedrock": 0.00505,
    "k_transport": 0.505,
    "test_name": "final_rand_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}
final_rand_1D_Gh10th = {
    "k_bedrock": 0.0055,
    "k_transport": 0.055,
    "test_name": "final_rand_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_rand_1D_Gh1_3 = {
    "k_bedrock": 0.006665,
    "k_transport": 0.020015015,
    "test_name": "final_rand_1D_Gh1_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_rand_1D_Gh1_2 = {
    "k_bedrock": 0.0075,
    "k_transport": 0.015,
    "test_name": "final_rand_1D_Gh1_2",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_rand_1D_Gh2_3 = {
    "k_bedrock": 0.008335,
    "k_transport": 0.012496252,
    "test_name": "final_rand_1D_Gh2_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_rand_1D_Gh1 = {
    "k_bedrock": 0.01,
    "k_transport": 0.01,
    "test_name": "final_rand_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_rand_1D_Gh2 = {
    "k_bedrock": 0.015,
    "k_transport": 0.0075,
    "test_name": "final_rand_1D_Gh2",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_rand_1D_Gh10 = {
    "k_bedrock": 0.055,
    "k_transport": 0.0055,
    "test_name": "final_rand_1D_Gh10",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_rand_1D_Gh100 = {
    "k_bedrock": 0.505,
    "k_transport": 0.00505,
    "test_name": "final_rand_1D_Gh100",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    #"starting_grid": "rand_1D_Gh100__block"
}



##############Final runs hold kt################
########### 1D FINAL Runs#######
#Kd/kt values are selected for a Keff of .005
final_kd_rand_1D_Gh100th = {
    "k_bedrock": 0.001,
    "k_transport": 0.1,
    "test_name": "final_kd_rand_1D_Gh100th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}
final_kd_rand_1D_Gh10th = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "final_kd_rand_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh1_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.003,
    "test_name": "final_kd_rand_1D_Gh1_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh1_2 = {
    "k_bedrock": 0.001,
    "k_transport": 0.002,
    "test_name": "final_kd_rand_1D_Gh1_2",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh2_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0015,
    "test_name": "final_kd_rand_1D_Gh2_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh1 = {
    "k_bedrock": 0.001,
    "k_transport": 0.001,
    "test_name": "final_kd_rand_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh2 = {
    "k_bedrock": 0.002,
    "k_transport": 0.001,
    "test_name": "final_kd_rand_1D_Gh2",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh10 = {
    "k_bedrock": 0.01,
    "k_transport": 0.001,
    "test_name": "final_kd_rand_1D_Gh10",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh100 = {
    "k_bedrock": 0.1,
    "k_transport": 0.001,
    "test_name": "final_kd_rand_1D_Gh100",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    #"starting_grid": "rand_1D_Gh100__block"
}


final_kd_rand_1D_Gh10_2 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0001,
    "test_name": "final_kd_rand_1D_Gh10_2",
    "timestep": 50.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
}

final_kd_rand_1D_Gh100_2 = {
    "k_bedrock": 0.001,
    "k_transport": 0.00001,
    "test_name": "final_kd_rand_1D_Gh100_2",
    "timestep": 100.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    #"starting_grid": "rand_1D_Gh100__block"
}


######################################################################################################
####block ss for kd 1d ####################################################################
final_kd_1D_Gh100th = {
    "k_bedrock": 0.001,
    "k_transport": 0.1,
    "test_name": "final_kd_1D_Gh100th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh100th__block"
}
final_kd_1D_Gh10th = {
    "k_bedrock": 0.001,
    "k_transport": 0.01,
    "test_name": "final_kd_1D_Gh10th",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh10th__block"
}

final_kd_1D_Gh1_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.003,
    "test_name": "final_kd_1D_Gh1_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh1_3__block"
}

final_kd_1D_Gh1_2 = {
    "k_bedrock": 0.001,
    "k_transport": 0.002,
    "test_name": "final_kd_1D_Gh1_2",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh1_2__block"
}

final_kd_1D_Gh2_3 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0015,
    "test_name": "final_kd_1D_Gh2_3",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh2_3__block"
}

final_kd_1D_Gh1 = {
    "k_bedrock": 0.001,
    "k_transport": 0.001,
    "test_name": "final_kd_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh1__block"
}

final_kd_1D_Gh2 = {
    "k_bedrock": 0.002,
    "k_transport": 0.001,
    "test_name": "final_kd_1D_Gh2",
    "timestep": 5.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh2__block"
}

final_kd_1D_Gh10 = {
    "k_bedrock": 0.01,
    "k_transport": 0.001,
    "test_name": "final_kd_1D_Gh10",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh10__block"
}

final_kd_1D_Gh100 = {
    "k_bedrock": 0.1,
    "k_transport": 0.001,
    "test_name": "final_kd_1D_Gh100",
    "timestep": 1.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh100__block"
}
# these actually match the 2D model parameters
final_kd_1D_Gh10_2 = {
    "k_bedrock": 0.001,
    "k_transport": 0.0001,
    "test_name": "final_kd_1D_Gh10_2",
    "timestep": 50.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh10_2__block"
}

final_kd_1D_Gh100_2 = {
    "k_bedrock": 0.001,
    "k_transport": 0.00001,
    "test_name": "final_kd_1D_Gh100_2",
    "timestep": 100.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 100,
    "starting_grid": "final_kd_rand_1D_Gh100_2__block"
}

#############big grid
big_grid = {
    "k_bedrock": 0.0001,
    "k_transport": 0.01,
    "test_name": "big_grid",
    "timestep": 100.0,
    "node_spacing": 10,
    "num_rows": 200,
    "num_cols": 100,
    #"starting_grid":"final_rand_2D_Gh10th__block"
    #"starting_grid":"rand_2D_Gh10th_final__ramp" # starting at 500,000yrs ramp ss
}

##############long#############

long_kd_1D_Gh1 = {
    "k_bedrock": 0.001,
    "k_transport": 0.001,
    "test_name": "long_kd_1D_Gh1",
    "timestep": 10.0,
    "node_spacing": 20,
    "num_rows": 3,
    "num_cols": 10000,
    "starting_grid": "longer_kd_1D_Gh1__block"
}