# ProteusDS Solar Platform Generator
This repository contains a CLI tool, `pds-solar-gen`, that generates floating solar platforms for 
DSA's ProteusDS. The goal of this tool is to reduce the tediousness of writing ProteusDS simulation 
files for large floating solar platforms. 

This tool generates a series of simulation files containing the specifications 
and parameters of individual floats, the connections between them, and/or thrusters to drive the 
platform. It does not generate the ProteusDS executable (.PDSi), summary (.PDSp) files, or the custom 
meshes for the individual floats. 

This tool is designed to be used per the following workflow:
1. Open ProteusDS and save a blank simulation
2. Copy the "config.yaml" into the simulation folder and edit as necessary
3. Open a command terminal or Anaconda prompt, "cd" to the current working folder, and run
    ```bash
    pds-solar-gen generate <n_rows> <n_cols> config.yaml .
    ```
4. This will generate an array of the entered rows and columns and save the files in the current working folder
5. Reopen the simulation executable
6. Run the simulation to allow the array to settle
7. When the initial simulation has completed, export the results to a new simulation
7. In the new simulation, edit environment and simulation time parameters in the ProteusDS GUI as desired
8. Run the new simulation


### Usage
To use this tool, you must first have Conda (Anaconda or Miniconda) and Git installed on your local machine.
1. Pip install the repository from the github repository:
    ```shell
    pip install "git+https://github.com/jmcvey3/pds-solar-gen.git@main#egg=pds-solar-gen"
    ```
2. Run the tool with:

    ```shell
    pds-solar-gen generate <nrows> <ncols> <path/to/config_file.yaml> <path/to/simulation/folder>
    ```

Full usage instructions can be obtained using the `--help` flag:

```shell
>>> pds-solar-gen generate --help

Usage: pds-solar-gen generate [OPTIONS] NROWS NCOLS CONFIG_FILE OUTPUT_PATH

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    nrows   INT  Number of rows, i.e. rows of solar panels, to create for the platform. Dictates number│
│                   of long and small floats to use.                                                      │
│                       [default: 3]                                                                      │
│                       [required]                                                                        │
│ *    ncols   INT  Number of columns, i.e. columns of solar panels, to create for the platform. Dictates │
│                   number of main floats and solar panels, in the platform to create.                    │
│                       [default: 3]                                                                      │
│                       [required]                                                                      │
│ *    config_file   PATH  Path to the configuration file that that should be used to generate the array. │
│                              [default: config.yaml]                                                     │
│                              [required]                                                                 │
│ *    output_path   PATH  Path to the folder that the generation simulation files should be saved.       │
│                              [default: pds_sim]                                                         │
│                              [required]                                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help                                                                Show this message and exit.       │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Setting Thruster Locations

There are several thruster parameters than can be edited in 
the yaml configuration file ("config.yaml").
- The thruster model
- Number of thrusters
- Thruster location
- Thruster angle
- RPM setpoint

The thruster model is specified via the `name` and `body` keys. 
Currently the Blue Robotics T200 and T500 are programmed into the 
sourcecode, with the default set to use 4 BlueRobotics T200
thrusters.

To add thrusters, 
1. First set `n` to the total number in use.
2. Next, pair the thruster with the float you plan to attach it to in 
`float_pairs`. The keys should be in numerical order, starting from "0",
and the items are the float names, either "Small_Float#", 
"Main_Float#", or "Long_Float#", where "#" is the float number.

3. To locate the thrusters in space, set the distance in cartesian 
coordinates (x, y, z) from the center of the float to the thruster 
in `float_location`. These are ordered in the same order as 
`float_pairs`. For a small float, setting a thruster at the edge of its
shorter side is [0, -0.2, 0.16]. Note that +Z is down in ProteusDS.

4. Set the angle you want each thruster to point towards with 
`angle`. Setting this to 90 means that the thruster is facing 
along the +Y axis (the row axis) in ProteusDS, directing thrust in 
the -Y direction.

5. Finally, we can set the `RPM` setpoint. This ultimately determines the 
thruster speed. ProteusDS uses the thrust and torque coefficients in 
the thruster library file to determine speed from RPM.
