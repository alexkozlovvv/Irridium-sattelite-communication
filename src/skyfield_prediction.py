#!/usr/bin/python
from datetime import datetime

from satellites_skyfield import Satellites
import pandas as pd
from pytz import timezone

CONFIG_FILE = '../configs/config.yaml'
TLE_FILE = '../configs/iridium.tle'


def main():
    satellites_class = Satellites(CONFIG_FILE, TLE_FILE)
    # satellites_class.show_satellites_list()
    satellite = satellites_class.get_satellite_by_name('IRIDIUM 103')
    print(satellite)
    print(satellites_class.get_satellite_lat_lon(satellite))

    print("*** PREDICTION FOR THIS SATELLITE ***")
    time, events = satellites_class.predict_satellite_pass(satellite)
    if len(events):
        for ti, event in zip(time, events):
            name = (f'rise above {satellites_class.elevation_deg}°',
                    'culminate', f'set below {satellites_class.elevation_deg}°')[event]
            print(ti.utc_strftime('%d-%b-%Y %H:%M:%S'), name)
    else:
        print("No passes :(")

    print(f'\n\n\n\n*** PREDICTION FOR ALL SATELLITES ***\n'
          f'!!!! THIS IS UTC TIME !!!!\n'
          f'*** ELEVATION DEGREE IS {satellites_class.elevation_deg}° ***')
    data = []
    for sat in satellites_class.satellites_tle:
        # time, events = satellites_class.predict_satellite_pass(sat,
        #                   start_time=datetime(2023, 4, 1, 17, 0, 0, tzinfo=timezone('utc')), prediction_hours=24)
        time, events = satellites_class.predict_satellite_pass(sat)
        if len(events):
            for i in range(0, int(len(time) / 3)):
                t_raise, t_max, t_fall, sat_raise_azimuth, sat_max_azimuth, sat_fall_azimuth = [0, 0, 0, 0, 0, 0]
                try:
                    tz = timezone('Europe/Moscow')
                    t_raise = time[0 + i * 3].astimezone(tz).strftime('%d-%b-%Y %H:%M:%S')
                    t_max = time[1 + i * 3].astimezone(tz).strftime('%d-%b-%Y %H:%M:%S')
                    t_fall = time[2 + i * 3].astimezone(tz).strftime('%d-%b-%Y %H:%M:%S')
                    # t_raise = time[0 + i * 3].astimezone(tz).strftime('%H:%M:%S')
                    # t_max = time[1 + i * 3].astimezone(tz).strftime('%H:%M:%S')
                    # t_fall = time[2 + i * 3].astimezone(tz).strftime('%H:%M:%S')
                    sat_raise_azimuth = satellites_class.get_satellite_azimuth(sat, time[0 + i * 3])
                    sat_max_azimuth = satellites_class.get_satellite_azimuth(sat, time[1 + i * 3])
                    sat_fall_azimuth = satellites_class.get_satellite_azimuth(sat, time[2 + i * 3])
                except (IndexError, ValueError):
                    print('events != 3')
                print(
                    f'{sat.name}: T-raise {t_raise} |'
                    f' T-max {t_max} | T-fall {t_fall} |'
                    f' Raise azimuth {sat_max_azimuth} |'
                    f' Max azimuth {sat_max_azimuth} |'
                    f' Fall azimuth {sat_fall_azimuth}')
                data.append((sat.name, str(t_raise), str(t_max), str(t_fall),
                             sat_raise_azimuth, sat_max_azimuth, sat_fall_azimuth))

    df = pd.DataFrame(data, columns=['satellite name', 'T-raise', 'T-max', 'T-fall',
                                     'Raise azimuth', 'Max azimuth', 'Fall azimuth'])
    df.to_excel('../satellites_prediction.xlsx', sheet_name='sheet1', index=False)

    print(satellites_class.spectator_location)


if __name__ == '__main__':
    main()
