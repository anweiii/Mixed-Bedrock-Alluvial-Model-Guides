import os

import matplotlib.pyplot as plt
import numpy as np
from landlab import RasterModelGrid  # imshow_grid
from landlab.components import (DepressionFinderAndRouter, ChannelProfiler, SteepnessFinder, FlowAccumulator,
                                ChiFinder, SpaceLargeScaleEroder, Space, ErosionDeposition, 
                                )
from landlab.io import write_esri_ascii, read_esri_ascii
from matplotlib.gridspec import GridSpec


# to do
# transience
# make different classes
# Check plots with Kelin

# Class to run tests on SPACE
# First, gets all the parameters, then methods:
# make the grid, run space, plot the results, save the results, could even analyze the results
# will also have inheritance to other classes with specified parameters including DL, TL, Mixed bedrock, and a dynamic
# one? or maybe I don't need to make a dynamic one,
# so I can run from main and even without defining parameters it will run a DL and make a plot
# and I can specify what the starting grid is

class TestSPACE:
    def __init__(
            self,
            # SPACE Parameters (make DL default)
            K_sed=0.01,
            K_br=0.001,
            K_t=0.001,
            F_f=0.,
            phi=0.,
            H_star=1.,
            v_s=1.0,
            m_sp=0.5,
            n_sp=1.0,
            sp_crit_sed=0.,
            sp_crit_br=0.,

            # Grid info, starting grid, rows, columns, dxy
            starting_grid="random",
            num_rows=20,
            num_cols=20,
            node_spacing=100.0,  # m,

            # time parameters, timestep, run time, print time, elapsed time
            # years
            timestep=10.0,
            # Set model run time
            run_time=1000,  # years
            # Set elapsed time to zero
            elapsed_time=0,
            print_time=1000,

            # Other Parameters
            rock_uplift_rate=1e-4,  # m/yr# Set rock uplift rate
            soil_depth=0,
            r=1.,  # m/yr # Define runoff parameter r, where Q=Ar
            test_name="Default",
            run_component="SpaceLargeScale",
            run_type="",
            dimension = 2,
            grid_directory = "./output/grids",

            # specify what plots to make?
    ):
        self.ChannelProfiler = None
        self.space = None
        self.chi_finder = None
        self.steepness_finder = None
        self.depression_finder = None
        self.flow_accumulator = None
        self.model_grid = None
        self.K_sed = K_sed
        self.K_br = K_br
        self.K_t = K_t

        self.F_f = F_f
        self.phi = phi
        self.H_star = H_star
        self.v_s = v_s
        self.m_sp = m_sp
        self.n_sp = n_sp
        self.sp_crit_sed = sp_crit_sed
        self.sp_crit_br = sp_crit_br

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
        self.soil_depth = soil_depth
        self.r = r  # m/yr # Define runoff parameter r, where Q=Ar
        self.test_name = test_name
        self.run_component = run_component
        self.export_file_name = (f"{self.test_name}_t{str(self.run_time)[0]}E{len(str(self.run_time)) - 1}_U"
                                 f"{round(self.rock_uplift_rate * 1000, 2)}"
                                 f"_{self.starting_grid[:10]}")
        self.theta = self.m_sp / self.n_sp
        self.run_type = run_type
        self.dimension = dimension
        self.grid_directory = grid_directory


    def __str__(self):
        return f"""\
        K_br: {self.K_br}
        K_sed: {self.K_sed}
        K_t: {self.K_t}
        F_f: {self.F_f}
        phi: {self.phi}
        H_star: {self.H_star}
        v_s: {self.v_s}
        m_sp: {self.m_sp}
        n_sp: {self.n_sp}
        sp_crit_sed: {self.sp_crit_sed}
        sp_crit_br: {self.sp_crit_br}
        starting_grid: {self.starting_grid}
        num_rows: {self.num_rows}
        num_cols: {self.num_cols}
        node_spacing: {self.node_spacing}
        timestep: {self.timestep}
        run_time: {self.run_time}
        elapsed_time: {self.elapsed_time}
        print_time: {self.print_time}
        rock_uplift_rate: {self.rock_uplift_rate}
        soil_depth: {self.soil_depth}
        r: {self.r}
        test_name: {self.test_name}
        component: {self.run_component}\
        """

    def make_grid(self):
        # use make grid from jupyter functions file
        #print(self.__str__())
        if 'random' == self.starting_grid:
            mg = RasterModelGrid((self.num_rows, self.num_cols), self.node_spacing)
            # Create initial topography
            np.random.seed(seed=5000)  # constant seed for constant random roughness

            # create grid for topo elevation?
            mg.add_zeros('node', 'topographic__elevation')
            # make elevation a tilted platform increasing in +x, +y direction (NE?)
            divided_factor = 100# before yuval change: 100000
            mg['node']['topographic__elevation'] += mg.node_y / divided_factor + mg.node_x / divided_factor + np.random.rand(
                len(mg.node_y)) / divided_factor
            # Create a grid field for soil depth
            mg.add_zeros('node', 'soil__depth')
            # Give an initial soil depth, in this case 0 m
            mg.at_node['soil__depth'][:] = self.soil_depth  # meters
            # Create a field for bedrock elevation
            mg.add_zeros('node', 'bedrock__elevation')
            # Make bedrock elevation equal to topographic elevation
            mg.at_node['bedrock__elevation'][:] = mg.at_node['topographic__elevation']
            # Increase topographic elevation by soil depth, in case there is any soil
            mg.at_node['topographic__elevation'][:] += mg.at_node['soil__depth']

        else:

            # import starting grid fields
            (grid1, topo) = read_esri_ascii(f"{self.grid_directory}/{self.starting_grid}/{self.starting_grid}_topo.asc")
            (grid2, sed) = read_esri_ascii(f"{self.grid_directory}/{self.starting_grid}/{self.starting_grid}_sed.asc")
            (grid3, bedr) = read_esri_ascii(f"{self.grid_directory}/{self.starting_grid}/{self.starting_grid}_bedr.asc")

            # make grid and add imported fields
            mg = RasterModelGrid((self.num_rows, self.num_cols), self.node_spacing)
            mg.add_field("topographic__elevation", topo, at="node")
            mg.add_field("soil__depth", sed, at="node")
            mg.add_field("bedrock__elevation", bedr, at="node")

            # check

        # SET GRID BOUNDARY CONDITIONS################################################
        # Close all domain borders

        """
        mg.set_closed_boundaries_at_grid_edges(bottom_is_closed=True, left_is_closed=True, right_is_closed=False,
                                                   top_is_closed=True)
        #if self.dimension == 2:
        """
        mg.set_closed_boundaries_at_grid_edges(bottom_is_closed=True, left_is_closed=True, right_is_closed=True,
                                               top_is_closed=True)
        mg.set_watershed_boundary_condition_outlet_id(int(mg.nodes[1,0]), mg['node']['topographic__elevation'], -9999.)
            # Open lower-left (southwest) corner


        self.model_grid = mg

    # Instantiate components###################################################
    def instantiate_components(self):

        # steepness finder,
        # chifinder
        self.flow_accumulator = FlowAccumulator(self.model_grid, flow_director="D8")
        # Instantiate depression finder and router; optional
        self.depression_finder = DepressionFinderAndRouter(self.model_grid)

        self.steepness_finder = SteepnessFinder(self.model_grid, reference_concavity=self.theta,
                                                min_drainage_area=1000.0)
        # initialize the component that will calculate the chi index
        self.chi_finder = ChiFinder(
            self.model_grid, min_drainage_area=1000.0, reference_concavity=self.theta, use_true_dx=True)

        # Instantiate SPACE model with chosen parameters
        if self.run_component == "SpaceLargeScale":
            self.space = SpaceLargeScaleEroder(self.model_grid, K_sed=self.K_sed, K_br=self.K_br, F_f=self.F_f,
                                               phi=self.phi,
                                               H_star=self.H_star, v_s=self.v_s, m_sp=self.m_sp, n_sp=self.n_sp,
                                               sp_crit_sed=self.sp_crit_sed, sp_crit_br=self.sp_crit_br,
                                               erode_flooded_nodes=False)

        if self.run_component == "OGSpace":
            self.space = Space(self.model_grid, K_sed=self.K_sed, K_br=self.K_br, F_f=self.F_f,
                               phi=self.phi,
                               H_star=self.H_star, v_s=self.v_s, m_sp=self.m_sp, n_sp=self.n_sp,
                               sp_crit_sed=self.sp_crit_sed, sp_crit_br=self.sp_crit_br,
                               # erode_flooded_nodes=False
                               )
            print("space")

        if self.run_component == "ErosionDepo":
            self.space = ErosionDeposition(
                self.model_grid, K=self.K_sed, v_s=self.v_s,
                m_sp=self.m_sp, n_sp=self.n_sp, sp_crit=0
            )

        #if self.run_component == "SSPM":
         #   self.space = SharedStreamPower(
         #       self.model_grid, K_d=self.K_br, K_t=self.K_t,
          #      m_sp=self.m_sp, n_sp=self.n_sp, sp_crit=0
          #  )

    def run_space(self):

        self.make_grid()
        self.instantiate_components()  # instantiates flow_accumulator, depression_finder, steepness_finder,
        # chi_finder, # space

        # SPACE Loop
        self.model_grid.at_node['topographic__elevation'][:] += 100
        while self.elapsed_time < self.run_time:
            if self.elapsed_time % self.print_time == 0:
                print("Elapsed time {}", self.elapsed_time)

            # Run the flow router
            self.flow_accumulator.run_one_step()

            # Run the depression finder and router; optional
            self.depression_finder.map_depressions()

            # There used to be something about flooded nodes here, but i deleted it
            # Run the SPACE model for one timestep
            self.space.run_one_step(dt=self.timestep)

            # Move bedrock elevation of core nodes upwards relative to base level
            # at the rock uplift rate
            self.model_grid.at_node['bedrock__elevation'][
                self.model_grid.core_nodes] += self.rock_uplift_rate * self.timestep

            # Strip any soil from basin outlet so that all topographic change is due to
            # rock uplift
            # self.model_grid.at_node['soil__depth'][0] = 0.

            # Recalculate topographic elevation to account for rock uplift
            self.model_grid.at_node['topographic__elevation'][:] = self.model_grid.at_node['bedrock__elevation'][
                                                                   :] + self.model_grid.at_node['soil__depth'][:]

            self.elapsed_time += self.timestep

    #import matplotlib.pyplot as plt
    #import numpy as np
    #from landlab import RasterModelGrid  # imshow_grid
    #from landlab.components import (DepressionFinderAndRouter, ChannelProfiler, SteepnessFinder, FlowAccumulator,
                                    #ChiFinder, ErosionDeposition)
    #from landlab.io import write_esri_ascii, read_esri_ascii

    # to do
    # transience
    # make different classes
    # Check plots with Kelin

    # Class to run tests on SPACE
    # First, gets all the parameters, then methods:
    # make the grid, run space, plot the results, save the results, could even analyze the results
    # will also have inheritance to other classes with specified parameters including DL, TL, Mixed bedrock, and a dynamic
    # one? or maybe I don't need to make a dynamic one,
    # so I can run from main and even without defining parameters it will run a DL and make a plot
    # and I can specify what the starting grid is

    def get_plot_sets(self):

        # slope area: X:area Y:slope
        # flux area: X area Y: qs
        # Ksn: X:distance_upstream, Y:Ksn_vals

        # Define fields for plotting###
        # define area field
        area = np.zeros(len(self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]))
        area[:] = self.model_grid.at_node['drainage_area'][self.model_grid.core_nodes]
        # define sed flux field
        qs = np.zeros(len(self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]))
        qs[:] = self.model_grid.at_node['sediment__flux'][self.model_grid.core_nodes]
        # define the slope field
        slope = np.zeros(len(self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]))
        slope[:] = self.model_grid.at_node['topographic__steepest_slope'][self.model_grid.core_nodes]
        # Pick Channels
        self.ChannelProfiler = ChannelProfiler(
            self.model_grid,
            number_of_watersheds=1,
            main_channel_only=True,
            minimum_channel_threshold=1,
        )
        self.ChannelProfiler.run_one_step()
        # make arrays for Ksn along channels and distances from outlet
        self.steepness_finder.calculate_steepnesses()

        for i, outlet_id in enumerate(self.ChannelProfiler.data_structure):
            for j, segment_id in enumerate(self.ChannelProfiler.data_structure[outlet_id]):
                segment = self.ChannelProfiler.data_structure[outlet_id][segment_id]
                profile_ids = segment["ids"]
                distance_upstream = segment["distances"]
                Ksn_vals = self.model_grid.at_node["channel__steepness_index"][profile_ids]

        Area = area.copy()
        Slope = slope.copy()
        Sedflux = qs.copy()

        Distance = distance_upstream.copy()
        Ksn = Ksn_vals.copy()

        # Analytical solutions

        analytical_domain = np.arange(min(area), max(area), 1)
        K_eff = 1 / (1 / self.K_br + 1 / self.K_sed * self.v_s)
        slope_soln = np.power(self.rock_uplift_rate * analytical_domain ** (-self.m_sp)
                              / K_eff, 1 / self.n_sp)
        sedflux_soln = self.rock_uplift_rate * analytical_domain

        analytical_Ksn_domain = np.arange(0.0, 2750.0, 1.0)

        Ksn_soln_number = np.power(self.rock_uplift_rate / K_eff, 1 / self.n_sp)
        Ksn_soln = Ksn_soln_number + analytical_Ksn_domain * 0
        parameter_txt = self.__str__()
        plot_title = f"{self.test_name}, {self.run_time} yrs, {self.starting_grid} start"
        export_file_name = self.export_file_name

        return (Area, Slope, Sedflux, Distance, Ksn, analytical_domain, slope_soln, sedflux_soln,
                analytical_Ksn_domain, Ksn_soln, parameter_txt, plot_title, export_file_name)

    def plot(self):

        # Define fields for plotting###
        # define sed depth
        sed_depth = np.zeros(len(self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]))
        sed_depth[:] = self.model_grid.at_node['soil__depth'][self.model_grid.core_nodes]
        # define area field
        area = np.zeros(len(self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]))
        area[:] = self.model_grid.at_node['drainage_area'][self.model_grid.core_nodes]
        # define sed flux field
        qs = np.zeros(len(self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]))
        qs[:] = self.model_grid.at_node['sediment__flux'][self.model_grid.core_nodes]
        # define the slope field
        slope = np.zeros(len(self.model_grid.at_node['topographic__elevation'][self.model_grid.core_nodes]))
        slope[:] = self.model_grid.at_node['topographic__steepest_slope'][self.model_grid.core_nodes]

        # Pick Channels
        self.ChannelProfiler = ChannelProfiler(
            self.model_grid,
            number_of_watersheds=1,
            main_channel_only=True,
            minimum_channel_threshold=self.node_spacing ** 2,
        )
        self.ChannelProfiler.run_one_step()

        # instantiate figure for subplot
        total_fig = plt.figure(figsize=(12, 12),layout="constrained")
        total_fig.suptitle(f"{self.test_name}, {self.run_time} yrs, {self.starting_grid} start", fontsize=16)

        # Slope Area for all nodes
        slope_area_plot = plt.subplot(421)

        # Plot drainage area on the x-axis and slope on the y-axis.
        slope_area_plot.scatter(area, slope, marker='o', color='k', label='Model slope')

        # set x-axis to log scale
        slope_area_plot.set_xscale('log')
        slope_area_plot.set_yscale('log')

        # Label axes
        slope_area_plot.set_xlabel(r'Drainage area [m$^2$]')
        slope_area_plot.set_ylabel('Slope [-]')

        # Calculate and plot analytical solution
        analytical_domain = np.arange(min(area), max(area), 1)

        # Default Analytical Soln for slope
        slope_DL_analytical_soln = np.power(
            self.rock_uplift_rate / (self.K_br * np.power(analytical_domain, self.m_sp)), 1 / self.n_sp)

        sed_depth_DL_analytical_soln = 0  # -self.H_star * np.log(1 - (self.v_s / ((self.K_sed * self.r / self.K_br)
        # + self.v_s)))
        sed_depth_DL_analytical_array = np.repeat(sed_depth_DL_analytical_soln, len(analytical_domain))

        # TL Solution for slope
        slope_TL_analytical_soln = np.power(
            (self.rock_uplift_rate * self.v_s) / (
                    self.K_sed * np.power(analytical_domain, self.m_sp) * self.r), 1 / self.n_sp)
        # Equation 44 solution
        slope_TL44_analytical_soln = np.power(
            (self.rock_uplift_rate * self.v_s) / (
                    self.K_sed * np.power(analytical_domain, self.m_sp) * self.r) + self.rock_uplift_rate /
            (self.K_sed * np.power(analytical_domain, self.m_sp)), 1 / self.n_sp)

        # Calculate analytical sediment depth
        sed_depth_TL_analytical_soln = -self.H_star * np.log(
            1 - (self.v_s / ((self.K_sed * self.r / self.K_br) + self.v_s)))
        sed_depth_TL_analytical_array = np.repeat(sed_depth_TL_analytical_soln, len(analytical_domain))

        # Mixed bedrock analytical solution
        slope_MB_analytical_soln = np.power(
            (self.rock_uplift_rate * self.v_s) / (
                    self.K_sed * np.power(analytical_domain, self.m_sp) * self.r) + self.rock_uplift_rate / (
                    self.K_br * np.power(analytical_domain, self.m_sp)), 1 / self.n_sp)

        sed_depth_MB_analytical_soln = -self.H_star * np.log(
            1 - (self.v_s / ((self.K_sed * self.r / self.K_br) + self.v_s)))
        sed_depth_MB_analytical_array = np.repeat(sed_depth_MB_analytical_soln, len(analytical_domain))

        # DL plot solution
        slope_area_plot.plot(analytical_domain, slope_DL_analytical_soln, linewidth=3, color='blue', linestyle='-',
                             label='DL')
        # TL plot solution
        slope_area_plot.plot(analytical_domain, slope_TL_analytical_soln, linewidth=2, color='red', linestyle='-',
                             label='TL')
        slope_area_plot.plot(analytical_domain, slope_TL44_analytical_soln, linewidth=1.5, color='orange',
                             linestyle='-',
                             label='eq 44')
        # MB plot solution
        slope_area_plot.plot(analytical_domain, slope_MB_analytical_soln, linewidth=1, color='green', linestyle='-',
                             label='MB')

        # Make a legend
        slope_area_plot.legend(loc='center left',  # Anchor the legend at the center-left of the bounding box
            bbox_to_anchor=(1, 0.5),  # Place it outside to the right of the plot
            fontsize=8)
        # plt.title(f"Slope Area")

        # Ksn PLOT#########

        # Code Block 21
        # Plot channel steepness along profiles and across the landscape

        # calculate channel steepness
        self.steepness_finder.calculate_steepnesses()

        # plots of steepnes vs. distance upstream in the profiled channels
        ksn_plot = plt.subplot(425)

        for i, outlet_id in enumerate(self.ChannelProfiler.data_structure):
            for j, segment_id in enumerate(self.ChannelProfiler.data_structure[outlet_id]):
                if j == 0:
                    label = f"channel {i + 1}"
                else:
                    label = "_nolegend_"
                segment = self.ChannelProfiler.data_structure[outlet_id][segment_id]
                profile_ids = segment["ids"]
                distance_upstream = segment["distances"]
                color = segment["color"]
                plt.plot(
                    distance_upstream,
                    self.model_grid.at_node["channel__steepness_index"][profile_ids],
                    "x",
                    color=color,
                    label=label,
                )
        analytical_Ksn_domain = distance_upstream

        # Default Analytical Soln for slope
        # Ksn_analytical_soln_Ks = np.power(
        #     self.rock_uplift_rate / (1 / (1 / self.K_br + 1 / self.K_sed)) + analytical_Ksn_domain * 0, 1 / self.n_sp)
        # print(Ksn_analytical_soln)
        # Ksn calculated with Kt = ks/G, G = V/r
        Ksn_analytical_soln_Keff = np.power(
            self.rock_uplift_rate / (
                    1 / (1 / self.K_br + 1 / (self.K_sed / (self.v_s / self.r)))) + analytical_Ksn_domain * 0,
            1 / self.n_sp)

        plt.plot(analytical_Ksn_domain, Ksn_analytical_soln_Keff, linewidth=2, color='green', linestyle='-',
                 label='K_eff solution')
        # plt.plot(analytical_Ksn_domain, Ksn_analytical_soln_Ks, linewidth=1, color='red', linestyle='-',
        #         label='Kt solution')

        plt.xlabel("distance upstream (m)")
        plt.ylabel("Ksn")
        plt.legend(loc='center left',  # Anchor the legend at the center-left of the bounding box
            bbox_to_anchor=(1, 0.5),  # Place it outside to the right of the plot
            fontsize=8)
        # plt.title(f"Ksn")
       
        # Instantiate subplot
        sedflux_plot = plt.subplot(423)

        # Plot drainage area on the x-axis and Qs on the y-axis.
        sedflux_plot.scatter(area, qs, marker='o', color='k', label='Model Qs')

        # set x-axis to log scale
        sedflux_plot.set_xscale('log')

        # Label axes
        sedflux_plot.set_xlabel(r'Drainage area [m$^2$]')
        sedflux_plot.set_ylabel(r'Sediment flux [m$^3$/s]')

        # Plot analytical solution
        sedflux_plot.plot(analytical_domain, self.rock_uplift_rate * analytical_domain, linewidth=2, color='grey',
                          linestyle='-', label='Analytical Qs')

        # Make a legend
        sedflux_plot.legend(loc='center left',  # Anchor the legend at the center-left of the bounding box
            bbox_to_anchor=(1, 0.5),  # Place it outside to the right of the plot
            fontsize=8)

        
        # Sed Depth Plot######

        # Instantiate subplot
        sed_depth_plot = plt.subplot(427)

        # Plot drainage area on the x-axis and slope on the y-axis.
        sed_depth_plot.scatter(area, sed_depth, marker='o', color='k', label='Model depth')

        # set x-axis to log scale
        sed_depth_plot.set_xscale('log')

        # Label axes
        sed_depth_plot.set_xlabel(r'Drainage area [m$^2$]')
        sed_depth_plot.set_ylabel('Sediment depth [m]')
        # sed_depth_plot.set_title('Sediment ')

        # Calculate and plot analytical solution
        # DL plot solution
        sed_depth_plot.plot(analytical_domain, sed_depth_DL_analytical_array, linewidth=2, color='blue', linestyle='-',
                            label='DL')
        # TL plot solution
        sed_depth_plot.plot(analytical_domain, sed_depth_TL_analytical_array, linewidth=2, color='red', linestyle='-',
                            label='TL')
        # MB plot solution
        sed_depth_plot.plot(analytical_domain, sed_depth_MB_analytical_array, linewidth=2, color='green', linestyle='-',
                            label='MB')
        sed_depth_plot.legend(loc='upper right')
        

        parameter_text = plt.subplot(428)
        parameter_text.set_axis_off()
        parameter_text.text(0, 0, self.__str__(), fontsize = 7)
        #total_fig.tight_layout()

        # if os.path.isfile(f"output/{self.export_file_name}/{self.export_file_name}_topo.asc") == True:
        if not os.path.isfile(f"./output/figures/{self.export_file_name}_space.png"):
            total_fig.savefig(f"./output/figures/{self.export_file_name}_space.png")

    # total_fig.suptitle(self.__str__())

    # come up with detailed label from plots with __str__ or __repr__
    # could create if statements for each plot

    # plot slope area,
    # plot sed depth vs area
    # plot Ksn
    # plot chi
    # plot channel locations on topography
    # plot elevation vs distance
    # plot sediment flux vs area

    def save_grid(self, directory="./output/grids"):
        path = f"{directory}/{self.export_file_name}"

        # check if directory exists
        if not os.path.isfile(f"{path}/{self.export_file_name}_topo.asc"):
            os.mkdir(path)  # make folder for this output\
            # write .asc files for topo,sed,bedrock
            write_esri_ascii(f"{path}/{self.export_file_name}_topo.asc", self.model_grid, 'topographic__elevation')
            write_esri_ascii(f"{path}/{self.export_file_name}_sed.asc", self.model_grid, 'soil__depth')
            write_esri_ascii(f"{path}/{self.export_file_name}_bedr.asc", self.model_grid, 'bedrock__elevation')

    def calc_hss(self):
        hss = -self.H_star * np.log(1 - 1 / (1 + self.K_sed / (self.v_s / self.r * self.K_br)))

        print(hss)

