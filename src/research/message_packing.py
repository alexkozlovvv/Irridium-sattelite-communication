#!/usr/bin/python

import iotj_pb2
import numpy
import random
import json

poisson_m = 5
iteractions = 1000
sbd_size = 320

messages = numpy.random.poisson(poisson_m, iteractions)

messages_list = list()

print("--- Messages generation ---\n")


def print_packing_result():
    objects = 0
    objects_average = 0.0
    size = 0
    size_average = 0.0

    global containers_amount
    global containers_capacity
    global containers

    for i in range(containers_amount + 1):
        print("Container " + str(i) + " " + str(containers_capacity[i]) + " " + str(len(containers[i])))
        objects += containers_capacity[i]
        size += len(containers[i])

    objects_average = objects / len(containers)
    size_average = size / len(containers)

    print("Number of containers " + str(len(containers)))
    print("Size " + str(size) + " average " + str(size_average))
    print("Objects " + str(objects) + " average " + str(objects_average))
    print("Ticks " + str(ticks))

    return


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
                mac="1dee08d0b691d149", rfChain=1, rssi=-57, size=23, time="0001-01-01T00:00:00Z", timestamp=2074240683)
js = dict(rxinfo=info)
js["phyPayload"] = dict()

for j in range(1, messages[i] + 1):
    value = random.uniform(-1999.9, 1999.9)
    pb.phyPayload.data.append(value)
    js["phyPayload"]["data" + str(j)] = value

js_s = json.dumps(js)
protobuf_s = pb.SerializeToString()
messages_list.append(protobuf_s)

print(str(messages[i]) + " " + str(len(js_s)) + " " + str(len(protobuf_s)));

print("\nOne opened container\n")

containers = list()
containers.append("")
containers_amount = 0
containers_capacity = list()
containers_capacity.append(0)
ticks = 0

for i in range(iteractions):
    ticks += 1
    if len(containers[containers_amount]) + len(messages_list[i]) < sbd_size:
        containers[containers_amount] = containers[containers_amount] + messages_list[i]
        containers_capacity[containers_amount] += 1
    else:
        containers.append(messages_list[i])
        containers_amount += 1
        containers_capacity.append(1)

print_packing_result()

print("\nAll containers opened (data is not sorted)\n")

containers = list()
containers.append("")
containers_amount = 0
containers_capacity = list()
containers_capacity.append(0)
ticks = 0

for i in range(iteractions):
    included = False
    j = 0
    ticks += 1
    while j < containers_amount + 1 and not included:
        if len(containers[j]) + len(messages_list[i]) < sbd_size:
            containers[j] = containers[j] + messages_list[i]
            containers_capacity[j] += 1
            included = True
        j += 1
        ticks += 1
    if not included:
        containers.append(messages_list[i])
        containers_amount += 1
        containers_capacity.append(1)

print_packing_result()

print("\nSort all data")

ticks = 0

for i in range(len(messages_list)):
    for j in range(i + 1, len(messages_list)):
        ticks += 1
        if len(messages_list[i]) < len(messages_list[j]):
            x = messages_list[i]
            messages_list[i] = messages_list[j]
            messages_list[j] = x

print("\nAll containers opened (data is sorted)\n")

containers = list()
containers.append("")
containers_amount = 0
containers_capacity = list()
containers_capacity.append(0)

for i in range(iteractions):
    included = False
    j = 0
    ticks += 1
    while j < containers_amount + 1 and not included:
        if len(containers[j]) + len(messages_list[i]) < sbd_size:
            containers[j] = containers[j] + messages_list[i]
            containers_capacity[j] += 1
            included = True
        j += 1
        ticks += 1
    if not included:
        containers.append(messages_list[i])
        containers_amount += 1
        containers_capacity.append(1)

print_packing_result()
