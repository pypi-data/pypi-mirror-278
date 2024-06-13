"""
Basic ProteusDS file definitions shared for all simulations.
"""

SIM = "// Instrumentation\n\
$IntervalOutput 0.1\n\
\n\
// Integration\n\
$StartTime 0\n\
$EndTime 10\n\
$Integrator integrator\n"

ENV = "// Air\n\
$AirDensity 1.29\n\
$AirKinematicViscosity 1.568E-05\n\
\n\
// Current\n\
$CurrentProfile 0\n\
$CurrentShielding 0\n\
\n\
// Environment Transition\n\
$EnvironmentTransitionMode 1\n\
$CurrentTransitionMode 0\n\
$WindTransitionMode 0\n\
$WaveTransitionMode 1\n\
$WaveStartTime 10\n\
$WaveRampDuration 10\n\
\n\
// Instrumentation\n\
$WaveStatsProbe 0 0\n\
\n\
// Mean water level\n\
$MeanWaterLevelTransitionMode 0\n\
$MeanWaterLevel 0\n\
\n\
// Seabed\n\
$WaterDepth 5\n\
$CustomBathymetry 0\n\
$SoilProperties environmentSoil\n\
$UseMultipleSoilLayers 0\n\
\n\
// Water\n\
$WaterDensity 1025\n\
$WaterKinematicViscosity 1.8E-06\n\
$FluidDomainPrecision 3\n\
$FluidDomainUpdatePeriod 0.1\n\
\n\
// Wave\n\
$WaveType 0\n\
\n\
// Wind\n\
$WindProfile 4\n"

LIB = '<environmentSoil type="EnvironmentSoil">\n\
// Mechanical\n\
$KNSoil 10000\n\
$CNASoil 100\n\
$MuSoil 0.5\n\
$MuNormalSoil 0\n\
$DeadZoneVel 0.001\n\
</environmentSoil>\n\
\n\
<integrator type="Integrator">\n\
// Integrator parameters\n\
$IntegratorType 1\n\
$TruncationError 0.0001\n\
$InitialTimeStep 0.0001\n\
$MaximumTimeStep 1\n\
$MinimumTimeStep 1E-15\n\
</integrator>\n\
\n\
<segment0 type="DCableSegment">\n\
// Axial Rigidity\n\
$AxialRigidityMode 0\n\
$EA 1000000\n\
\n\
// Damping\n\
$AxialDampingMode 1\n\
$AxialReferenceDampingRatio 0.5\n\
$FlexuralDampingMode 1\n\
$FlexuralReferenceDampingRatio 0.5\n\
$TCID 0\n\
\n\
// Fluid loading\n\
$CDc 1\n\
$CDt 0.01\n\
$CAc 1\n\
\n\
// Mechanical\n\
$EI1 1\n\
$EI2 1\n\
$GJ 0\n\
$Diameter 0.01\n\
$Density 1025\n\
$CE 1\n\
\n\
// Strain Limit\n\
$ElongationLimitMode 0\n\
</segment0>\n\
\n'
