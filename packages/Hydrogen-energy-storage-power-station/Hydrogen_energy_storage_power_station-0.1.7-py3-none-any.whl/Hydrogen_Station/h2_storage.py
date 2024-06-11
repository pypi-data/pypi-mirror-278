# 计算储氢罐的压力
def h2_storage(nH2_in, nH2_out):

    # 理想气体常数(j/mol*K)
    R = 8.314
    # 储氢罐体积(100W立方)
    V = 1e6
    # 储氢罐温度(K)
    T_tank = 30 + 273.15
    # 储氢罐初始压力(Pa)
    Pi = 6e6

    # 储氢罐初始氢气摩尔量(mol)
    nH2_initial = Pi * V / (R * T_tank)
    # 储氢罐注入氢气摩尔量(mol)
    nH2_in_mol = nH2_in/0.022414
    # 储氢罐输出氢气摩尔量(mol)
    nH2_out_mol = nH2_out/0.022414
    # 储氢罐内氢气摩尔量(mol)
    nH2_mol = nH2_initial + nH2_in_mol - nH2_out_mol
    # 储氢罐内压力(Pa)
    P = nH2_mol * (R * T_tank) / V

    if P < 0:
        print("Hydrogen reserves lower than 0 MPa")
    elif P > 1e7:
        print("Hydrogen reserves higher than 10 MPa")

    return P


# 计算储氢罐的压力变化
def h2_storage_change(nH2_in, nH2_out, T_tank, timestep):     # timestep是时间间隔，以小时为单位
    # 理想气体常数(j/mol*K)
    R = 8.314
    # 储氢罐体积(100W立方)
    V = 1e6
    # 储氢罐温度(K)
    # T_tank = 30 + 273.15

    # 储氢罐注入氢气摩尔流量(mol/h)
    nH2_in_mol = nH2_in / 0.022414
    # 储氢罐输出氢气摩尔流量(mol/h)
    nH2_out_mol = nH2_out / 0.022414
    # 储氢罐氢气变化摩尔量(mol)
    nH2_mol_change = nH2_in_mol*timestep - nH2_out_mol*timestep
    # 储氢罐压力变化量(Pa)
    P_change = nH2_mol_change * (R * T_tank) / V

    return P_change
