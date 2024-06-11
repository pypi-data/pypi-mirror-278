import pandas as pd
import json


def read_json(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


# 生成电站发电计划
def power_station_load():
    json = read_json('power_control_par.json')
    grid_out_time = json['grid_out_time']
    grid_out_deep_power = json['grid_out_deep_power']
    grid_out_valley_power = json['grid_out_valley_power']
    grid_out_power = json['grid_out_power']
    grid_out_peak_power = json['grid_out_peak_power']
    grid_out_top_power = json['grid_out_top_power']
    power_time = json['power_time']
    csv = pd.read_csv('init_time_hour.csv')
    times = csv['Datetime'].tolist()
    power_pz = []
    for time in times[0:]:
        t = time.split('/')
        month = t[1]
        hour = int(t[2].split(' ')[1].split(':')[0])
        append_power = 0
        if hour in grid_out_time[month]:
            power_par = power_time[month][hour]
            if power_par == 0:
                append_power = grid_out_power
            elif power_par == 1:
                append_power = grid_out_peak_power
            elif power_par == 2:
                append_power = grid_out_top_power
            elif power_par == -1:
                append_power = grid_out_valley_power
            elif power_par == -2:
                append_power = grid_out_deep_power
        power_pz.append(append_power)
    power_pz = pd.DataFrame([times, power_pz]).T
    power_pz.columns = ['Datetime', 'Output Power']
    # power_pz.to_csv('power_pz.csv', index=False, header=False, encoding='utf-8-sig')
    return power_pz

# if __name__ == '__main__':
#     PowerStationLoad()
