#!/usr/bin/python

import iotj_pb2
import numpy
import random
import json
import zlib

poisson_m = 5
iteractions = 1000
sbd_size = 320
sbd_size_min = 320
sbd_size_max = 9000
sbd_size_period = 10

messages = numpy.random.poisson(poisson_m, iteractions)

messages_list = list()

print("--- Messages generation ---")


def print_packing_result():
    objects = 0
    objects_average = 0.0
    size = 0
    size_average = 0.0
    compressed_size = 0

    global containers_amount
    global containers_capacity
    global containers
    global ticks
    global sbd_size

    for i in range(containers_amount + 1):
        compressed_size += len(zlib.compress(containers[i]))
        # print("Container " + str(i) + " " + str(containers_capacity[i]) + " " + str(len(containers[i])) + " " + str(len(compressed_data)))
        objects += containers_capacity[i]
        size += len(containers[i])

    objects_average = objects / len(containers)
    size_average = size / len(containers)
    compressed_average = compressed_size / len(containers)

#    print("Number of containers " + str(len(containers)))
#    print("Size " + str(size) + " average " + str(size_average))
#    print("Objects " + str(objects) + " average " + str(objects_average))
#    print("Ticks " + str(ticks))
    print(str(sbd_size) + " " + str(len(containers)) + " {0:.2f}".format(size_average) + " {0:.2f}".format(compressed_average) + " {0:.2f}".format(objects_average) + " {0:.4f}".format(compressed_average/size_average))

    return


for i in range(iteractions):

    # Create

    pb = iotj_pb2.iotj()

    # LORA fields from generic LORA Message
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
    messages_list.append(protobuf_s)
    protobuf_sz=zlib.compress(protobuf_s)
    print(str(messages[i]) + " " + str(len(js_s)) + " " + str(len(protobuf_s)) + " " + str(len(protobuf_sz)))

print("\nOne opened container\n")
print("SBD Containers AvgUncompressed AvgCompressed AvgAmount Ratio")
for sbd_size in range(sbd_size_min, sbd_size_max, sbd_size_period):
    containers = list()
    containers.append(str.encode(""))
    containers_amount = 0
    containers_capacity = list()
    containers_capacity.append(0)
    ticks = 0
    for i in range(iteractions):
        ticks += 1
        if len(zlib.compress(containers[containers_amount] + zlib.compress(messages_list[i]))) < sbd_size:
            containers[containers_amount] = containers[containers_amount] + messages_list[i]
            containers_capacity[containers_amount] += 1
        else:
            containers.append(messages_list[i])
            containers_amount += 1
            containers_capacity.append(1)
    print_packing_result()
