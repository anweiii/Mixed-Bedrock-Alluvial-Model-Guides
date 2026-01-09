from SetupSSPM import TestSSPM
import DictionariesSSPM as td
import os
import numpy as np

# Changes 4/10: plotty time, added final ss in setupsspm, which just plot the last timestep
#Added a 10yrs plot to see starting steady state
# got rid of .ooo1 and .00001 final dotted lines
# changed black line to be 50 yrs
run_time = 1000
#ploty_time = run_time # change if you want to plot differently than run time
#plot_times = [10, 500, 1000, 2000, 5000, 10000, 20000, 30000, 50000, 100000]
#plot_times = np.arange(0, ploty_time + 1, ploty_time // 10)  # Use to plot series of time steps
#plot_times[0] = 50  # Use to plot series of time steps
plot_times = [run_time]  # Use to plot one time steps

TestDicts = [td.long_kd_1D_Gh1]
discharge_fields = ["surface_water__discharge"]  # ,"water__unit_flux_in"]  # [\\"surface_water__discharge",
uplifts = [0.00001]  # for block, ramp, this is the higher uplift, 0.0001
uplift_types = ["none"]
save_grid = False
save_figures = False
save_dem = False
save_plot_sets = False  # saves arrays in datasets, scratch, runs slowly
for TestDict in TestDicts:
    directory_name = (f"/Users/anniet/Library/Mobile Documents/com~apple~CloudDocs/Documents/Document"
                      f"s - Annie’s MacBook Pro (2)/Fall 2024/Landlab/code/in_out_landlab/figures/scrat"
                      f"ch/{TestDict["test_name"]}_{run_time}")
    while os.path.isdir(directory_name):
        directory_name += "i"
    if save_figures:
        os.mkdir(directory_name)
    for field in discharge_fields:
        sp_crit = 0.0
        if field == "water__unit_flux_in":
            sp_crit = 0.00
        for uplift_type in uplift_types:
            for uplift in uplifts:
                sspm = TestSSPM(sp_crit=sp_crit, run_time=run_time,
                                solver='adaptive', rock_uplift_rate=uplift, uplift_type=uplift_type,
                                plot_times=plot_times, **TestDict, discharge_field=field, ksn_series=False,
                                qs_plot=False)
                sspm.run_SSPM()
                if save_grid:
                    sspm.save_grid()
                sspm.plot()
                export_name = f"{TestDict["test_name"]}_{uplift_type}"
                sspm.finalize_plots(save=save_figures, directory=directory_name, export_file_name1=export_name,
                                    plot_map=False, plot_channels=False, ksn_map=False, topo_map=False, UA_plot=False,
                                    ksn_profiles=False, ksn_profiles2=False, qsqc=True)
                sspm.print_nodes()
                #sspm.plot_map()
                if save_dem:
                    sspm.export_grid()
                if save_plot_sets:
                    sspm.save_plot_sets()


