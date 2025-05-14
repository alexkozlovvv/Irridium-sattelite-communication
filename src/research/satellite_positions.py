import ephem
from datetime import datetime, timezone, timedelta
from pyorbital.orbital import Orbital
from datetime import datetime

if __name__ == '__main__':
    print("#### EPHEM ####")
    gatech = ephem.Observer()
    gatech.lon, gatech.lat = '55.803218', '37.410161'

    # start_date = datetime.now(timezone.utc) - timedelta(minutes=10)
    iridium_sat = ephem.readtle("IRIDIUM 129",
                                "1 42958U 17061D   23069.72137539  .00000769  00000+0  26754-3 0  9998",
                                "2 42958  86.4035 164.4548 0002115  90.8789 269.2649 14.34221414283599")
    gatech.date = '2023/3/11 18:37:00'
    iridium_sat.compute(gatech)
    info = gatech.next_pass(iridium_sat)
    print(info)
    print("Rise time: %s azimuth: %s" % (info[0], info[1]))
    print("Max time: %s azimuth: %s" % (info[2], info[3]))


    print("#### PYORBITAL ####")
    # Use current TLEs from the internet:
    orb = Orbital("IRIDIUM 134")
    timestamp = datetime.now(timezone.utc)
    # Get normalized position and velocity of the satellite:
    print(orb.get_position(timestamp))
    # Get longitude, latitude and altitude of the satellite:
    print(orb.get_lonlatalt(timestamp))
