"""
Script for generating floating solar platforms consisting of a main float,
which holds the solar panel, and two slimmer floats that form the walkways
between rows of solar panels/main floats.
"""

import os
import numpy as np
from itertools import product

import pds_solar_gen.lib_basic as lb
import pds_solar_gen.lib_floats as lf
import pds_solar_gen.lib_thrusters as lt


def check_configurations(thruster, floats):
    ## Configuration checks
    if thruster["n"]:
        if len(thruster["float_pairs"]) != thruster["n"]:
            raise Exception(
                "Number of entries in `float_thruster_pairs` should equal `n_thrusters`"
            )
        if len(thruster["float_location"]) != thruster["n"]:
            raise Exception(
                "Number of entries in `thruster_loc` should equal `n_thrusters`"
            )
        if len(thruster["angle"]) != thruster["n"]:
            raise Exception(
                "Number of entries in `thruster_ang` should equal `n_thrusters`"
            )
        if thruster["name"] not in ["blue_robotics_t200", "blue_robotics_t500"]:
            raise ValueError(
                f"{thruster['name']} not encoded in `lib_thrusters`. "
                "Please select 'blue_robotics_t200' or 'blue_robotics_t500'."
                "If this has changed, please update this error code in config.py."
            )

    for ky, val in floats["moments_of_inertia"].items():
        if len(val) != 3:
            raise Exception(
                f"MoI of {ky} should have 3 entries for Ixx, Iyy, and Izz, in kg m^2"
            )
    for ky, val in floats["cD"].items():
        if len(val) != 4:
            raise Exception(
                f"cD of {ky} should have 4 entries for cDt, cDx, cDy, and cDz"
            )
    for ky, val in floats["cA"].items():
        if len(val) != 3:
            raise Exception(f"cA of {ky} should have 3 entries for cAx, cAy, and cAz")


def create_directory(proteus_directory):
    """Generic function for creating a filepath"""
    if not os.path.exists(proteus_directory):
        os.makedirs(proteus_directory)


def n_floats(nrows, ncols):
    """Returns a tuple of the number of floats given the number
    of rows and columns.
    """

    n_main = nrows * ncols  # includes perimeter floats
    n_small = (nrows + 1) * ncols
    n_long = (nrows + 1) * (ncols - 1)

    return n_main, n_small, n_long


def create_ini(proteus_directory, nrows, ncols, floats, solar_panel):
    """Write .ini files, which contain the rigid body physical parameters,
    mesh filenames, and any 'probes' (instruments).
    """

    n_main, n_small, n_long = n_floats(nrows, ncols)
    # Figure out perimeter indices
    idx = np.linspace(0, ncols * nrows - 1, nrows + 1)
    idc = np.ceil(idx)
    idf = np.floor(idx)
    i_perimeter = set(np.hstack((idc, idf)))

    for i in range(n_main):
        fname = os.path.join(proteus_directory, f"Main_Float{i}.ini")
        if floats["perimeter"] and (i in i_perimeter):
            with open(fname, "w") as f:
                f.write(
                    lf.MAIN(
                        floats["moments_of_inertia"]["main"], floats["mass"]["main"]
                    )
                )
        else:
            with open(fname, "w") as f:
                f.write(
                    lf.MAIN_PANEL(
                        floats["moments_of_inertia"]["main_panel"],
                        floats["mass"]["main_panel"],
                        solar_panel["height"],
                        solar_panel["pitch"],
                    )
                )

    for i in range(n_long):
        fname = os.path.join(proteus_directory, f"Long_Float{i}.ini")
        with open(fname, "w") as f:
            f.write(
                lf.LONG(floats["moments_of_inertia"]["long"], floats["mass"]["long"])
            )

    for i in range(n_small):
        fname = os.path.join(proteus_directory, f"Small_Float{i}.ini")
        with open(fname, "w") as f:
            f.write(
                lf.SMALL(floats["moments_of_inertia"]["small"], floats["mass"]["small"])
            )


def create_dat(proteus_directory, nrows, ncols, spacing, heading):
    """
    Creates .dat files, which contain the initial state tensor of the rigid body.

    Float coordinates are organized in the coords dictionary by (row, col),
    starting from the lower left hand corner, filling up the row from left to
    right, then bumping up the column and filling in the next row, and so on.
    """

    # Write out spacing dimensions
    r_main = spacing["main"][0]  # m, row spacing between main floats
    c_main = spacing["main"][1]  # m, column spacing between main floats
    r_long_offset = spacing["long"][0]  # m, row offset between main and long floats
    c_long_offset = spacing["long"][1]  # m, column offset between main and long floats
    r_small_offset = spacing["small"][0]  # m, row offset between main and small floats
    c_small = spacing["small"][1]  # m, column spacing between small floats

    ## Create .dat files
    n_main, n_small, n_long = n_floats(nrows, ncols)

    # Main float coordinates
    rows = np.arange(0, nrows * r_main, r_main)
    cols = np.arange(0, ncols * c_main, c_main)
    coords = {}
    # Trim to avoid issues when float spacing is divisible by nrows or ncols
    coords["main"] = tuple(product(rows[:nrows], cols[:ncols]))

    # Long float coordinates
    rows = np.arange(
        r_long_offset, abs(nrows * r_long_offset * 2), abs(r_long_offset * 2)
    )
    cols = np.arange(c_long_offset, (ncols - 1) * c_long_offset * 2, c_long_offset * 2)
    coords["long"] = tuple(product(rows[: nrows + 1], cols[: ncols - 1]))

    # Small float coordinates
    rows = np.arange(
        r_small_offset, abs(nrows * r_small_offset * 2), abs(r_small_offset * 2)
    )
    cols = np.arange(0, ncols * c_small, c_small)
    coords["small"] = tuple(product(rows[: nrows + 1], cols[:ncols]))

    def create_state(coords, flt, i):
        zero = lf.STATE_ZERO.split("\n")
        x = coords[flt][i][0]  # X, column axis
        y = coords[flt][i][1]  # Y, row axis

        # Rotate floats based on initial heading
        cos = np.cos(np.deg2rad(heading))  # cosd(heading)
        sin = np.sin(np.deg2rad(heading))  # sind(heading)
        xp = x * cos - y * sin
        yp = x * sin + y * cos

        # Set state string
        zero[7] = str(xp)
        zero[8] = str(yp)
        zero[12] = str(heading)
        state = "\n".join(zero)

        return state

    for i in range(n_main):
        fname = os.path.join(proteus_directory, f"Main_Float{i}.dat")
        with open(fname, "w") as f:
            state = create_state(coords, "main", i)
            f.write(state)

    for i in range(n_long):
        fname = os.path.join(proteus_directory, f"Long_Float{i}.dat")
        with open(fname, "w") as f:
            state = create_state(coords, "long", i)
            f.write(state)

    for i in range(n_small):
        fname = os.path.join(proteus_directory, f"Small_Float{i}.dat")
        with open(fname, "w") as f:
            state = create_state(coords, "small", i)
            f.write(state)


def create_env(proteus_directory):
    """Writes a basic environment file"""

    fname = os.path.join(proteus_directory, "env.ini")
    with open(fname, "w") as f:
        f.write(lb.ENV)


def create_sim(proteus_directory, nrows, ncols):
    """Writes the simulation file, which includes the time deltas and
    a list of rigid bodies and their connections.
    """

    n_main, n_small, n_long = n_floats(nrows, ncols)
    # Number of extra or less small or long floats than number of main
    nrows_sub = nrows + 1
    ncols_sub = ncols - 1

    fname = os.path.join(proteus_directory, "sim.ini")
    with open(fname, "w") as f:
        f.write(lb.SIM)

        ## Write DObjects
        base = "$DObjects RigidBody "
        for i in range(n_main):
            f.write(base + f"Main_Float{i}\n")
        for i in range(n_long):
            f.write(base + f"Long_Float{i}\n")
        for i in range(n_small):
            f.write(base + f"Small_Float{i}\n")

        ## Write Connections
        # Fill in the connections by rows
        # Connect small floats to long floats
        base = "$Connections "
        for j_long in range(nrows_sub):
            j_row = j_long * ncols_sub
            j_row_small = j_long * ncols
            for i_long in range(ncols_sub):
                long_float = f"Long_Float{i_long+j_row} "
                small_float_left = f"Small_Float{i_long+j_row_small} "
                small_float_right = f"Small_Float{i_long+j_row_small+1} "
                connection_left = (long_float + small_float_left).replace(" ", "_")
                connection_right = (long_float + small_float_right).replace(" ", "_")

                f.write(
                    base
                    + long_float
                    + small_float_left
                    + connection_left
                    + "top-left\n"
                )
                f.write(
                    base
                    + long_float
                    + small_float_left
                    + connection_left
                    + "bot-left\n"
                )
                f.write(
                    base
                    + long_float
                    + small_float_right
                    + connection_right
                    + "top-right\n"
                )
                f.write(
                    base
                    + long_float
                    + small_float_right
                    + connection_right
                    + "bot-right\n"
                )

        # Connect small floats to main floats
        for j_main in range(nrows):
            j_row = j_main * ncols
            for i_main in range(ncols):
                main_float = f"Main_Float{i_main+j_row} "
                small_float_bot = f"Small_Float{i_main+j_row} "
                small_float_top = f"Small_Float{i_main+j_row+ncols} "
                connection_bot = (main_float + small_float_bot).replace(" ", "_")
                connection_top = (main_float + small_float_top).replace(" ", "_")

                f.write(
                    base + main_float + small_float_bot + connection_bot + "bot-left\n"
                )
                f.write(
                    base + main_float + small_float_bot + connection_bot + "bot-right\n"
                )
                f.write(
                    base + main_float + small_float_top + connection_top + "top-left\n"
                )
                f.write(
                    base + main_float + small_float_top + connection_top + "top-right\n"
                )

        # Connect main floats to long floats
        for j_long in range(nrows_sub):
            j_row = j_long * ncols_sub
            j_row_main = j_long * ncols
            for i_long in range(ncols_sub):
                long_float = f"Long_Float{i_long+j_row} "
                main_float_top_left = f"Main_Float{i_long+j_row_main} "
                main_float_top_right = f"Main_Float{i_long+j_row_main+1} "
                main_float_bot_left = f"Main_Float{i_long+j_row_main-ncols} "
                main_float_bot_right = f"Main_Float{i_long+j_row_main-ncols+1} "
                connection_top_left = (long_float + main_float_top_left).replace(
                    " ", "_"
                )
                connection_top_right = (long_float + main_float_top_right).replace(
                    " ", "_"
                )
                connection_bot_left = (long_float + main_float_bot_left).replace(
                    " ", "_"
                )
                connection_bot_right = (long_float + main_float_bot_right).replace(
                    " ", "_"
                )

                if j_long < nrows:
                    f.write(
                        base
                        + long_float
                        + main_float_top_left
                        + connection_top_left
                        + "top-left\n"
                    )
                    f.write(
                        base
                        + long_float
                        + main_float_top_right
                        + connection_top_right
                        + "top-right\n"
                    )
                if j_long != 0:
                    f.write(
                        base
                        + long_float
                        + main_float_bot_left
                        + connection_bot_left
                        + "bot-left\n"
                    )
                    f.write(
                        base
                        + long_float
                        + main_float_bot_right
                        + connection_bot_right
                        + "bot-right\n"
                    )


def create_lib(
    proteus_directory, nrows, ncols, floats, solar_panel, connections, joints
):
    """Writes the library file, which contains the hydrodynamic parameters of
    rigid bodies and other simulation objects, as well as the connection
    type and coefficients.
    """

    # Write out string versions of the float joint coordinates
    M = joints["main"]
    L = joints["long"]
    S = joints["small"]
    p_main = [
        f"{M[0]} {-M[1]}",  # top left
        f"{M[0]} {M[1]}",  # top right
        f"{-M[0]} {-M[1]}",  # bot left
        f"{-M[0]} {M[1]}",  # bot right
    ]
    p_long = [
        f"{L[0]} {-L[1]}",
        f"{L[0]} {L[1]}",
        f"{-L[0]} {-L[1]}",
        f"{-L[0]} {L[1]}",
    ]
    p_small = [
        f"{S[0]} {-S[1]}",
        f"{S[0]} {S[1]}",
        f"{-S[0]} {-S[1]}",
        f"{-S[0]} {S[1]}",
    ]

    # Number of extra or less small or long floats than number of main
    nrows_sub = nrows + 1
    ncols_sub = ncols - 1
    stiffness = (
        connections["stiffness"]["translational"],
        connections["damping"]["translational"],
        connections["stiffness"]["rotational"],
        connections["damping"]["rotational"],
    )

    fname = os.path.join(proteus_directory, "lib.ini")
    with open(fname, "w") as f:
        ## Write general library file
        f.write(lb.LIB)

        # Write platform components
        f.write(
            lf.SMALL_LIB(
                floats["dimensions"]["small"],
                floats["cA"]["small"],
                floats["cD"]["small"],
            )
        )
        f.write(lf.SMALL_WIND_LIB(floats["dimensions"]["small"], floats["cD_wind"]))

        f.write(
            lf.LONG_LIB(
                floats["dimensions"]["long"], floats["cA"]["long"], floats["cD"]["long"]
            )
        )
        f.write(lf.LONG_WIND_LIB(floats["dimensions"]["long"], floats["cD_wind"]))

        f.write(
            lf.MAIN_LIB(
                floats["dimensions"]["main"],
                floats["cA"]["main"],
                floats["cD"]["main"],
                "main_float",
            )
        )
        f.write(
            lf.MAIN_LIB(
                floats["dimensions"]["main"],
                floats["cA"]["main_panel"],
                floats["cD"]["main_panel"],
                "main_panel_float",
            )
        )
        f.write(lf.SOLAR_PANEL_LIB(solar_panel["dims"], solar_panel["cD"]))
        f.write(lf.MAIN_WIND_LIB(floats["dimensions"]["main"], floats["cD_wind"]))

        ## Write Connections for Long Floats to Small Floats
        # Connection name is based off long float.
        # top-left of long float connects to top-right of small float
        # [top-left, bot-left, top-right, bot-right]
        p_long_order = [p_long[0], p_long[2], p_long[1], p_long[3]]
        # [top-right, bot-right, top-left, bot-left]
        p_small_order = [p_small[1], p_small[3], p_small[0], p_small[2]]

        # Fill in the connections by rows
        for j_long in range(nrows_sub):
            j_row = j_long * ncols_sub
            j_row_small = j_long * ncols
            for i_long in range(ncols_sub):
                long_float = f"Long_Float{i_long+j_row} "
                small_float_left = f"Small_Float{i_long+j_row_small} "
                small_float_right = f"Small_Float{i_long+j_row_small+1} "
                connection_left = (long_float + small_float_left).replace(" ", "_")
                connection_right = (long_float + small_float_right).replace(" ", "_")

                connection_names = [
                    connection_left + "top-left",
                    connection_left + "bot-left",
                    connection_right + "top-right",
                    connection_right + "bot-right",
                ]
                for i, nm in enumerate(connection_names):
                    master = p_long_order[i] + " 0 0 0 0"
                    follower = p_small_order[i] + " 0 0 0 0"
                    f.write(
                        lf.CONNECTION_LIB(
                            nm, master, follower, "1 1 1 0 1 1", stiffness
                        )
                    )

        ## Write Connections for Main Floats to Small Floats
        # Connection name is based off main float.
        # top-left of long float connects to bot-left of small float
        # [bot-left, bot-right, top-left, top-right]
        p_main_order = [p_main[2], p_main[3], p_main[0], p_main[1]]
        # [top-left, top-right, bot_left, bot_right]
        p_small_order = [p_small[0], p_small[1], p_small[2], p_small[3]]

        for j_main in range(nrows):
            j_row = j_main * ncols
            for i_main in range(ncols):
                main_float = f"Main_Float{i_main+j_row} "
                small_float_bot = f"Small_Float{i_main+j_row} "
                small_float_top = f"Small_Float{i_main+j_row+ncols} "
                connection_bot = (main_float + small_float_bot).replace(" ", "_")
                connection_top = (main_float + small_float_top).replace(" ", "_")

                connection_names = [
                    connection_bot + "bot-left",
                    connection_bot + "bot-right",
                    connection_top + "top-left",
                    connection_top + "top-right",
                ]
                for i, nm in enumerate(connection_names):
                    master = p_main_order[i] + " 0 0 0 0"
                    follower = p_small_order[i] + " 0 0 0 0"
                    f.write(
                        lf.CONNECTION_LIB(
                            nm, master, follower, "1 1 1 1 0 1", stiffness
                        )
                    )

        ## Write Connections for Long Floats to Main Floats
        # Connection name is based off long float.
        # top-left of long float connects to bot-right of main float
        # [top-left, top-right, bot-left, bot-right]
        p_long_order = [p_long[0], p_long[1], p_long[2], p_long[3]]
        # [bot-right, bot-left, top-right, top-left]
        p_main_order = [p_main[3], p_main[2], p_main[1], p_main[0]]

        # Fill in the connections by rows
        for j_long in range(nrows_sub):
            j_row = j_long * ncols_sub
            j_row_main = j_long * ncols
            for i_long in range(ncols_sub):
                long_float = f"Long_Float{i_long+j_row} "
                main_float_top_left = f"Main_Float{i_long+j_row_main} "
                main_float_top_right = f"Main_Float{i_long+j_row_main+1} "
                main_float_bot_left = f"Main_Float{i_long+j_row_main-ncols} "
                main_float_bot_right = f"Main_Float{i_long+j_row_main-ncols+1} "
                connection_top_left = (long_float + main_float_top_left).replace(
                    " ", "_"
                )
                connection_top_right = (long_float + main_float_top_right).replace(
                    " ", "_"
                )
                connection_bot_left = (long_float + main_float_bot_left).replace(
                    " ", "_"
                )
                connection_bot_right = (long_float + main_float_bot_right).replace(
                    " ", "_"
                )
                connection_names = [
                    connection_top_left + "top-left",
                    connection_top_right + "top-right",
                    connection_bot_left + "bot-left",
                    connection_bot_right + "bot-right",
                ]

                for i, nm in enumerate(connection_names):
                    if (j_long >= nrows) & ("top" in nm):
                        continue
                    if (j_long == 0) & ("bot" in nm):
                        continue
                    master = p_long_order[i] + " 0 0 0 0"
                    follower = p_main_order[i] + " 0 0 0 0"
                    f.write(
                        lf.CONNECTION_LIB(
                            nm, master, follower, "1 1 1 1 1 1", stiffness
                        )
                    )


def create_thrusters(proteus_directory, thruster):
    """Creates and appends thruster tiles and parameters to those already
    created for the floats.
    """

    # ABA connection initial state: velocity, angle
    initial_state = [0, 0]

    def create_state(coords):
        zero = lt.STATE_ZERO.split("\n")
        zero[1] = str(coords[0])
        zero[2] = str(coords[1])
        state = "\n".join(zero)
        return state

    if not thruster["n"]:
        return

    for i in range(thruster["n"]):
        fname = os.path.join(proteus_directory, f"Thruster{i}.dat")
        with open(fname, "w") as f:
            state = create_state(initial_state)
            f.write(state)

        fname = os.path.join(proteus_directory, f"Thruster{i}.ini")
        with open(fname, "w") as f:
            name = thruster["name"] + "_" + str(i)
            f.write(lt.THRUSTER(name, thruster["body"], thruster["mass"]))

        fname = os.path.join(proteus_directory, "sim.ini")
        with open(fname, "a") as f:
            f.write(f"$DObjects RigidBody Thruster{i}\n")
            a = thruster["float_pairs"][i]  # ex: Small_Float0
            f.write(f"$Connections {a} Thruster{i} {a}_Thruster{i}_ABA\n")

    fname = os.path.join(proteus_directory, "lib.ini")
    with open(fname, "a") as f:
        ## Write thruster components

        # Blue Robotics T200 Thruster
        motor_rpms = np.unique(list(thruster["rpm"].values()))
        if thruster["name"] == "blue_robotics_t200":
            for ky, val in thruster["rpm"].items():
                f.write(lt.THRUSTER_T200_LIB(ky, val))  # thruster
            f.write(lt.T200_LIB)  # thruster frame

        # Blue Robotics T500 Thruster
        if thruster["name"] == "blue_robotics_t500":
            for ky, val in thruster["rpm"].items():
                f.write(lt.THRUSTER_T200_LIB(ky, val))
            f.write(lt.T500_LIB)

        # Thruster connection joint properties
        f.write(lt.THRUSTER_JOINT_PROP_LIB)
        # Thruster connections - allows thruster to spin below main float
        for i in range(thruster["n"]):
            a = thruster["float_pairs"][i]  # ex: Small_Float0
            nm = f"{a}_Thruster{i}_ABA"
            # Convert list of floats to string
            loc = " ".join(str(e) for e in thruster["float_location"][i])
            master = loc + " 0 0 " + str(thruster["angle"][i])
            follower = "0 0 0 0 0 0"
            axis = 0
            f.write(lt.CONNECTION_LIB(nm, master, follower, axis))
