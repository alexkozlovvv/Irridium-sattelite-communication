#!/usr/bin/python

import time
import logging
from IridiumModem import IridiumModem
import message_generate
from satellites_skyfield import Satellites

# ----- GLOBAL VARS ------
global modem

CONFIG_FILE = '../configs/config.yaml'
TLE_FILE = '../configs/iridium.tle'


# Init modem
def init_modem():
    global modem
    modem = IridiumModem(CONFIG_FILE)


# ----- Loggging -----
def init_logging():
    logging.basicConfig(filename='msg_parser.log',
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)


# --------------------
def send_data(data):
    try:
        start_time = time.time()
        logging.info("SBD Message prepared for transfer. Original message size - " + str(len(data)) +
                     ". Time - " + str(start_time))
        if modem.buffer_text_data(data):
            if modem.send_sbd_message() == 1:
                stop_time = time.time()
                logging.info("SBD Message sent. Original message size - " + str(len(data)) +
                             ". Time - " + str(stop_time) +
                             ". Time delta - " + str(stop_time - start_time))
            else:
                stop_time = time.time()
                logging.info("Unable to send message. Original message size - " + str(len(data)) +
                             ". Time - " + str(stop_time) +
                             ". Time delta - " + str(stop_time - start_time))
        else:
            logging.warning("Unable to buffer data to SBD Modem. Data - " + data + "\n")
    except KeyError:
        logging.warning("No phyPayload exist")
    except Exception as e:
        logging.error("Something went wrong", exc_info=True)
        print("ERROR: ", e)


# ------------ MAIN -----------
def main():
    print("Welcome to SBD text sender!")
    satellites_class = Satellites(CONFIG_FILE, TLE_FILE)
    init_logging()
    init_modem()

    print("Ready to send data")
    print(f'*** USED ELEVATION DEGREE IS {satellites_class.elevation_deg}° ***')
    logging.info(f'*** USED ELEVATION DEGREE IS {satellites_class.elevation_deg}° ***')
    while True:
        for sat in satellites_class.satellites_tle:
            if satellites_class.is_able_send(sat):
                print(f'Sending to {sat.name}')
                logging.info(f'Sending to {sat.name}')
                send_attempt = 1
                message = message_generate.generate()
                logging.info(f"Send attempt: {send_attempt}, message: {message}")
                send_data(message)
                send_attempt += 1
        time.sleep(1)


if __name__ == '__main__':
    main()
