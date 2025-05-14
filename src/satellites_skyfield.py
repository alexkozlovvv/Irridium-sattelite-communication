import skyfield.sgp4lib
import skyfield.api
from datetime import timezone, datetime, timedelta
from read_config import Configfile


class Satellites(object):
    """Satellite class based on skyfield library

    Class used for simplify receiving satellite coordinates
    and calculating next passes



    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!                 IMPORTANT                !!!
    !!! ALL CALCULATIONS WORK IN UTC TIME FORMAT !!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    'config_file'
        path to config.yaml of spectator coordinates, hours predict etc.
    'tle_file'
        path to TLE file
    'satellites_tle'
        list of satellites from TLE file
    'timestamp'
        service variable for calculations time
    'longitude'
        spectator's longitude
    'latitude'
        spectator's latitude
    'altitude'
        spectator's altitude in kilometers  {MAYBE USELESS}
    'tolerance'
        accuracy   {MAYBE USELESS}
    'elevation_deg'
        elevation degree of antenna
    'hours_predict'
        Hours to predict passes
    """

    def __init__(self, config_file, tle_file):
        self.config_file = config_file
        self.tle_file = tle_file
        self.satellites_tle = skyfield.api.load.tle_file(self.tle_file)
        self.timestamp = skyfield.api.load.timescale()

        config_store = Configfile(self.config_file)
        self.longitude = config_store.get_param('longitude')
        self.latitude = config_store.get_param('latitude')
        self.altitude = config_store.get_param('altitude')
        self.tolerance = config_store.get_param('tolerance')
        self.elevation_deg = config_store.get_param('elevation_deg')
        self.hours_predict = config_store.get_param('hours_predict')

        self.spectator_location = skyfield.api.wgs84.latlon(self.latitude, self.longitude, self.altitude)

        print(f'Successfully loaded {len(self.satellites_tle)} satellites')

    def show_satellites_list(self):
        """Shows list of all satellites with data from TLE
        Example:
            IRIDIUM 106 catalog #41917 epoch 2023-03-11 03:31:26 UTC
            IRIDIUM 103 catalog #41918 epoch 2023-03-10 20:31:18 UTC
            ...
        """
        for satellite in self.satellites_tle:
            print(satellite)

    def get_satellite_by_name(self, name):
        """Returns satellite object from TLE by given name
        Example:
            > get_satellite_by_name('IRIDIUM 103')
            IRIDIUM 103 catalog #41918 epoch 2023-03-10 20:31:18 UTC
        """
        for satellite in self.satellites_tle:
            if satellite.name == name:
                return satellite

    def get_satellite_lat_lon(self,
                              satellite: skyfield.sgp4lib.EarthSatellite,
                              start_time=datetime.now(timezone.utc)):
        """Return satellite's latitude and longitude
        Input params:
            'satellite'
                satellite class, can be received in get_satellite_by_name
            'start_time'
                datetime of start calculations. datetime.now() by default
        """
        time_start = self.timestamp.utc(start_time)
        geocentric_position = satellite.at(time_start)
        lat, lon = skyfield.api.wgs84.latlon_of(geocentric_position)
        return lat, lon

    def predict_satellite_pass(self,
                               satellite: skyfield.sgp4lib.EarthSatellite,
                               start_time=datetime.now(timezone.utc),
                               prediction_hours=0):
        """Return satellite's time of passes of spectator's location
        Input params:
            'satellite'
                satellite class, can be received in get_satellite_by_name
            'start_time'
                datetime of start calculations. datetime.now() by default
            'prediction_hours'
                hours of prediction, by default uses from config.yaml
        """
        time_start = self.timestamp.utc(start_time)
        if prediction_hours == 0:
            time_end = time_start + timedelta(hours=self.hours_predict)
        else:
            time_end = time_start + timedelta(hours=prediction_hours)

        time, events = satellite.find_events(self.spectator_location,
                                             time_start,
                                             time_end,
                                             altitude_degrees=self.elevation_deg)
        return time, events

    def is_able_send(self,
                     satellite: skyfield.sgp4lib.EarthSatellite,
                     time_lag=15):
        """Returns true if satellite above spectator
        Input params:
            'satellite'
                satellite class, can be received in get_satellite_by_name
            'time_lag'
                delta in time for predict in past
        """
        time_start = datetime.now(timezone.utc) - timedelta(minutes=time_lag)

        time, events = self.predict_satellite_pass(satellite, time_start, 1)
        if len(events):
            timestamp = self.timestamp.utc(datetime.now(timezone.utc))
            # print(f'Current time is {timestamp}')
            # print(f'Time 0 is {time[0]}')
            # print(f'Time 1 is {time[1]}')
            # print(f'Time 2 is {time[2]}')

            if (timestamp - time[0]) > 0 and (time[1] - timestamp) > 0:
                return True
            else:
                return False
        else:
            return False

    def get_satellite_azimuth(self, satellite: skyfield.sgp4lib.EarthSatellite, time):
        difference = satellite - self.spectator_location
        topocentric = difference.at(time)
        altitude, azimuth, distance = topocentric.altaz()

        return azimuth.dstr()
