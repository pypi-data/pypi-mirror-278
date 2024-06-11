import matplotlib.pyplot as plt
from Hydrogen_Station import electrolyzer_model_old
from Hydrogen_Station import pem_fuelcell_model

current, voltage, power, max_p = electrolyzer_model_old.power_to_current_curve(95, 1, 6750)

nH2_vf, _, _ = electrolyzer_model_old.electrolyzer_produce(current, 95, 1, 3600)


current_f, voltage_f, power_f, max_P_f = pem_fuelcell_model.power_to_current_curve(60 + 273, 3, 3)





plt.plot(current_f, power_f)
plt.show()

plt.plot(current, power)
plt.show()

plt.plot(power, nH2_vf)
# plt.plot(P_elec_FuelCell, color='blue', label='electrical power')
# plt.plot(efficiency_FuelCell, color='blue', label='efficiency_FuelCell')
# plt.legend()
plt.show()
