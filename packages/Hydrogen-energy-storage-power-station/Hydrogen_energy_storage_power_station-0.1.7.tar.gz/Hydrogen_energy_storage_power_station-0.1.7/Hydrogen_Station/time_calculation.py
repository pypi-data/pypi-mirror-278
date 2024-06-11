import datetime
import pandas as pd


def data_density(dens):
    if dens == "day":
        return 1
    elif dens == "hour":
        return 2
    elif dens == "30min":
        return 3
    elif dens == "15min":
        return 4
    elif dens == "min":
        return 5
    elif dens == "sec":
        return 6
    else:
        print("data density error")
        exit()


# day calculation
def calc_day(year, month, day):
    date = datetime.date(int(year), int(month), int(day))
    total_day = date.timetuple().tm_yday
    # print(f"{raw_data}是第{total_day}天")
    return total_day


# hour calculation
def calc_hour(year, month, day, hour):
    date = datetime.date(int(year), int(month), int(day))
    total_day = date.timetuple().tm_yday
    total_hour = (total_day - 1) * 24 + (int(hour) + 1)
    # print(f"{raw_data} {raw_hour} 是第{total_hour}小时")
    return total_hour


# 30 min calculation
def calc_30min(year, month, day, hour, min):
    date = datetime.date(int(year), int(month), int(day))
    total_day = date.timetuple().tm_yday
    if min == "00":
        total_30min = (total_day - 1) * 24 + int(hour) * 2
    elif min == "30":
        total_30min = (total_day - 1) * 24 + int(hour) * 2 + 1
    else:
        print("data time error")
        exit()
    return total_30min


def generate_timestamps_for_year(year):
    start_date = pd.to_datetime(str(year) + '-1-1 00:00:00')
    end_date = pd.to_datetime(str(year) + '-12-31 23:59:00')

    date_range = pd.date_range(start=start_date, end=end_date, freq='h')
    date_year = date_range.strftime('%Y-%m-%d %HH:%MM:%ss')
    date_year = pd.DataFrame(date_year)
    return date_year



# if __name__ == '__main__':
#     raw_data = input("请输入年月日格式如2023-11-12：")
#     raw_hour = input("请输入24小时时间格式如13：23：19: ")
#     year, month, day = raw_data.split("-")
#     hour, min, sec = raw_hour.split(":")
#     calc_day(year, month, day)
#     calc_hour(year, month, day, hour)
