# 氧气液化(nO2_vf是氧气的标方, t0是氧气的初始温度, t1是氧气的目标温度, n_eff是冷却系统效率, t是冷却的时间)
def liquid_oxygen_energy(nO2_vf, t0, t1, n_eff, t):
    cp = 0.918  # 氧气的比热容(J/(g·K))
    M_O2 = 32  # 氧气的摩尔质量(g/mol)
    L = 213  # 氧气的液化潜热(J/g)

    nO2 = nO2_vf / 0.022414  # 氧气的摩尔
    m = nO2 * M_O2  # 氧气的质量(g)

    Q_cooling = m * cp * (t0 - t1)
    Q_liquefaction = m * L
    Q_total = Q_cooling + Q_liquefaction

    E = Q_total/n_eff
    P = E/t

    return P



