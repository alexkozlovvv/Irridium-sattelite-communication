#!/usr/bin/python

from pyorbital import orbital
from datetime import datetime, timezone, timedelta
import os
from read_config import Configfile
# import pandas as pd
from matplotlib import rc


font = {'family': 'normal',
        'size': 8}

rc('font', **font)


def main():
    config_store = Configfile('../configs/config.yaml')
    longitude = config_store.get_param('longitude')
    latitude = config_store.get_param('latitude')
    altitude = config_store.get_param('altitude')
    tolerance = config_store.get_param('tolerance')
    elevation_deg = config_store.get_param('elevation_deg')
    hours_predict = config_store.get_param('hours_predict')

    tle_filepath = os.sep.join([os.path.dirname(os.path.abspath(__file__)), '../configs/iridium.tle'])

    SAT_LIST = list()
    with open(tle_filepath, 'r') as f:
        count = 0
        for line in f:
            if count % 3 == 0:
                SAT_LIST.append(line.rstrip('\n'))
            count += 1
    print(SAT_LIST)
    start_date = datetime.now(timezone.utc) - timedelta(minutes=10)
    print(start_date)
    data = []
    for satellite in SAT_LIST:
        new = orbital.Orbital(satellite, tle_filepath)
        passes = new.get_next_passes(start_date, hours_predict, longitude, latitude, altitude, tolerance, elevation_deg)
        for next_pass in passes:
            t_raise = next_pass[0].replace().astimezone(tz=None)
            t_fall = next_pass[1].replace().astimezone(tz=None)
            t_max = next_pass[2].replace().astimezone(tz=None)
            observ_list = tle_satellite.get_observer_look(next_pass[2], longitude, latitude, altitude)
            max_elevation_deg = observ_list[1]
            azimuth_max_elevation_deg = observ_list[0]
            print(
                f'{satellite}: T-raise {t_raise} '
                f'| T-max {t_max} '
                f'| T-fall {t_fall} '
                f'| max elevation {max_elevation_deg} '
                f'| azimuth {azimuth_max_elevation_deg}')
            data.append(
                (satellite, max_elevation_deg, str(t_max), str(t_raise), str(t_fall), azimuth_max_elevation_deg))
    # df = pd.DataFrame(data, columns=['satellite', 'max_elevation_deg', 't_max', 't_raise', 't_fall',
    #                                  'azimuth_max_elevation_deg'])
    # df.to_excel('testexternal.xlsx', sheet_name='sheet1', index=False)


if __name__ == '__main__':
    main()
