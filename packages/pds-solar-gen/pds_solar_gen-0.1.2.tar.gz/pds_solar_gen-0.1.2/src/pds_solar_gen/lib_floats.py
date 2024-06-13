"""
ProteusDS float file definitions. Some platform parameters are hardcoded in.
"""

# .dat files
# [U, V, W, omegaX, omegaY, omegaZ,
#  X, Y, Z, thetaX (roll), thetaY (pitch), thetaZ(heading)]
STATE_ZERO = "<state>\n\
0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n0\n\
</state>\n"

## .ini files
SMALL = (
    lambda MoI, m: f"// Mass Properties\n\
$Ix {MoI[0]}\n\
$Iy {MoI[1]}\n\
$Iz {MoI[2]}\n\
$Ixy 0\n\
$Ixz 0\n\
$Iyz 0\n\
$DefineInertiaAboutCG 1\n\
$CGPosition 0 0 0\n\
$Mass {m}\n\
\n\
// Numerical \n\
$Kinematic 0\n\
\n\
$Cuboid small_float 0 0 0 0 0 0\n\
$Cuboid small_float_wind 0 0 -0.0785 0 0 0 \n"
)

MAIN = (
    lambda MoI, m: f"// Mass Properties\n\
$Ix {MoI[0]}\n\
$Iy {MoI[1]}\n\
$Iz {MoI[2]}\n\
$Ixy 0\n\
$Ixz 0\n\
$Iyz 0\n\
$DefineInertiaAboutCG 1\n\
$CGPosition 0 0 0\n\
$Mass {m}\n\
\n\
// Numerical \n\
$Kinematic 0\n\
\n\
$Cuboid main_float 0 0 0 0 0 0\n\
$Cuboid main_float_wind 0 0 -0.082 0 0 0\n"
)

MAIN_PANEL = (
    lambda MoI, m, z, pitch: f"// Mass Properties\n\
$Ix {MoI[0]}\n\
$Iy {MoI[1]}\n\
$Iz {MoI[2]}\n\
$Ixy 0\n\
$Ixz 0\n\
$Iyz 0\n\
$DefineInertiaAboutCG 1\n\
$CGPosition 0 0 0\n\
$Mass {m}\n\
\n\
// Numerical \n\
$Kinematic 0\n\
\n\
$Cuboid main_panel_float 0 0 0 0 0 0\n\
$Cuboid main_float_wind 0 0 -0.082 0 0 0\n\
$Cuboid solar_panel 0 0 -{z} {pitch} 0 90\n"
)

LONG = (
    lambda MoI, m: f"// Mass Properties\n\
$Ix {MoI[0]}\n\
$Iy {MoI[1]}\n\
$Iz {MoI[2]}\n\
$Ixy 0\n\
$Ixz 0\n\
$Iyz 0\n\
$DefineInertiaAboutCG 1\n\
$CGPosition 0 0 0\n\
$Mass {m}\n\
\n\
// Numerical \n\
$Kinematic 0\n\
\n\
$Cuboid long_float 0 0 0 0 0 0\n\
$Cuboid long_float_wind 0 0 -0.0795 0 0 0 \n"
)

SMALL_LIB = (
    lambda dim, cA, cD: f'<small_float type="RigidBodyCuboid">\n\
// Added Mass Coefficients\n\
$CAx {cA[0]}\n\
$CAy {cA[1]}\n\
$CAz {cA[2]}\n\
\n\
// Dimensions\n\
$LengthX {dim[0]}\n\
$LengthY {dim[1]}\n\
$LengthZ {dim[2]- 0.002}\n\
\n\
// Drag Coefficients\n\
$CDt {cD[0]}\n\
$CDx {cD[1]}\n\
$CDy {cD[2]}\n\
$CDz {cD[3]}\n\
\n\
// Fluid loading\n\
$WindLoading 0\n\
$HydroLoading 1\n\
$HydrostaticFroudeKrylov 1\n\
\n\
// Mesh\n\
$SegmentsX 2\n\
$SegmentsY 2\n\
$SegmentsZ 1\n\
\n\
// Soil loading\n\
$SoilLoading 1\n\
</small_float>\n\
\n'
)

SMALL_WIND_LIB = (
    lambda dim, cdt: f'<small_float_wind type="RigidBodyCuboid">\n\
// Added Mass Coefficients\n\
$CAx 0.5\n\
$CAy 0.5\n\
$CAz 0.5\n\
\n\
// Dimensions\n\
$LengthX {dim[0]}\n\
$LengthY {dim[1]}\n\
$LengthZ 0.002\n\
\n\
// Drag Coefficients\n\
$CDt {cdt}\n\
$CDx 0\n\
$CDy 0\n\
$CDz 0\n\
\n\
// Fluid loading\n\
$WindLoading 1\n\
$HydroLoading 0\n\
$HydrostaticFroudeKrylov 0\n\
\n\
// Mesh\n\
$SegmentsX 2\n\
$SegmentsY 2\n\
$SegmentsZ 1\n\
\n\
// Soil loading\n\
$SoilLoading 1\n\
</small_float_wind>\n\
\n'
)

MAIN_LIB = (
    lambda dim, cA, cD, name: f'<{name} type="RigidBodyCuboid">\n\
// Added Mass Coefficients\n\
$CAx {cA[0]}\n\
$CAy {cA[1]}\n\
$CAz {cA[2]}\n\
\n\
// Dimensions\n\
$LengthX {dim[0]}\n\
$LengthY {dim[1]}\n\
$LengthZ {dim[2] - 0.002}\n\
\n\
// Drag Coefficients\n\
$CDt {cD[0]}\n\
$CDx {cD[1]}\n\
$CDy {cD[2]}\n\
$CDz {cD[3]}\n\
\n\
// Fluid loading\n\
$WindLoading 0\n\
$HydroLoading 1\n\
$HydrostaticFroudeKrylov 1\n\
\n\
// Mesh\n\
$SegmentsX 2\n\
$SegmentsY 2\n\
$SegmentsZ 1\n\
\n\
// Soil loading\n\
$SoilLoading 1\n\
</{name}>\n\
\n'
)

MAIN_WIND_LIB = (
    lambda dim, cdt: f'<main_float_wind type="RigidBodyCuboid">\n\
// Added Mass Coefficients\n\
$CAx 0.5\n\
$CAy 0.5\n\
$CAz 0.5\n\
\n\
// Dimensions\n\
$LengthX {dim[0]}\n\
$LengthY {dim[1]}\n\
$LengthZ 0.002\n\
\n\
// Drag Coefficients\n\
$CDt {cdt}\n\
$CDx 0\n\
$CDy 0\n\
$CDz 0\n\
\n\
// Fluid loading\n\
$WindLoading 1\n\
$HydroLoading 0\n\
$HydrostaticFroudeKrylov 0\n\
\n\
// Mesh\n\
$SegmentsX 2\n\
$SegmentsY 2\n\
$SegmentsZ 1\n\
\n\
// Soil loading\n\
$SoilLoading 1\n\
</main_float_wind>\n\
\n'
)

SOLAR_PANEL_LIB = (
    lambda dim, cD: f'<solar_panel type="RigidBodyCuboid">\n\
// Added Mass Coefficients\n\
$CAx 0.5\n\
$CAy 0.5\n\
$CAz 1\n\
\n\
// Dimensions\n\
$LengthX {dim[0]}\n\
$LengthY {dim[1]}\n\
$LengthZ {dim[2]}\n\
\n\
// Drag Coefficients\n\
$CDt {cD[0]}\n\
$CDx {cD[1]}\n\
$CDy {cD[2]}\n\
$CDz {cD[3]}\n\
\n\
// Fluid loading\n\
$WindLoading 1\n\
$HydroLoading 0\n\
$HydrostaticFroudeKrylov 0\n\
\n\
// Mesh\n\
$SegmentsX 5\n\
$SegmentsY 5\n\
$SegmentsZ 1\n\
\n\
// Soil loading\n\
$SoilLoading 1\n\
</solar_panel>\n\n'
)

LONG_LIB = (
    lambda dim, cA, cD: f'<long_float type="RigidBodyCuboid">\n\
// Added Mass Coefficients\n\
$CAx {cA[0]}\n\
$CAy {cA[1]}\n\
$CAz {cA[2]}\n\
\n\
// Dimensions\n\
$LengthX {dim[0]}\n\
$LengthY {dim[1]}\n\
$LengthZ {dim[2] - 0.002}\n\
\n\
// Drag Coefficients\n\
$CDt {cD[0]}\n\
$CDx {cD[1]}\n\
$CDy {cD[2]}\n\
$CDz {cD[3]}\n\
\n\
// Fluid loading\n\
$WindLoading 0\n\
$HydroLoading 1\n\
$HydrostaticFroudeKrylov 1\n\
\n\
// Mesh\n\
$SegmentsX 3\n\
$SegmentsY 3\n\
$SegmentsZ 1\n\
\n\
// Soil loading\n\
$SoilLoading 1\n\
</long_float>\n\
\n'
)

LONG_WIND_LIB = (
    lambda dim, cdt: f'<long_float_wind type="RigidBodyCuboid">\n\
// Added Mass Coefficients\n\
$CAx 0.5\n\
$CAy 0.5\n\
$CAz 0.5\n\
\n\
// Dimensions\n\
$LengthX {dim[0]}\n\
$LengthY {dim[1]}\n\
$LengthZ 0.002\n\
\n\
// Drag Coefficients\n\
$CDt {cdt}\n\
$CDx 0\n\
$CDy 0\n\
$CDz 0\n\
\n\
// Fluid loading\n\
$WindLoading 1\n\
$HydroLoading 0\n\
$HydrostaticFroudeKrylov 0\n\
\n\
// Mesh\n\
$SegmentsX 2\n\
$SegmentsY 2\n\
$SegmentsZ 1\n\
\n\
// Soil loading\n\
$SoilLoading 1\n\
</long_float_wind>\n\
\n'
)

CONNECTION_LIB = (
    lambda name, master_loc, follower_loc, constraint, stiffness: f'<{name} type="RigidBodyRigidBodyForceConnection">\n\
// Connection configuration\n\
$MasterConnectionLocation {master_loc}\n\
$FollowerConnectionLocation {follower_loc}\n\
$ActiveConstraintDirection {constraint}\n\
\n\
// Rotational stiffness\n\
$FCRKJoint {stiffness[2]}\n\
$FCRCJoint {stiffness[3]}\n\
\n\
// Translational stiffness\n\
$FCKJoint {stiffness[0]}\n\
$FCCJoint {stiffness[1]}\n\
</{name}>\n\n'
)
