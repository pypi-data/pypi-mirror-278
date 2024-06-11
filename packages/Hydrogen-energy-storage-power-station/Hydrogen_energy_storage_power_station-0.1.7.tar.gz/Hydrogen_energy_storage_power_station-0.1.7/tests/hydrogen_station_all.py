import numpy as np
import matplotlib.pyplot as plt
from Hydrogen_Station import karamay_pvwattsv8
from Hydrogen_Station import electrolyzer_model
from Hydrogen_Station import pem_fuelcell_model
from Hydrogen_Station import h2_storage
from Hydrogen_Station import load_generation
from tests import HydrogenParameter

"""
由于电解槽模型不是匹配克拉玛依项目的，电解槽小太多了。设计文档(技术方案)电解槽CDQ-1000的设备的直流电耗4.5MW，
额定电流是6750A，额定电压720V。而目前仿真的电解槽在6750A时（95℃），只能输出4.21V，差距近171倍。
故电解槽模型的串联数量增加165倍，以接近真实的电解槽。
"""
electrolyzer_adjust1 = 171

"""
目前的仿真模型，在电流为6750A，电压为720V时，氢气产量是471.18Nm3/h。
和中船给的设计方案中，CDQ-1000的设备，在额定电流是6750A，额定电压720V下，
产氢量是1000Nm3/h有将近2.12倍的差距（原因不详需要调查），故需要修正2.3倍。
"""
electrolyzer_adjust2 = 2.12

Tc = 95  # Tc是电解槽的温度 (℃)

"""
本项目位于新疆，制氢规模300MW，项目采用以4台1000Nm³/h电解槽对应1套氢气处理量为4000Nm³/h气液分离装置
和1套4000Nm³/h的纯化装置为一套四对一制氢系统，每间厂房配置共5套四对一制氢系统，共计三间厂房，即 60 台 1000Nm³/h 电解槽。
"""
n_e = 4 * 5 * 3  # 电解槽并联套数

m_e = electrolyzer_adjust1  # 电解槽串联个数
year = 2024  # 年份

Tk = 60 + 273  # Tk是燃料电池的温度 (K)

"""
目前燃料电池模型（单个电堆）最大输出功率约为0.607w/cm2（该值是由FuelCell_Power_Current中的max_P得出的），
按280cm2算，约170W，和1MW差了5882倍。故假定当前燃料电池是由5882个单体串联。
"""
n_f = 5882  # 一个1MW的燃料电池组的电堆个数(串联)

m_f = 81  # 燃料电池机组的个数(并联)

A = 280  # 燃料的电池的截面积cm2是参考simulink中的官方模型的默认数值
P_H2 = 3  # 氢气输入压力(atm，一个标准大气压=101325Pa)
P_air = 3  # 空气输入压力(atm)

R = 8.314  # 理想气体常数(j/mol*K)
V = 1e6  # 储氢罐体积(m3)
Tt = 30 + 298  # 储氢罐温度(K)
Pi = 10e6  # 储氢罐初始压力(Pa)

Pt = Pi  # 储氢罐实时压力(Pa)

DELTA_G = 237  # Gibbs energy (kJ/mol)
F = 96485  # F是法拉第常数
z = 2  # z是电子数量(氢)
DELTA_HHV = 286  # 标准状态下分解水的焓值(高热值) (kJ/mol)
DELTA_LHV = 242  # 标准状态下分解水的焓值(低热值) (kJ/mol)

Utn = (DELTA_LHV * 1000) / (z * F)  # 热中性电池电压(几乎不变)

# 系统运行参数记录数组(电解槽)
current_electrolyzer = np.array([])
voltage_electrolyzer = np.array([])

Q_electrolyzer = np.array([])
Q_electrolyzer_1 = np.array([])


P_in_electrolyzer = np.array([])

nH2_electrolyzer = np.array([])
nO2_electrolyzer = np.array([])
nH2O_electrolyzer = np.array([])

# 系统运行参数记录数组(燃料电池)
current_FuelCell = np.array([])
voltage_FuelCell = np.array([])
P_elec_FuelCell = np.array([])
Q_cool_FuelCell = np.array([])
Q_gen_FuelCell = np.array([])
efficiency_FuelCell = np.array([])
nH2_FuelCell = np.array([])

# 系统运行参数记录数组(储氢罐)
P_storage = np.array([])

# 电解槽的功率曲线和功率最大值
current_e, voltage_e, power_e, max_P_e = electrolyzer_model.power_to_current_curve(Tc, m_e, 6750)

# 燃料电池的功率曲线和功率最大值
current_f, voltage_f, power_f, max_P_f = pem_fuelcell_model.power_to_current_curve(Tk, P_H2, P_air)

# 电解槽的输入功率(kW)
power_year_solar = karamay_pvwattsv8.output_power_year(year)  # 输出功率单位是kW
# power_year_solar = [4500, 4000, 3800, 3500]

# 燃料电池的负载功率(kW)
power_year_load = load_generation.power_station_load()  # 负载功率单位是MW
# power_year_load = [1000*81, 900*81, 800*81, 850*81]


# nH2_initial = Pi * V / (R * Tt)  # mol
# nH2_mol = nH2_initial


for i in range(len(power_year_solar)):

    # 将输入功率平均分配到每一台CDQ-1000上
    # power_in = power_year_solar.loc[i, 'Output Power'] * 1000 / n_e / solar_power_adjust  # 单位W
    power_in = power_year_solar.loc[i, 'Output Power'] * 1000 / n_e  # 单位W
    # power_in = power_year_solar[i] * 1000

    if power_in < 0:
        print("error: power input is lower than 0")
        exit()
    elif power_in == 0:
        P_e = 0
        current_in = 0
        voltage_in = 0
        Q_gen_e = 0
        Q_gen_e_1 = 0
    elif power_in > max_P_e:
        P_e = max_P_e
        current_in, voltage_in = electrolyzer_model.power_to_current(P_e, current_e, voltage_e, power_e)
        Q_gen_e = electrolyzer_model.electrolyzer_heat_1(P_e, voltage_in, m_e)
        Q_gen_e_1 = electrolyzer_model.electrolyzer_heat_2(current_in, voltage_in, P_e, m_e)
        # Q_gen_e = max_P_e * (1 - (Utn * m_e) / voltage_in)
        print("warning: power input is higher than maximum input power of electrolyzer")
    else:
        P_e = power_in
        current_in, voltage_in = electrolyzer_model.power_to_current(P_e, current_e, voltage_e, power_e)
        Q_gen_e = electrolyzer_model.electrolyzer_heat_1(P_e, voltage_in, m_e)
        Q_gen_e_1 = electrolyzer_model.electrolyzer_heat_2(current_in, voltage_in, P_e, m_e)
        # Q_gen_e = power_in * (1 - (Utn * m_e) / voltage_in)

    current_electrolyzer = np.append(current_electrolyzer, [current_in])
    voltage_electrolyzer = np.append(voltage_electrolyzer, [voltage_in])

    P_e_all = P_e * n_e
    P_in_electrolyzer = np.append(P_in_electrolyzer, [P_e_all])
    # 将所有CDQ-1000的产热累加在一起
    Q_gen_e_all = Q_gen_e * n_e
    Q_electrolyzer = np.append(Q_electrolyzer, [Q_gen_e_all])

    Q_gen_e_all_1 = Q_gen_e_1 * n_e
    Q_electrolyzer_1 = np.append(Q_electrolyzer_1, [Q_gen_e_all_1])

    # 将所有CDQ-1000的产氢量累加在一起
    nH2_in_vf, nH2O_in_vf, nO2_in_vf = electrolyzer_model.electrolyzer_produce(current_in, Tc, m_e, 3600)

    nH2_in_vf = nH2_in_vf * electrolyzer_adjust2 * n_e
    nH2O_in_vf = nH2O_in_vf * electrolyzer_adjust2 * n_e
    nO2_in_vf = nO2_in_vf * electrolyzer_adjust2 * n_e

    nH2_electrolyzer = np.append(nH2_electrolyzer, [nH2_in_vf])
    nH2O_electrolyzer = np.append(nH2O_electrolyzer, [nH2O_in_vf])
    nO2_electrolyzer = np.append(nO2_electrolyzer, [nO2_in_vf])

    # 将燃料电池的负载平均分配到单个电堆上
    power_out_dens = power_year_load.loc[i, 'Output Power'] * 1e6 / A / n_f / m_f  # W/cm2
    # power_out_dens = power_year_load[i] * 1000 / A / n_f / m_f  # W/cm2

    if power_out_dens < 0:
        print("error: Load requirement is lower than 0")
        exit()
    elif power_out_dens == 0:
        p_f = 0
        current_out_dens = 0
        Q_gen_f = 0
        Q_cool_f = 0
        eff_f = 0
    elif power_out_dens > max_P_f:
        p_f = max_P_f
        current_out_dens, voltage_out = pem_fuelcell_model.power_to_current(p_f, current_f, voltage_f, power_f)
        Q_gen_f, Q_cool_f = pem_fuelcell_model.fuelcell_heat_dens(current_out_dens, p_f)
        # Q_gen_f = p_f * (1 - Utn / voltage_out)
        # Q_gen_f = (current_out_dens * DELTA_LHV * 1000) / (z * F)
        # Q_cool_f = Q_gen_f - p_f
        eff_f = p_f / Q_gen_f
        print("warning: Load requirement is higher than the maximum output power of fuel cell")
    else:
        p_f = power_out_dens
        current_out_dens, voltage_out = pem_fuelcell_model.power_to_current(p_f, current_f, voltage_f, power_f)
        Q_gen_f, Q_cool_f = pem_fuelcell_model.fuelcell_heat_dens(current_out_dens, p_f)
        # Q_gen_f = p_f * (1 - Utn / voltage_out)
        # Q_gen_f = (current_out_dens * DELTA_LHV * 1000) / (z * F)
        # Q_cool_f = Q_gen_f - p_f
        eff_f = p_f / Q_gen_f
    # if power_out_dens == 0:
    #     current_out_dens = 0
    # else:
    #     current_out_dens = curve_P_f(power_out_dens)
    #     voltage_out = curve_V_f(current_out_dens)
    # if current_out_dens < 0:
    #     print("Load requirement is higher than the maximum output power of fuel cell")
    #     # exit()
    #     power_out_dens = 81 * 1e6 / A / n_f / m_f
    #     current_out_dens = curve_P_f(power_out_dens)
    current_out = current_out_dens * A
    current_FuelCell = np.append(current_FuelCell, [current_out])
    voltage_FuelCell = np.append(voltage_FuelCell, [voltage_out])

    p_f_all = p_f * A * n_f * m_f
    P_elec_FuelCell = np.append(P_elec_FuelCell, [p_f_all])

    # 将所有电堆的耗氢量累加到一起
    nH2_out = pem_fuelcell_model.fuelcell_consumption(current_out, 3600) * n_f * m_f  # Nm3/h
    nH2_FuelCell = np.append(nH2_FuelCell, [nH2_out])

    # 将所有燃料电池的产热累加在一起
    # Q_gen_f = (current_out / 2 / 96485) * 48.7
    Q_gen_f_all = Q_gen_f * n_f * m_f * A
    Q_gen_FuelCell = np.append(Q_gen_FuelCell, [Q_gen_f_all])

    Q_cool_f_all = Q_cool_f * n_f * m_f * A
    Q_cool_FuelCell = np.append(Q_cool_FuelCell, [Q_cool_f_all])

    # 计算燃料电池效率
    efficiency_FuelCell = np.append(efficiency_FuelCell, [eff_f])

    # 计算储氢罐的压力变化
    P_change = h2_storage.h2_storage_change(nH2_in_vf, nH2_out, Tt, 1)

    # 计算当前储氢罐的压力
    Pt = Pt + P_change
    # nH2_in_mol = nH2_in / 0.022414
    # nH2_out_mol = nH2_out / 0.022414
    # nH2_mol = nH2_mol + nH2_in_mol - nH2_out_mol
    #
    # Pt = nH2_mol * (R * Tt) / V

    # 判断储氢罐的运行状态
    if Pt < 0:
        print("Hydrogen reserves lower than 0 MPa")
    elif Pt > 1e7:
        print("Hydrogen reserves higher than 10 MPa")
    else:
        print("Hydrogen reserves under control")

    P_storage = np.append(P_storage, [Pt])


print(np.sum(Q_electrolyzer))
print(np.sum(Q_electrolyzer_1))

# 2创建画布和子图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# 绘制第一张图
ax1.plot(Q_electrolyzer_1, color='red', label='electrical power')
ax1.plot(Q_electrolyzer, color='blue', label='total power')
# ax1.plot(Q_cool_FuelCell, color='orange', label='cooling power')
ax1.legend()

# 绘制第二张图
ax2.plot(efficiency_FuelCell, color='blue', label='efficiency_FuelCell')
ax2.legend()

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()

# plt.plot(Q_gen_FuelCell, color='red', label='total power')
# plt.plot(P_elec_FuelCell, color='blue', label='electrical power')
# plt.plot(efficiency_FuelCell, color='blue', label='efficiency_FuelCell')
# plt.legend()
# plt.show()
