#!/usr/bin/python
import queue
import paho.mqtt.client as mqtt
import json
import time
import logging
import iotj_pb2
from IridiumModem import IridiumModem

# ----- GLOBAL VARS ------
global modem
global client
global queue_data
global counter


CONFIG_FILE = '../configs/config.yaml'
MQTT_USERNAME = ''
MQTT_PASSWD = ''
MQTT_URL = 'test.mosquitto.org'
MQTT_PORT = 1883


# ------ MQTT Message parsing
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global queue_data
    global counter
    #  ----  Debug received event
    logging.debug("Message received: " + msg.topic + " " + msg.payload.decode('ascii'))

    # ----- JSON Convert
    try:
        msg_data = msg.payload.decode('ascii')
        datajson = json.loads(msg_data)
        queue_data.put(datajson)

    except Exception as e:
        logging.warning("Unexpected error:", exc_info=True)
        print("ERROR: ", e)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("iot_miem/#")


def myOnPublishCallback():
    logging.info("Confirmed event received by IoTF\n")


# Init modem
def init_modem():
    global modem
    modem = IridiumModem(CONFIG_FILE)


# ------ MQTT Connect
def init_mqtt():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWD)
    client.connect(MQTT_URL, MQTT_PORT)


# ----- Init queue -----
def init_queue():
    global queue_data
    global counter
    queue_data = queue.Queue()
    counter = 1


# ----- Loggging -----
def init_logging():
    logging.basicConfig(filename='msg_parser.log',
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=logging.DEBUG)


#  ------ encode data to protobuf  -----
def encode_data(source):
    pb = iotj_pb2.iotj()
    pb.rxinfo.channel = source["rxInfo"]["channel"]
    pb.rxinfo.codeRate = source["rxInfo"]["codeRate"]
    pb.rxinfo.crcStatus = source["rxInfo"]["crcStatus"]
    pb.rxinfo.dataRate.bandwidth = source["rxInfo"]["dataRate"]["bandwidth"]
    pb.rxinfo.dataRate.modulation = iotj_pb2.rate.LORA
    pb.rxinfo.dataRate.spreadFactor = source["rxInfo"]["dataRate"]["spreadFactor"]
    pb.rxinfo.frequency = source["rxInfo"]["frequency"]
    pb.rxinfo.loRaSNR = source["rxInfo"]["loRaSNR"]
    pb.rxinfo.mac = source["rxInfo"]["mac"]
    pb.rxinfo.rfChain = source["rxInfo"]["rfChain"]
    pb.rxinfo.rssi = source["rxInfo"]["rssi"]
    pb.rxinfo.size = source["rxInfo"]["size"]
    pb.rxinfo.time.FromJsonString(source["rxInfo"]["time"])
    pb.rxinfo.timestamp.FromSeconds(source["rxInfo"]["timestamp"])

    pb.phyPayload = source["phyPayload"]

    protobuf_s = pb.SerializeToString(
    )
    return protobuf_s


# --------------------

def send_data():
    global queue_data
    global counter
    data = queue_data.get()

    try:
        encoded_data = encode_data(data)
        start_time = time.time()
        logging.info("SBD Message prepared for transfer. Message num - " + str(counter) +
                     ". Original message size - " + str(len(json.dumps(data))) + ". Encoded message size - " +
                     str(len(encoded_data)) + ". Time - " + str(start_time) + ".")
        if modem.BufferBinaryData(encoded_data):
            if modem.SendSBDMessage() == 1:
                stop_time = time.time()
                logging.info("SBD Message sent. Message num - " + str(counter) +
                             ". Original message size - " + str(len(json.dumps(data))) + ". Encoded message size - " +
                             str(len(encoded_data)) + ". Time - " + str(stop_time) + ". Time delta - " +
                             str(stop_time - start_time) + ".")
                counter = counter + 1
            else:
                stop_time = time.time()
                logging.info("Unable to send message. Message num - " + str(counter) +
                             ". Original message size - " + str(len(json.dumps(data))) + ". Encoded message size - " +
                             str(len(encoded_data)) + ". Time - " + str(stop_time) + ". Time delta - " +
                             str(stop_time - start_time) + ".")
                counter = counter + 1
        else:
            logging.warning("Unable to buffer data to SBD Modem. Data - " + data["phyPayload"].encode() + "\n")
    except KeyError:
        logging.warning("No phyPayload exist")
    except Exception as e:
        logging.error("Something went wrong", exc_info=True)
        print("ERROR: ", e)


# ------------ MAIN -----------
if __name__ == '__main__':
    print("Welcome to SBD sender!")
    init_logging()
    init_modem()
    init_mqtt()
    init_queue()

    client.loop_start()
    print("Ready to receive data")
    while True:
        send_data()
