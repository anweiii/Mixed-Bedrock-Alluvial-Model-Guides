import os
import matplotlib.pyplot as plt
import numpy as np
from landlab import RasterModelGrid, imshow_grid, imshowhs_grid
from landlab.components import (DepressionFinderAndRouter, ChannelProfiler, SteepnessFinder, FlowAccumulator,
                                ChiFinder, SharedStreamPower, PriorityFloodFlowRouter)
from landlab.io import write_esri_ascii, read_esri_ascii
from matplotlib.gridspec import GridSpec
from landlab.io.netcdf import write_netcdf
from landlab.io.esri_ascii import dump
from matplotlib.colors import ListedColormap
from scipy.special import gamma
#from landlab.components import PrecipitationDistribution

class TestSSPM:
    # instantiate test object
    def __init__(
            self,
        
            # landscape conditions
            k_bedrock=0.01,
            k_transport=0.001,
            F_f=0.,
            m_sp=0.5,
            n_sp=1.0,
            sp_crit=0.,
        
            # Grid info, starting grid, rows, columns, dxy
            starting_grid="random",
            num_rows=10,
            num_cols=10,
            node_spacing=200.0,  # m,
        
            # time parameters, timestep, run time, print time, elapsed time
            # years
            timestep=10.0,
            run_time=1000,  # years
            # Set elapsed time to zero
            elapsed_time=0,
            print_time=1000,

            # Other Parameters
            rock_uplift_rate=1e-4,  # m/yr# Set rock uplift rate
            r=1.,  # m/yr # Define runoff parameter r, where Q=Ar
            test_name="Default",
            uplift_type= False,
            solver='basic',
            plot_times=[],
            discharge_field="surface_water__discharge",
            ksn_series=False,
            qs_plot=False,
    ):
        
        #sets all parameters as a part of test object
        self.ChannelProfiler = None
        self.chi_finder = None
        self.steepness_finder = None
        self.depression_finder = None
        self.flow_accumulator = None
        self.model_grid = None
        self.area = None
        self.slope = None
        self.qs = None
        self.distance_upstream = None
        self.Ksn_vals = None
        self.k_bedrock = k_bedrock
        self.k_transport = k_transport
        self.F_f = F_f
        self.m_sp = m_sp
        self.n_sp = n_sp
        self.sp_crit = sp_crit

        # Grid info, starting grid, rows, columns, dxy
        self.starting_grid = starting_grid
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.node_spacing = node_spacing  # m,

        # time parameters, timestep, run time, print time, elapsed time
        # years
        self.timestep = timestep
        # Set model run time
        self.run_time = run_time  # years
        # Set elapsed time to zero
        self.elapsed_time = elapsed_time
        self.print_time = print_time

        # Other Parameters
        self.rock_uplift_rate = rock_uplift_rate  # m/yr# Set rock uplift rate
        self.r = r  # m/yr # Define runoff parameter r, where Q=Ar
        self.test_name = test_name
        self.uplift_type = uplift_type
        self.export_file_name = (f"{self.test_name}_{self.uplift_type}")
        self.theta = self.m_sp / self.n_sp
        self.solver = solver
        self.plot_times = plot_times
        self.discharge_field = discharge_field
        self.ksn_series = ksn_series
        self.qs_plot = qs_plot

    #returns a string of all parameters used
    def __str__(self):
        return f"""\
        k_bedrock: {self.k_bedrock}
        k_transport: {self.k_transport}
        F_f: {self.F_f}
        m_sp: {self.m_sp}
        n_sp: {self.n_sp}
        sp_crit: {self.sp_crit}
        num_rows: {self.num_rows}
        num_cols: {self.num_cols}
        node_spacing: {self.node_spacing}
        timestep: {self.timestep}
        run_time: {self.run_time}
        elapsed_time: {self.elapsed_time}
        rock_uplift_rate: {self.rock_uplift_rate}
        r: {self.r}
        test_name: 
        {self.test_name}
        uplift_type = {self.uplift_type}
        discharge_field = 
        {self.discharge_field}
        starting_grid: 
        {self.starting_grid}\
        """

    def make_grid(self):
        # make a flat grid with small scale random noise 
        if 'random' == self.starting_grid:
            mg = RasterModelGrid((self.num_rows, self.num_cols), self.node_spacing)
            np.random.seed(0)  # seed set to zero so our figures are reproducible
            mg_noise = np.random.rand(mg.number_of_nodes) / 1000.0  # intial noise on elevation grid
            # set up the elevation on the grid
            zr = mg.add_zeros("topographic__elevation", at="node") #set all topography to zero
            zr += mg_noise # add noise

        else: # load existing grid file (.asc)

            # import starting grid fields
            (grid1, topo) = read_esri_ascii(
                f"output/grids/{self.starting_grid}_topo.asc")

            # make grid and add imported fields
            mg = RasterModelGrid((self.num_rows, self.num_cols), self.node_spacing)
            mg.add_field("topographic__elevation", topo, at="node")


        # SET GRID BOUNDARY CONDITIONS################################################

        # for one left node open:
        #mg.set_watershed_boundary_condition_outlet_id(int(mg.nodes[1, 0]), mg['node']['topographic__elevation'], -9999.)
        # for left border open:
        mg.set_closed_boundaries_at_grid_edges(True, True, False, True)

        # set uplift field
        if self.uplift_type == "linear": #linear gradient from U / 10 at outlet, up to U at the top
            gradient = np.linspace(self.rock_uplift_rate/10, self.rock_uplift_rate, self.num_cols)
            uplift = np.tile(gradient, (self.num_rows, 1))
            mg.add_field("uplift", uplift, at="node", units="-", copy=False, clobber=True)
            #mg['node']['uplift'] += self.rock_uplift_rate + mg.node_x * 1E-5

        elif self.uplift_type == "block": # Left outlet half has U/10, right upstream half has U
            gradient = np.empty(self.num_cols)
            gradient[:self.num_cols // 2] = self.rock_uplift_rate / 100  # left half with 0.01
            gradient[self.num_cols // 2:] = self.rock_uplift_rate  # right half with 0.001
            uplift = np.tile(gradient, (self.num_rows, 1))
            mg.add_field("uplift", uplift, at="node", units="-", copy=False, clobber=True)

        elif self.uplift_type == "ramp": #left half has U/10, right quarter is U, area in between is a linearly increasing ramp
            gradient = np.empty(self.num_cols)
            gradient[:self.num_cols // 2] = self.rock_uplift_rate / 10  # left half with 0.01
            gradient[self.num_cols // 2:] = self.rock_uplift_rate  # right half with 0.001
            gradient_middle = np.linspace(self.rock_uplift_rate/10, self.rock_uplift_rate, self.num_cols // 4)
            gradient[self.num_cols // 2: self.num_cols // 2 + self.num_cols // 4] = gradient_middle
            uplift = np.tile(gradient, (self.num_rows, 1))
            mg.add_field("uplift", uplift, at="node", units="-", copy=False, clobber=True)

        else: #if set to "none", constant uplift throughout area
            mg.add_zeros("uplift", at="node")
            mg['node']['uplift'] += self.rock_uplift_rate

        self.model_grid = mg # set grid as part of test object

    # Instantiate components###################################################
    def instantiate_components(self):

        self.flow_accumulator = FlowAccumulator(self.model_grid, flow_director="D8")
        #self.fr = PriorityFloodFlowRouter(self.model_grid, flow_metric="D8")
        

        if self.discharge_field == "water__unit_flux_in":
            _ = self.model_grid.add_zeros("water__unit_flux_in", at="node", clobber=True) # make new field for water__unit_flux_in
            
        # Instantiate depression finder and router; optional
        self.depression_finder = DepressionFinderAndRouter(self.model_grid)
        self.steepness_finder = SteepnessFinder(self.model_grid, reference_concavity=self.theta,
                                                min_drainage_area=1000.0) #change minimum drainage area for visual preference

        self.chi_finder = ChiFinder(
            self.model_grid, min_drainage_area=100.0, reference_concavity=self.theta, use_true_dx=True)

        self.SSPM = SharedStreamPower(
            self.model_grid,  k_bedrock=self.k_bedrock, k_transport=self.k_transport,
            m_sp=self.m_sp, n_sp=self.n_sp, sp_crit=self.sp_crit, discharge_field=self.discharge_field,
            solver=self.solver
        )
        self.instantiate_plots() # makes plots so that data can be added to them throughout the run

    # Instantiate plots ###################################################
    def instantiate_plots(self):
        self.fig = plt.figure(figsize=(12, 12), layout="tight")
        self.gs = GridSpec(4, 3, figure=self.fig)


        self.slope_area_plot = self.fig.add_subplot(self.gs[3, 0:2])
        self.sedflux_plot = self.fig.add_subplot(self.gs[2, 0:2])
        self.ksn_plot = self.fig.add_subplot(self.gs[1, 0:2])
        self.parameters = self.fig.add_subplot(self.gs[:, 2])
        self.topo_plot = self.fig.add_subplot(self.gs[0, 0:2])

        self.slope_area_plot.set_xscale('log')
        self.slope_area_plot.set_yscale('log')
        self.slope_area_plot.set_xlabel(r'Drainage area [m$^2$]')
        self.slope_area_plot.set_ylabel('Slope [-]')

        self.sedflux_plot.set_xscale('log')
        self.sedflux_plot.set_xlabel(r'Drainage area [m$^2$]')
        self.sedflux_plot.set_ylabel(r'Sediment flux [m$^3$/s]')
        self.sedflux_plot.invert_xaxis()

        self.ksn_plot.set_xlabel("Distance upstream (m)")
        self.ksn_plot.set_ylabel(f"$K_{{sn}}$")
        #self.ksn_plot.invert_xaxis()

        self.topo_plot.set_xlabel(r'Drainage area [m$^2$]')
        self.topo_plot.set_ylabel('Elevation [-]')
        self.topo_plot.invert_xaxis()

        ###########Parameter Text###################
        self.parameters.set_axis_off()

        # Define a rainbow color cycle
        rainbow_colors = plt.cm.rainbow(np.linspace(0, 1, 11))
        # Update the default color cycle in rcParams
        self.slope_area_plot.set_prop_cycle(color=rainbow_colors)
        self.topo_plot.set_prop_cycle(color=rainbow_colors)
        self.ksn_plot.set_prop_cycle(color=rainbow_colors)
        self.sedflux_plot.set_prop_cycle(color=rainbow_colors)

        # Included for plotting the uplift ont the Ksn plot
        # Create second y-axis that shares the same x-axis
        #self.uplift_ax = self.ksn_plot.twinx()
        # Plot uplift data (replace x and uplift with your actual data variables)
        #uplift_data = self.model_grid['node']['uplift'][101:198]
        #x = np.arange(self.node_spacing, (self.num_cols- 2) * self.node_spacing, self.node_spacing)
        #self.uplift_ax.plot(x, uplift_data, color='red', label='Uplift')  # Customize color/label as needed
        # Set the label for the second y-axis
        #self.uplift_ax.set_ylabel('Uplift [mm/yr]')  # Adjust units as necessary


        if self.qs_plot:
            self.qs_fig = plt.figure(10)
            self.qs_pl = self.qs_fig.add_subplot()
            self.qs_pl.set_prop_cycle(color=rainbow_colors)
            self.qs_pl.set_xlabel("drainage area")
            self.qs_pl.set_ylabel("Qs/Qc")

        #plots analytical solutions underneath data. I switched these to be plotted in finalize_plots, so that they are on top
        #self._get_plot_sets()
        #self.sedflux_plot.plot(self.analytical_domain, self.sedflux_soln_0, linewidth=3, color='black',
        #                       linestyle=':', label='SS, U = 0.0001')
        #self.sedflux_plot.plot(self.analytical_domain, self.sedflux_soln, linewidth=3, color='red',
        #                       linestyle=':', label='SS, U = 0.00001')

        #self.ksn_plot.plot(self.Ksn_vals, self.distance_upstream, linewidth=3, color='black', linestyle=':',
        #                   label='Starting SS')
        #self.ksn_plot.plot(self.analytical_Ksn_domain, self.Ksn_soln, linewidth=3, color='red', linestyle=':',
        #                   label='SS, U = 0.00001')




    # Evolves Landscape
    def run_SSPM(self):
        self.make_grid()
        self.instantiate_components()

        # SSPM Loop
        while self.elapsed_time < self.run_time:

            # for plotting the starting grid as a black line, good for transient plots
            # if self.elapsed_time == 10: #for transient case, plot the starting steady state
            #    self._get_plot_sets()
            #    self.ksn_plot.plot(self.distance_upstream, self.Ksn_vals, linewidth=3, color='black',
            #                       label='10 yrs')
            #    self.topo_plot.plot(self.area, self.topo, linewidth=3,
            #                        color='black', label='10 yrs')

            # prints time every 1000 years
            if self.elapsed_time % self.print_time == 0:
                print("Elapsed time {}", self.elapsed_time)
                
            #  for plotting each timestep in plot_times
            if np.any(np.isin(self.elapsed_time, self.plot_times)):
                self._get_plot_sets()
                self.plot()

            if self.discharge_field == "water__unit_flux_in": # creating water flux as stochastic flooding

                # This is one function for stochastic flooding from from puerto rico distribusion, Rossi et al. 2016. 
                # This section can be modified
                # as desired to update a new_r (new runoff) value at each time step
                # e.g. increasing runoff overtime would just be :
                #new_r = elapsed_time/10000 + 1
                mean_r = 1.0  # m/yr
                shape_factor = 0.065 * (1000 * mean_r) ** 0.23  # From Rossi et al. 2016, converts to mm
                shape = 0.5
                scale_factor = mean_r / gamma(1.0 + (1.0 / shape_factor)) # From Rossi et al. 2016
                np.random.seed(3000)  # Setting the seed for reproducibility
                new_r = (scale_factor * ((-np.log(np.random.rand())) ** (1.0 / shape_factor)))

                #updates runoff values
                self.SSPM.update_runoff(new_runoff=new_r)

            # Run the flow router
            self.flow_accumulator.run_one_step()
            #self.fr.run_one_step()

            # Run the depression finder and router; optional
            self.depression_finder.map_depressions()

            # Calculates Erosion
            self.SSPM.run_one_step(dt=self.timestep)

            # Move  elevation of core nodes upwards relative to base level
            # at the rock uplift rate
            self.model_grid.at_node['topographic__elevation'][
                self.model_grid.core_nodes] += self.model_grid.at_node['uplift'][
                                                   self.model_grid.core_nodes] * self.timestep

            self.elapsed_time += self.timestep



    # Returns data sets used for plotting
    def _get_plot_sets(self): 

        # Define fields for plotting
        self.topo = self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]
        self.area = self.model_grid.at_node['drainage_area'][self.model_grid.core_nodes]
        #self.dist = self.model_grid.at_node[self.model_grid.core_nodes]['distances']
        self.qs = self.model_grid.at_node['sediment__flux'][self.model_grid.core_nodes] # sediment flux
        self.slope = self.model_grid.at_node['topographic__steepest_slope'][self.model_grid.core_nodes]
        self.qc = self.k_transport * self.area**(self.m_sp + 1) * self.slope**self.n_sp # sediment transport capacity
        self.x_all = self.model_grid.node_x[self.model_grid.core_nodes] # x value for each node, used in UA plot only

        # Pick Channels to get Ksn and distance upstream
        self.ChannelProfiler = ChannelProfiler(
            self.model_grid,
            number_of_watersheds=1,
            main_channel_only=True,
            minimum_channel_threshold=self.node_spacing ** 2,
        )
        self.ChannelProfiler.run_one_step()
        # make arrays for Ksn along channels and distances from outlet

        #runs through channels and gets Ksn values
        for i, outlet_id in enumerate(self.ChannelProfiler.data_structure):
            for j, segment_id in enumerate(self.ChannelProfiler.data_structure[outlet_id]):
                segment = self.ChannelProfiler.data_structure[outlet_id][segment_id]
                profile_ids = segment["ids"]
                self.distance_upstream = segment["distances"]
                self.steepness_finder.calculate_steepnesses()
                self.Ksn_vals = self.model_grid.at_node["channel__steepness_index"][profile_ids]
                #self.x_values = self.model_grid.node_x[profile_ids]
                
        self.distance_upstream = self.distance_upstream[1:-2] # adjusting to have same size as other arrays
        self.Ksn_vals = self.Ksn_vals[1:-2]



    # Finalizes plots, adds analytical solutions, and creates extra plots
    def finalize_plots(self, show=True, save=False, directory="./output/figures",
                        title='', plot_map=False, plot_channels=False, ksn_map=False, topo_map=False,
                       chi_map=False, UA_plot=False, ksn_profiles=False, ksn_profiles2=False, qsqc=False, watersheds=1):

        # Defining area and distance upstream sets as domains
        self.analytical_domain = np.arange(min(self.area), max(self.area), 1)
        self.analytical_Ksn_domain = np.arange(min(self.distance_upstream), max(self.distance_upstream),
                                               1)  #(0.0, 2750.0, 1.0)
        # Finding solution for Slope area plot
        self.K_eff = 1 / (1 / self.k_transport + 1 / self.k_bedrock)
        self.slope_soln = np.power(self.rock_uplift_rate * self.analytical_domain ** (-self.m_sp) #0.0001 is uplift rate
                                   / self.K_eff, 1 / self.n_sp)
        self.slope_soln_0 = np.power(0.0001 * self.analytical_domain ** (-self.m_sp)
                                   / self.K_eff, 1 / self.n_sp)
        #finding upper and lower bound solutions for sediment flux
        self.sedflux_soln = 0.00001 * self.analytical_domain
        self.sedflux_soln_0 = 0.0001 * self.analytical_domain

        # finding upper and lower bound solutions for Ksn
        self.Ksn_soln_number = np.power(0.00001 / self.K_eff, 1 / self.n_sp)  #changed self.uplift_rate to 0.0001 to get exact plot
        self.Ksn_soln_number_0 = np.power(0.0001 / self.K_eff, 1 / self.n_sp)
        #creating an array of these values the size of the domain
        self.Ksn_soln = self.Ksn_soln_number + self.analytical_Ksn_domain * 0
        self.Ksn_soln_0 = self.Ksn_soln_number_0 + self.analytical_Ksn_domain * 0
        
        #setting parameter text from self.__str__()
        self.parameter_txt = self.__str__()
     
        #plot slope solutions
        self.slope_area_plot.plot(self.analytical_domain, self.slope_soln_0, linewidth=3, color='black',
                               linestyle=':', label='SS, U = 0.0001')
        self.slope_area_plot.plot(self.analytical_domain, self.slope_soln, linewidth=3, color='red',
                               linestyle=':', label='SS, U = 0.00001')
        # plot sediment flux solutions
        self.sedflux_plot.plot(self.analytical_domain, self.sedflux_soln_0, linewidth=3, color='black',
                               linestyle=':', label='SS, U = 0.0001')
        self.sedflux_plot.plot(self.analytical_domain, self.sedflux_soln, linewidth=3, color='red',
                               linestyle=':', label='SS, U = 0.00001')

        # Plot Ksn solutions. Use to plot analytical solutions that are just lines
        self.ksn_plot.plot(self.analytical_Ksn_domain, self.Ksn_soln_0, linewidth=3, color='black', linestyle=':',
                           label='SS, U = 0.0001')
        self.ksn_plot.plot(self.analytical_Ksn_domain, self.Ksn_soln, linewidth=3, color='red', linestyle=':',
                           label='SS, U = 0.00001')
        
        # Use to plot a elevation solution as a final timestep as dotted line
        #self._get_plot_sets()
        #self.topo_plot.plot(self.area, self.topo, linewidth=3,linestyle=':',
        #                            color='red', label='Final SS',)

        #prints parameters on the right
        self.parameters.text(0, 0, self.parameter_txt, ha="left")

        #sets title to be Gh value
        if title == '':
            title = f"$G_{{h}}$ = {self.k_bedrock/self.k_transport}"
        self.fig.suptitle(title, fontsize=20)

        # Creates legends
        self.sedflux_plot.legend(loc='center left',  # Anchor the legend at the center-left of the bounding box
            bbox_to_anchor=(1, 0.5),  # Place it outside to the right of the plot
            fontsize=8)
        self.topo_plot.legend(
            loc='center left',  # Anchor the legend at the center-left of the bounding box
            bbox_to_anchor=(1, 0.5),  # Place it outside to the right of the plot
            fontsize=8)
        self.slope_area_plot.legend(
            loc='center left',  # Anchor the legend at the center-left of the bounding box
            bbox_to_anchor=(1, 0.5),  # Place it outside to the right of the plot
            fontsize=8)
        self.ksn_plot.legend(
            loc='center left',  # Anchor the legend at the center-left of the bounding box
            bbox_to_anchor=(1, 0.5),  # Place it outside to the right of the plot
            fontsize=8)

        # shows plot
        if show == True:
            self.fig.show()
      
        # Finalizes qs plot
        if self.qs_plot:
            self.qs_fig.suptitle(title, fontsize=20)
            self.qs_pl.legend(loc='best', fontsize=8)
            self.qs_fig.show()

        # sets saved file name and saves first plot
        if save == True:
            name = self.export_file_name
            while os.path.isdir(f"{directory}/{name}"):
                name += "i"
            #while os.path.isfile(f"{directory}/{name}.png"):
            #    name += "i"
            directory = f"{directory}/{name}"
            os.mkdir(directory)
            self.fig.savefig(f"{directory}/{name}.pdf", format='pdf')
            #saves qs_plot
            if self.qs_plot:
                self.qs_fig.savefig(f"{directory}/{name}_qsqc.png")

        #runs Channel Profiler to plot profiles in map view and with elevation            
        if plot_map or plot_channels:
            self.CP = ChannelProfiler(
                self.model_grid,
                number_of_watersheds=1,
                main_channel_only=False,
                minimum_channel_threshold=self.node_spacing ** 2,
            )
        #plots elevation in map view with picked channels
        if plot_map == True:
            self.CP.run_one_step()
            map = plt.figure(4)
            map.suptitle("Elevation Map")
            self.CP.plot_profiles_in_map_view() 
            if show == True:
                plt.show()
            if save == True:
                map.savefig(f"{directory}/{name}_map.png")
                
        #plots area vs elevation for picked channels
        if plot_channels== True:
            channels = plt.figure(5)
            self.CP.plot_profiles(ylabel="Elevation")
            channels.suptitle("Channel Profiles")
            if show == True:
                plt.show()
            if save == True:
                channels.savefig(f"{directory}/{name}_chan.png")

        if ksn_map == True:
            self.steepness_finder.calculate_steepnesses()
            ksn = plt.figure(7)
            imshow_grid(
                self.model_grid,
                "channel__steepness_index",
                grid_units=("m", "m"),
                var_name=f"$K_{{sn}}$",
                cmap="jet",
            )
            ksn.suptitle(f"$G_{{h}}$ = {self.k_bedrock/self.k_transport}")
            if show == True:
                plt.show()
            if save == True:
                ksn.savefig(f"{directory}/{name}_Ksn_map.pdf")

        if topo_map == True:

            topomap = plt.figure(20)

            imshow_grid(
                self.model_grid,
                "topographic__elevation",
                grid_units=("m", "m"),
                #limits=[0, 25],
                var_name="Elevation",
                #cmap="jet",

            )
            topomap.suptitle(f"$G_{{h}}$ = {self.k_bedrock / self.k_transport}")
            #topomap.suptitle(f"{self.uplift_type}, G = {self.k_bedrock/self.k_transport}, {self.elapsed_time} yrs")
            if show == True:
                plt.show()
            if save == True:
                topomap.savefig(f"{directory}/{name}_topo_map.pdf")

        if chi_map == True:
            self.chi_finder.calculate_chi()
            chimap = plt.figure(21)
            imshow_grid(
                self.model_grid,
                "channel__chi_index",
                grid_units=("m", "m"),
                #limits=[0,0.1],
                var_name="Chi Index ",
                cmap="magma",
            )
            chimap.suptitle(f"$G_{{h}}$ = {self.k_bedrock / self.k_transport}")
            if show == True:
                plt.show()
            if save == True:
                chimap.savefig(f"{directory}/{name}_chi_map.png")


        if UA_plot == True:
            fig, axes = plt.subplots(3, 1, figsize=(6, 8))  # Create a figure with two subplots

            uplift = self.model_grid.at_node['uplift'][self.model_grid.core_nodes]

            # First plot: qs and UA vs. drainage area
            axes[0].scatter(self.area, self.qs, s=20, label="Qs", alpha=0.7, edgecolor='k')
            axes[0].scatter(self.area, self.area * uplift, s=10, label="UA", alpha=0.7, edgecolor='r')
            axes[0].set_title("Steady State Check")
            axes[0].set_xlabel("Drainage Area")
            axes[0].set_ylabel("Qs and UA")
            axes[0].legend()

            # Second plot: qs- UA vs. x-distance
            axes[1].scatter(self.x_all, self.qs - self.area * uplift, s=20, alpha=0.7, edgecolor='k')
            axes[1].set_title("Steady State Check")
            axes[1].set_xlabel("X-distance")
            axes[1].set_ylabel("Qs - UA")

            # Third plot: qs- UA vs. x-distance, zoomed in
            axes[2].scatter(self.x_all, self.qs - self.area * uplift, s=20, alpha=0.7, edgecolor='k')
            axes[2].set_title("Steady State Check, Zoomed")
            axes[2].set_xlabel("X-distance")
            axes[2].set_ylabel("Qs - UA")
            axes[2].set_ylim(-0.1, 0.1)
            fig.suptitle(f"{self.uplift_type}, G = {self.k_bedrock / self.k_transport}, {self.elapsed_time} yrs")

            plt.tight_layout()  # Prevents overlap of titles and labels
            plt.show()

            if show == True:
                plt.show()
            if save == True:
                fig.savefig(f"{directory}/{name}_UA_plot.png")

        if ksn_profiles == True:
            # Calculate steepnesses
            self.SF = SteepnessFinder(self.model_grid, reference_concavity=self.theta, min_drainage_area=0)
            self.SF.calculate_steepnesses()
            # Find steepnesses along channel
            self.CP = ChannelProfiler(
                self.model_grid,
                number_of_watersheds=1,
                main_channel_only=False,
                minimum_channel_threshold=5*self.node_spacing ** 2,
            )
            self.CP.run_one_step()

            #plot channels in map view
            ksnmap= plt.figure(9)
            self.CP.plot_profiles_in_map_view()

            #plot Ksn of channels
            ksnpro = plt.figure(15)
            #ax = ksnpro.add_subplot(111)
            self.CP.plot_profiles(field='channel__steepness_index', xlabel='Distance Along Profile', ylabel='Ksn',
                          title='Ksn Profiles', color=None)
            #set specific view
            ax.set_ylim(0, 0.02)
            #ax = plt.gca()
            #ax.relim()
            #ax.autoscale_view()
            #ax.grid(True, axis='y', linestyle='--')#, alpha=0.7)
            if show == True:
                plt.show()

            if save == True:
                ksnpro.savefig(f"{directory}/{name}_ksn_prof.png")

        if ksn_profiles2 == True:
            # plots of normalized channel steepness in the profiled channels
            plt.figure(10)
            plt.figure(figsize=(6, 2))
            for i, outlet_id in enumerate(self.CP.data_structure):
                for j, segment_id in enumerate(self.CP.data_structure[outlet_id]):
                    if j == 0:
                        label = f"channel {i + 1}"
                    else:
                        label = "_nolegend_"
                    segment = self.CP.data_structure[outlet_id][segment_id]
                    profile_ids = segment["ids"]
                    distance_upstream = segment["distances"]
                    color = segment["color"]
                    plt.plot(
                        distance_upstream,
                        #self.model_grid.at_node[node_x][profile_ids],
                        self.model_grid.at_node["channel__steepness_index"][profile_ids],
                        "x",
                        color=color,
                        label=label,
                    )

            plt.xlabel("distance upstream (m)")
            plt.ylabel("steepness index")
            plt.legend(loc="lower left")
            plt.title("Distance Upstream vs. Ksn")
            if show:
                plt.show()

        if qsqc:
            channels = plt.figure(11)
            qsqc = self.qs/ self.qc
            plt.scatter(self.area, qsqc)
            plt.gca().invert_xaxis()
            plt.xlabel("drainage area")
            plt.ylabel("Qs/Qc")
            if show:
                plt.show()
            if save:
                channels.savefig(f"{directory}/{name}_qs_qc.png")


    

    def save_grid(self, directory="./output/grids"):
        while os.path.isfile(f"{directory}/{self.export_file_name}_topo.asc"): 
            self.export_file_name += "i"
        write_esri_ascii(f"{directory}/{self.export_file_name}_topo.asc", self.model_grid, 'topographic__elevation')

    def save_plot_sets(self, directory="/Users/anniet/Library/Mobile Documents/com~apple~CloudDocs/Documents/Docu"
                                       "ments - Annie’s MacBook Pro (2)/Fall 2024/Landlab/code/in_out_la"
                                       "ndlab/datasets/scratch"):

        new_directory = f"{self.export_file_name}"
        while os.path.isdir(f"{directory}/{new_directory}"):
            new_directory += "i"

        self._get_plot_sets()

        # Save multiple arrays to a .npz file
        np.savez(f'{directory}/{new_directory}.npz', area=self.area,  distance_upstream=self.distance_upstream,
                 Ksn_vals=self.Ksn_vals, topo=self.topo, qs=self.qs, qc=self.qc)







    def print_nodes(self):
        #print(type(self.Ksn_vals))
        #print(np.get_printoptions())
        np.set_printoptions(legacy='1.13')
        qsqc = [self.qs,self.qc]
        print(qsqc)
        np.savetxt(f"/Users/anniet/Library/Mobile Documents/com~apple~CloudDocs/Documents/Documents - Annie"
                   f"’s MacBook Pro (2)/Fall 2024/Landlab/code/in_out_landlab/datasets/csvs/trans"
                   f"ients/test_{self.test_name}_{self.elapsed_time}_{self.rock_uplift_rate}_qsqc.csv", qsqc, delimiter=",", fmt="%.8f")

    def plot(self, save=False, show=True, directory="../TransientOutput/figures/scratch",
             export_file_name1=-1, ):

        self._get_plot_sets()

        ##############Slope Area Plot###################
        self.slope_area_plot.scatter(self.area, self.slope, label=f'{self.elapsed_time} yrs')

        ##############Sed Flux Plot#####################
        # Plot drainage area on the x-axis and Qs on the y-axis.
        self.sedflux_plot.scatter(self.area, self.qs, label=f'{int(self.elapsed_time)} yrs')

        ####################Ksn Plot#################
        self.ksn_plot.scatter(self.distance_upstream, self.Ksn_vals, label=f'{int(self.elapsed_time)} yrs')

        ##############topo###################
        self.topo_plot.scatter(self.area, self.topo, label=f'{int(self.elapsed_time)} yrs')
        #self.topo_plot = self.ChannelProfiler.plot_profiles()
        if self.qs_plot:
            self.qs_pl.plot(self.area, self.qs / self.qc, label=f'{int(self.elapsed_time)} yrs')

        if self.ksn_series == True:
            self.steepness_finder.calculate_steepnesses()
            ksn_map = plt.figure(10)
            self.model_grid.imshow(
                "channel__steepness_index",
                grid_units=("m", "m"),
                var_name="Steepness index ",
                cmap="jet",
            )
            plt.title(f"$K_{{d}}$={self.k_bedrock};$K_{{t}}$={self.k_transport}; $time$={self.elapsed_time} yr")
            plt.show()




    def save_plot(self, directory="../output/_figures",
                  export_file_name=-1):
        if export_file_name == -1:
            export_file_name = self.export_file_name
        if not os.path.isfile(f"{directory}/{self.export_file_name}.png"):
            self.fig.savefig(f"{directory}/{self.export_file_name}.png")


    def export_grid(self, directory=f"/Users/anniet/Library/Mobile Documents/com~apple~CloudDocs/Docum"
                                      f"ents/Documents - Annie’s MacBook Pro (2)/Fall 2024/Landlab/code"
                                      f"/in_out_landlab/datasets/dem"):
        ## Below has the name of the file that data will be written to.
        ## You need to change the name of the file every time that you want
        ## to write data, otherwise you will get an error.
        ## This will write to the directory that you are running the code in.
        write_file_name = f"{directory}/{self.export_file_name}_fixed.txt"
        ## Below is writing elevation data in the ESRI ascii format so that it can
        ## easily be read into Arc GIS or back into Landlab.
        with open(write_file_name, "w") as fp:
            dump(self.model_grid, fp,at="node", name="topographic__elevation")


