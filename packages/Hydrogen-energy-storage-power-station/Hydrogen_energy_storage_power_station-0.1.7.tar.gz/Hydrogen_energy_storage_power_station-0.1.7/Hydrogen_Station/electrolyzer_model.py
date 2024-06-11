import numpy as np
import os

datadir = os.environ.get('DATADIR')
if not datadir:
    datadir = '/data'


# 电解槽参数
def parameter(Tc):  # Tc是电解槽问题 (℃)
    DELTA_G = 237.2  # Gibbs energy (kJ/mol)
    F = 96485  # F是法拉第常数
    z = 2  # z是电子数量(氢)
    A = 0.18  # A 是电极面积
    s = 0.185  # s 是过电压系数 (V)
    t1 = 1.002  # t1是过电压系数 (A-1·m2)
    t2 = 8.424  # t2是过电压系数 (A-1·m2·℃)
    t3 = 247.3  # t3是过电压系数 (A-1·m2·℃)
    r1 = 8.05e-5  # r1是电解质的欧姆电阻相关的参数 (Ω·m2)
    r2 = -2.5e-7  # r2是电解质的欧姆电阻相关的参数 (Ω·m2·℃-1)
    f1 = 2.5 * Tc + 50  # f1是与法拉第效率相关的参数 (mA2/cm4)
    f2 = -0.00025 * Tc + 1  # f1是与法拉第效率相关的参数 (mA2/cm4)

    return DELTA_G, F, z, A, s, t1, t2, t3, r1, r2, f1, f2


# 电解槽电压计算
def electrolyzer_voltage(i, Tc, nc):  # i是电解槽电流, Tc是电解槽温度 (℃), nc是电解槽串联数量
    DELTA_G, F, z, A, s, t1, t2, t3, r1, r2, f1, f2 = parameter(Tc)

    v_rev = (DELTA_G * 1000) / (z * F)  # reversible cell voltage
    v_act = s * np.log10((t1 + t2 / Tc + t3 / np.square(Tc)) * i / A + 1)  # V_act是激活过电压
    v_ohm = (r1 + r2 * Tc) * i / A  # V_ohm是电解质的欧姆过电压
    v_cell = v_rev + v_act + v_ohm  # V_cell是小室的工作电压
    v_sys = nc * v_cell  # 电解槽电压
    return v_sys


# 电解槽产氢、产氧、耗水计算
def electrolyzer_produce(i, Tc, nc, t):  # i是电解槽电流, Tc是电解槽温度 (℃), nc是电解槽串联数量, t是时间(s)
    delta_G, F, z, A, s, t1, t2, t3, r1, r2, f1, f2 = parameter(Tc)

    nF = np.square(i / A) * f2 / (f1 + np.square(i / A))  # 法拉第效率
    nH2 = nF * i / (z * F)  # 氢气的摩尔流速(mol/s)
    nH2O = nH2  # 水的摩尔流速(mol/s)
    nO2 = 0.5 * nH2  # 氧气的摩尔流速(mol/s)

    nH2_vf = nc * nH2 * t * 0.022414  # volume flow 氢气的产量(Nm3/h)
    nH2O_vf = nc * nH2O * t * 0.018e-3  # 氢气的产量(Nm3/h)
    nO2_vf = nc * nO2 * t * 0.022414  # 氢气的产量(Nm3/h)

    return nH2_vf, nO2_vf, nH2O_vf


def electrolyzer_heat_1(power_in, voltage_in, nc):
    F = 96485  # F是法拉第常数
    z = 2  # z是电子数量(氢)
    DELTA_HHV = 286  # 标准状态下分解水的焓值(高热值) (kJ/mol)
    DELTA_LHV = 242  # 标准状态下分解水的焓值(低热值) (kJ/mol)

    Utn = (DELTA_LHV * 1000) / (z * F)  # 热中性电池电压(几乎不变)

    energy_gen_e = power_in * (1 - (Utn * nc) / voltage_in)
    energy_cool_e = energy_gen_e
    return energy_gen_e


def electrolyzer_heat_2(current_in, voltage_in, power_in, nc):
    F = 96485  # F是法拉第常数
    z = 2  # z是电子数量(氢)
    DELTA_HHV = 286  # 标准状态下分解水的焓值(高热值) (kJ/mol)
    DELTA_LHV = 242  # 标准状态下分解水的焓值(低热值) (kJ/mol)

    Utn = (DELTA_LHV * 1000) / (z * F)  # 热中性电池电压(几乎不变)
    nv = Utn * nc / voltage_in
    ni = 96.5 * np.exp((0.09 / current_in) - (75.5 / current_in)) / 100
    nel = ni * nv
    energy_cool_e = (1 - nel) * power_in
    return energy_cool_e


# 电解槽运行曲线
def power_to_current_curve(Tc, nc, max_i):  # Tc是电解槽温度 (℃), nc是电解槽串联数量, max_i是电解槽输入最大电流
    current = np.array([])  # Current(A)
    voltage = np.array([])  # Voltage(V)
    power = np.array([])  # Power(W)

    for j in range(0, 80000):
        i = float(j) * 0.1
        v = electrolyzer_voltage(i, Tc, nc)
        p = v * i

        current = np.append(current, [i])
        voltage = np.append(voltage, [v])
        power = np.append(power, [p])

    max_p = power[max_i * 10]

    return current, voltage, power, max_p


def save_power_to_current_curve(Tc, nc, max_i):
    current, voltage, power, max_p = power_to_current_curve(Tc, nc, max_i)
    np.savez(os.path.join(datadir, 'parameter', 'power_to_current_curve.npz'), current=current, voltage=voltage,
             power=power, max_p=max_p)


def load_power_to_current_curve():
    loaded_par = np.load(os.path.join(datadir, 'parameter', 'power_to_current_curve.npz'))
    return loaded_par['current'], loaded_par['voltage'], loaded_par['power'], loaded_par['max_p']


# 通过输入功率计算电解槽电流、电压（邻近拟合）
def power_to_current(p, current, voltage, power):  # p是电解槽输入功率, current, voltage, power是电解槽的运行曲线数据
    index = np.abs(power - p).argmin()
    i = current[index]
    v = voltage[index]
    return i, v


if __name__ == '__main__':
    save_power_to_current_curve(95, 60, 6750)
