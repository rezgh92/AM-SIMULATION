"""Physical constants and molar data. SI units throughout (K, s, m, kg, mol, Pa, J)."""

R = 8.314462618          # J/(mol K)
KB = 1.380649e-23        # J/K
SIGMA_SB = 5.670374419e-8  # W/(m^2 K^4)
G_ACC = 9.80665          # m/s^2
P_ATM = 101325.0         # Pa
T0C = 273.15             # K at 0 degC

# Molar masses, kg/mol
M_CU = 63.546e-3
M_O = 15.999e-3
M_C = 12.011e-3
M_H2 = 2.016e-3
M_H2O = 18.015e-3
M_O2 = 31.998e-3
M_N2 = 28.014e-3
M_CO = 28.010e-3
M_CO2 = 44.009e-3

# Condensed-phase densities, kg/m^3
RHO_CU = 8960.0
RHO_CU2O = 6000.0
RHO_CUO = 6310.0
RHO_CHAR = 1800.0        # disordered carbon residue

# Molar volumes per Cu atom, m^3/mol
V_CU = M_CU / RHO_CU                       # 7.09e-6
V_CU_IN_CU2O = (2 * M_CU + M_O) / RHO_CU2O / 2   # 11.93e-6 per Cu
V_CU_IN_CUO = (M_CU + M_O) / RHO_CUO             # 12.61e-6 per Cu

# Copper crystallography / melting (Frost & Ashby 1982, Table 4.1)
OMEGA_CU = 1.18e-29      # atomic volume, m^3
T_MELT_CU = 1357.77      # K (1084.62 degC)

# Cu-O eutectic (monotectic side of Cu-Cu2O): 1066 degC; solid solubility of O in
# Cu at the eutectic is ~0.008 wt% (80 ppm). Above that, liquid forms at 1066 degC.
T_EUTECTIC_CU_O = 1066.2 + T0C
O_SOLIDUS_PPM = 80.0

# Standard gas volume: 1 slpm (0 degC, 1 atm) in mol/s
SLPM_TO_MOLS = P_ATM / (R * T0C) / 1000.0 / 60.0   # 7.436e-4

STD = {
    "HOUR": 3600.0,
    "MIN": 60.0,
}
