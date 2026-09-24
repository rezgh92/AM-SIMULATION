"""Thermodynamic and kinetic window for binder burnout next to copper: Cu/Cu2O boundary,
C + H2O = CO + H2 equilibrium, and the char gasification half-life of the model."""
import json, sys
import numpy as np
from cupola import thermo
from cupola.constants import T0C
from cupola.cofire.run import cofire_scenario, glass_view
from cupola.cofire.glass import GlassSetup

s = cofire_scenario()
su = GlassSetup(glass_view(s))
T_C = np.linspace(300, 1000, 141)
T = T_C + T0C
ratio_cu = thermo.h2o_h2_boundary_Cu(T)
K = thermo.K_steam_gasification(T)
pCO = 1e-4
ratio_gas = pCO / K                      # below this pH2O/pH2 steam cannot gasify carbon (p_CO = 1e-4 bar)
# half-life map in (T, log10 ratio) at a steam fraction x_h2o
logr = np.linspace(-2, 8, 201)
maps = {}
for x_h2o in (0.023, 0.3, 0.9):
    x_h2 = x_h2o / 10.0 ** logr
    TT, XH2 = np.meshgrid(T, x_h2, indexing="xy")
    inh = (1.0 + su.K_inh * 0.04) / (1.0 + su.K_inh * np.minimum(XH2, 1.0))
    k = su.k_gasif(TT) * np.sqrt(x_h2o / su.x_h2o_ref) * inh
    maps[str(x_h2o)] = (np.log(2.0) / k / 3600.0).tolist()
# operating points
dp20 = float(thermo.x_h2o_from_dewpoint(20.0))
points = dict(forming_gas_bubbler=dict(ratio=dp20 / 0.04, x_h2o=dp20, label="4 % H2, dew point +20 C"),
              forming_gas_dry=dict(ratio=float(thermo.x_h2o_from_dewpoint(-60.0)) / 0.04, x_h2o=1e-5, label="4 % H2, dry"),
              ibm_1e4=dict(ratio=1e4, label="H2/H2O = 1e-4"))
json.dump(dict(T_C=T_C.tolist(), ratio_cu=ratio_cu.tolist(), ratio_gas=ratio_gas.tolist(), logr=logr.tolist(),
               half_life_h=maps, points=points, pCO=pCO), open(sys.argv[1], "w"))
print("done", float(ratio_cu[np.argmin(abs(T_C-780))]), float(ratio_gas[np.argmin(abs(T_C-780))]))
