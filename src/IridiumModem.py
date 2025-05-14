import struct
import serial
import re
import logging
import time
from read_config import Configfile


# ----- Iridium Modem Class -------
class IridiumModem:
    def __init__(self, config_file, timeout=1):
        config_store = Configfile(config_file)
        self.port = config_store.get_param('modem_port')
        self.speed = config_store.get_param('modem_baudrate')
        self.serial_port = serial.Serial(self.port, self.speed, timeout=timeout)
        self.send_command("ATI\r")

    def send_command(self, command, cr='\r'):
        if type(command) is bytes:
            send_str = command
        else:
            send_str = command.encode('ascii')
        self.serial_port.write(send_str)
        logging.debug("Command send to modem " + str(command))
        time_counter = 0
        success = False
        result = ""
        while not success and time_counter <= 20:
            line = str(self.serial_port.readline())
            logging.debug("Line got from modem - " + line)
            if line.find("OK") >= 0 or line.find("ERROR") >= 0 or line.find("READY") >= 0:
                success = True
            result = result + line
            if len(line) == 0:
                logging.debug("Zero length line from modem")
                time_counter = time_counter + 1
        logging.debug("Final response from modem got - " + result)
        print(result)
        return result, success

    def buffer_text_data(self, data):
        result, success = self.send_command('AT+SBDWT=' + data + '\r\n')
        if result.find("OK") > 0:
            return True
        else:
            return False

    def buffer_binary_data(self, data):
        status = False
        result, success = self.send_command('AT+SBDWB=' + str(len(data)) + '\r\n')
        if success and result.find("READY") >= 0:
            logging.debug("Modem is ready to receive binary data")
            data_crc = 0
            for i in range(len(data)):
                # print(i, data[i], len(data), bytes(data[i], encoding='ascii'))
                data_crc = data_crc + int.from_bytes(bytes(data[i], encoding='ascii'), 'big')
            data_crc = data_crc & 0xFFFF
            logging.debug("Data CRC - " + str(data_crc))

            data_send = str.encode(data, encoding='ascii')
            full_data = data_send + struct.pack("!H", data_crc)
            logging.debug("Full data value - " + str(full_data))
            result, success = self.send_command(full_data, '')
            if success and result.find("0") >= 0:
                logging.debug("Modem parsed SBD binary data")
                status = True
            else:
                logging.warning("Modem unable to parse recevied data")
        else:
            logging.warning("Modem is not ready to receive SBD binary data")
        return status

    def send_sbd_message(self, attempts=10, sleep=0):
        num_attempts = 0
        send_result = 99
        while send_result != 1 and num_attempts < attempts:
            output, status = self.send_command("AT+SBDI\r")
            num_attempts = num_attempts + 1
            if status:
                # SBDI: 2, 4, 2, 0, 0, 0
                sbd_regexp = re.compile("SBDI: (\d+)\, (\d+)\, (\d+)\, (\d+)\, (\d+)\, (\d+)")
                sbdi_result = sbd_regexp.search(output)
                if sbdi_result:
                    if sbdi_result.group(1) == "1":
                        logging.info("SBDI Data sent. Attempt - " + str(num_attempts) + ".")
                        send_result = 1
                    else:
                        logging.warning(
                            "SBDI error sending data with code " + sbdi_result.group(1) + ". Attempt - " + str(
                                num_attempts))
                        send_result = int(sbdi_result.group(1))
                else:
                    logging.warning("SBD Send error parsing SBDI result")
            time.sleep(sleep)
        logging.debug("Exiting from SendSBDMessage with code " + str(send_result))
        return send_result

