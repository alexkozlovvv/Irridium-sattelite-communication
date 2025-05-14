#!/usr/bin/python

import iotj_pb2
import numpy
import random
import json

poisson_m = 5
iteractions = 1000

messages = numpy.random.poisson(poisson_m, iteractions)

for i in range(iteractions):

    pb = iotj_pb2.iotj()
    pb.rxinfo.channel = 1
    pb.rxinfo.codeRate = "4/5"
    pb.rxinfo.crcStatus = 1
    pb.rxinfo.dataRate.bandwidth = 125
    pb.rxinfo.dataRate.modulation = iotj_pb2.rate.LORA
    pb.rxinfo.dataRate.spreadFactor = 7
    pb.rxinfo.frequency = 868300000
    pb.rxinfo.loRaSNR = 7
    pb.rxinfo.mac = "1dee08d0b691d149"
    pb.rxinfo.rfChain = 1
    pb.rxinfo.rssi = -57
    pb.rxinfo.size = 23
    pb.rxinfo.time.FromJsonString("0001-01-01T00:00:00Z")
    pb.rxinfo.timestamp.FromSeconds(2074240683)

    datarate = dict(bandwidth=125, modulation="LORA", spreadFactor=7)
    info = dict(channel=1, coderate="4/5", crcStatus=1, dataRate=datarate, frequency=868300000, loRaSNR=7,
                mac="1dee08d0b691d149", rfChain=1, rssi=-57, size=23, time="0001-01-01T00:00:00Z",
                timestamp=2074240683)
    js = dict(rxinfo=info)
    js["phyPayload"] = dict()

    for j in range(1, messages[i] + 1):
        value = random.uniform(-1999.9, 1999.9)
        pb.phyPayload.data.append(value)
        js["phyPayload"]["data" + str(j)] = value

    js_s = json.dumps(js)
    protobuf_s = pb.SerializeToString()

    print(str(messages[i]) + " " + str(len(js_s)) + " " + str(len(protobuf_s)))
