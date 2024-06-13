"""
ProteusDS thruster file definitions.
"""

STATE_ZERO = "<state>\n0\n0\n</state>\n"

THRUSTER = (
    lambda name, body, mass: f"// Mass properties\n\
$Ix 0.001\n\
$Iy 0.001\n\
$Iz 0.001\n\
$Ixy 0\n\
$Ixz 0\n\
$Iyz 0\n\
$DefineInertiaAboutCG 0\n\
$CGPosition 0 0 0\n\
$Mass {mass}\n\
\n\
// Numerical\n\
$Kinematic 0\n\
\n\
$Thruster {name} 0 0 0 0 0 0\n\
$Cylinder {body} 0 0 0 0 90 0\n"
)

THRUSTER_T200_LIB = (
    lambda name, rpm: f'<blue_robotics_t200_{name} type="RigidBodyThruster">\n\
// https://bluerobotics.com/store/thrusters/t100-t200-thrusters/t200-thruster-r2-rp/\n\
// @ 12 V\n\
// current = 17 A\n\
// rev/min = 3000 -> rev/s = 50 -> rad/s = 50/(2pi) = 314.2\n\
// rotor diameter = 0.076 m\n\
// hub diameter = 0.04 m\n\
// effective diameter = sqrt(0.076^2 - 0.04^2) = 0.065\n\
// thrust = 3.71 kg\n\
// prop pitch at 75% of radius = 22.5 deg\n\
// prop area = pi * ((0.076/2)^2 - (0.04/2)^2) = 0.00330 m^2\n\
// theoretical max flow speed = 3.18 m/s = 50 * (.75 * pi * 0.065 * tan(22.5))\n\
// theoretical flow rate = 3.18 m/s * 0.00330 m^2 = 0.0105 m^3/s\n\
// theoretical fluid power = 1/2 * 1000 kg/m^3 * 3.18 m/s ** 2 * 0.0105 m^3/s = 53.1 W\n\
// theoretical torque = 53.1 W / 314.2 rad/s = 0.169 Nm\n\
\n\
// Fluid\n\
$FluidModel 0\n\
\n\
// General\n\
$ThrusterType 0\n\
$RPMControlMode 0\n\
$RPM {rpm}\n\
\n\
// Propeller\n\
$Diameter 0.065\n\
$TorqueCoefficient 0 0.0583  // 0.169 / (rho * 50^2 * 0.065^5)\n\
$ThrustCoefficient 0 0.816  // (3.71 * 9.81) / (rho * 50^2 * 0.065^4)\n\
$TorqueCoefficient 0.98 0  // advance ratio @ max flow speed = v/nD = 3.18/(50*0.065) \n\
$ThrustCoefficient 0.98 0  // \n\
</blue_robotics_t200_{name}>\n\n'
)

T200_LIB = '<t200_body type="RigidBodyCylinder">\n\
// Added Mass Coefficients\n\
$CaAxial 0\n\
$CaNormal 0\n\
\n\
// Dimensions\n\
$Diameter 0.100\n\
$Length 0.113\n\
\n\
// Drag Coefficients\n\
$CDt 0\n\
$CdAxial 0\n\
$CdNormal 0\n\
\n\
// Fluid loading\n\
$WindLoading 0\n\
$HydroLoading 0\n\
$HydrostaticFroudeKrylov 0\n\
\n\
// Mesh\n\
$AxialSegments 3\n\
$RadialSegments 1\n\
$AngularSegments 8\n\
\n\
// Soil loading\n\
$SoilLoading 0\n\
</t200_body>\n\n'

THRUSTER_T500_LIB = (
    lambda name, rpm: f'<blue_robotics_t500_{name} type="RigidBodyThruster">\n\
// https://bluerobotics.com/store/thrusters/t100-t200-thrusters/t500-thruster/\n\
// @ 24 V\n\
// current = 43.5 A\n\
// rev/min = 3100 -> rev/s = 51.67 -> rad/s = 51.67/(2pi) = 324.6\n\\n\
// rotor diameter = 0.1145 m\n\
// hub diameter = 0.062 m\n\
// effective diameter = sqrt(0.1145^2 - 0.062^2) = 0.0963\n\
// thrust = 16.1 kg\n\
// prop pitch at 75% of radius = 22.5 deg\n\
// prop area = pi * ((0.1145/2)^2 - (0.062/2)^2) = 0.00728 m^2\n\
// theoretical max flow speed = 4.86 m/s = 51.67 * (.75 * pi * 0.1145 * tan(22.5))\n\
// theoretical flow rate = 4.86 m/s * 0.00728 m^2 = 0.0354 m^3/s\n\
// theoretical fluid power = 1/2 * 1000 kg/m^3 * 4.86 m/s ^ 2 * 0.0354 m^3/s = 418 W\n\
// theoretical torque = 418 W / 324.6 rad/s = 1.29 Nm\n\
\n\
// Fluid\n\
$FluidModel 0\n\
\n\
// General\n\
$ThrusterType 0\n\
$RPMControlMode 0\n\
$RPM {rpm}\n\
\n\
// Propeller\n\
$Diameter 0.1145\n\
$TorqueCoefficient 0 0.0583  // 1.29 / (rho * 51.67^2 * 0.0963^5)\n\
$ThrustCoefficient 0 0.688  // (16.1 * 9.81) / (rho * 51.67^2 * 0.0963^4)\n\
$TorqueCoefficient 0.98 0  // advance ratio @ max flow speed = v/nD = 4.86/(51.67*0.0963) \n\
$ThrustCoefficient 0.98 0  // \n\
</blue_robotics_t500_{name}>\n\n'
)

T500_LIB = '<t500_body type="RigidBodyCylinder">\n\
// Added Mass Coefficients\n\
$CaAxial 0\n\
$CaNormal 0\n\
\n\
// Dimensions\n\
$Diameter 0.141\n\
$Length 0.160\n\
\n\
// Drag Coefficients\n\
$CDt 0\n\
$CdAxial 0\n\
$CdNormal 0\n\
\n\
// Fluid loading\n\
$WindLoading 0\n\
$HydroLoading 0\n\
$HydrostaticFroudeKrylov 0\n\
\n\
// Mesh\n\
$AxialSegments 3\n\
$RadialSegments 1\n\
$AngularSegments 8\n\
\n\
// Soil loading\n\
$SoilLoading 0\n\
</t500_body>\n\n'

CONNECTION_LIB = (
    lambda name, master_loc, follower_loc, axis: f'<{name} type="RigidBodyRigidBodyABAConnection">\n\
// Mechanical\n\
$MasterConnectionLocation {master_loc}\n\
$FollowerConnectionLocation {follower_loc}\n\
$Joint 1\n\
$RevoluteJointAngular jointProperties\n\
$FollowerJointAxis {axis}\n\
</{name}>\n\n'
)

THRUSTER_JOINT_PROP_LIB = '<jointProperties type="RigidBodyABAConnectionJoint">\n\
// Applied loads\n\
$TJoint 0\n\
$TaJoint 0\n\
$TfJoint 0\n\
\n\
// End stop settings\n\
$EJoint 0\n\
$E0Joint 0\n\
\n\
// End stop stiffness and damping\n\
$KEJoint 0\n\
$CEJoint 0\n\
\n\
// Joint stiffness and damping\n\
$KJoint 0\n\
$CJoint 0\n\
\n\
// Resistive joint load settings\n\
$FRJoint 0\n\
$FRPDeadBand 0\n\
$FRNDeadBand 0\n\
$FRPJoint 0\n\
$FRPKJoint 0\n\
$FRPCJoint 0 0\n\
$FRNJoint 0\n\
$FRNKJoint 0\n\
$FRNCJoint 0 0\n\
</jointProperties>\n\n'
