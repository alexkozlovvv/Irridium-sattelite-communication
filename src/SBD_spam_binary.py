#!/usr/bin/python
import time
import logging
from IridiumModem import IridiumModem
import message_generate

# ----- GLOBAL VARS ------
global modem

CONFIG_FILE = '../configs/config.yaml'


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
        if modem.buffer_binary_data(data):
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
if __name__ == '__main__':
    print("Welcome to SBD binary sender!")
    init_logging()
    init_modem()

    print("Ready to send data")
    while True:
        send_attempt = 1
        message = message_generate.generate()
        logging.info(f"Send attempt: {send_attempt}, message: {message}")
        send_data(message)
        send_attempt += 1
