import math
import numpy as np
import time
from batch_gnome import tap_comp_volume


def comp_volume_mf(positions, mass, flags, grid, flag_bitmask_to_ignore=1 + 2 + 4 + 8 + 16):
    """
    computes the volume in each grid cell for a single time step
    Adapted for the wadden sea case where we want to look at beached oil only

    # default flags to not count:
    #    notReleased: 1
    #    offMaps: 4
    #    evaporated: 8
    #    notOnSurface: 16
    #    floating: 2

    # default flags to include:
    #    beached on mudflat: 32 is included.

    # for each grid box (and the whole grid), the bottom left is included, the top right is not

    """
    min_long = grid.min_long
    max_long = grid.max_long
    min_lat = grid.min_lat
    max_lat = grid.max_lat
    num_lat = grid.num_lat
    num_long = grid.num_long
    dlat = grid.dlat
    dlong = grid.dlong

    # create a grid:
    mass_grid = np.zeros((num_long, num_lat), dtype=np.float32)

    # loop through the LEs
    for i in xrange(len(positions)):
        # print "checking LE:", i
        # check the flag:
        if (flag_bitmask_to_ignore & flags[i]):
            # skip over this one
            # print "flag hit, skipping LE:", i
            continue
        # what cell is this LE in?
        lon = positions[i, 0]
        lat = positions[i, 1]
        # print "i, lat,lon", i, lat, lon
        if lon >= min_long and lon < max_long and lat >= min_lat and lat < max_lat:
            # < on max, so we don't run off the grid in the next step
            # and to be consistent - top right not included
            long_ind = int(math.floor((lon - min_long) / dlong))
            lat_ind = int(math.floor((lat - min_lat) / dlat))
            # print "row, col:", row, col
            mass_grid[long_ind, lat_ind] += mass[i]
            # else:
            # print "LE is off the grid"
    return mass_grid


from post_gnome import nc_particles


def CompThicknessCube_mf(FileList, OutputTimes, Grid, Weather=None):
    """
    CompThicknessCube computes the average thickness of the oil over
    each receptor site. It only works for grid receptors.

    Filelist is a list of netcdf file names: one for each trajectory

    OutputTimes is a sequence of output times, in hours, from the beginning of the run.

    Grid is a Grid object, specifying the grid parameters

    If Weather is not None it must be a tap_comp_volume.weather_curve object

    If Weather is None, then there is no change in volume.

    """

    ## read the header of the first trajectory file: It is assumed that
    ## the others will match..no check is made to assure this, but it
    ## will crash if anything is very wrong.
    # (junk, junk, HeaderData, junk) = ReadTrajectory(FileList[0],2)

    # read the trajectory data from the first netcdf file
    # print "**************"
    # print "getting header info from file:", FileList[0]
    traj_file = nc_particles.Reader(FileList[0])

    if traj_file.get_units('age') != 'seconds':
        raise ValueError("particle age units in netcdf file must be in seconds")

    NumTimesteps = len(traj_file.times)
    MaxNumLEs = traj_file.particle_count[:].max()

    TimeStep = traj_file.times[1] - traj_file.times[0]  # assume constant timestep!
    traj_file.close()

    TimeStepHours = TimeStep.total_seconds() / 3600.00
    ## OutputTimes should already be in hours
    OutputSteps = (np.array([0] + OutputTimes) / TimeStepHours).astype(np.int32)  # in integer units of time step
    # Allocate the Cube
    NumSpills, NumSites, NumTimes = len(FileList), Grid.num_cells, len(OutputTimes)
    ## fixme: need to make this a float cube!
    Cube = np.zeros((NumTimes, NumSites, NumSpills), np.float32)
    Cube_mf = np.zeros((NumTimes, NumSites, NumSpills), np.float32)

    start = time.time()  # just for timing how long it takes to run
    print OutputSteps

    ## Loop through each individual trajectory
    for SpillNum in range(NumSpills):
        # print "computing spill number %i"%(SpillNum,)
        # read new trajectory file:
        print "working with file:", FileList[SpillNum]
        traj_file = nc_particles.Reader(FileList[SpillNum])
        VolTable = np.zeros((NumSites), np.float32)  # this will store the Maximum volume in each grid box.
        VolTable_mf = np.zeros((NumSites), np.float32)  # this will store the Maximum volume in each grid box.

        ## Step through the Cube output time steps
        for step in xrange(len(OutputSteps) - 1):
            ## step through the Trajectory time steps between each Cube Timestep
            for t in xrange(OutputSteps[step], OutputSteps[step + 1]):
                LE_vars = traj_file.get_timestep(t, variables=['longitude', 'latitude', 'age', 'status_codes'])
                LE_lat = LE_vars['latitude']
                LE_long = LE_vars['longitude']
                LE_positions = np.column_stack((LE_long, LE_lat))
                NumLEs = LE_positions.shape[0]
                LE_age = LE_vars['age'].astype(np.float32) / 3600.00
                # NOTE: for TAP -- we assume that are the particles have unit mass at the start
                #      so we don't read it from the file
                LE_mass = np.ones((NumLEs,), dtype=np.float32)
                if Weather:
                    # print "weathering the LEs"
                    LE_mass = Weather.weather(LE_mass, LE_age)
                flags = LE_vars['status_codes'].astype(np.uint8)
                Vol = tap_comp_volume.comp_volume(LE_positions, LE_mass, flags, Grid)
                Vol_mf = comp_volume_mf(LE_positions, LE_mass, flags, Grid)
                # keep the largest volume computed between output timesteps
                VolTable = np.maximum(Vol.flat, VolTable)
                VolTable_mf = np.maximum(Vol_mf.flat, VolTable_mf)
            ## put the max volume in the Cube at this Cube time step
            # Cube[step,:,SpillNum] = transform(VolTable, MaxNumLEs)
            Cube[step, :, SpillNum] = VolTable
            Cube_mf[step, :, SpillNum] = VolTable_mf
        traj_file.close()
    # print "cube took %s seconds to generate"%(time.time() - start)
    return Cube, Cube_mf
