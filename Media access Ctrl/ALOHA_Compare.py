__author__ = 'Krish'

import random
import numpy as np
from matplotlib import pyplot as plt
import csv
import time
import datetime


global pkt_len
global sim_time

###Utility Functions

def drange(start, stop, step):
    """
    Similar to inbuilt "range()" function, but for Float. "range()" supports only 'int'
    :param start:
    :param stop:
    :param step:
    :return:
    """
    r = start
    while r < stop:
        yield r
    r += step


def round_to_slot(evt, slot_size):
    """
    Moves the event to the next possible slot. This function helps converting the pure aloha to slotted aloha.
    :param evt:
    :param slot_size:
    :return:
    """
    return evt - (evt % slot_size) + slot_size


def aloha_pure(rate):
    evt_lst_pkt_arr = []
    for i in range(int(rate * sim_time)):
        evt_lst_pkt_arr.append(random.uniform(0, sim_time))

    # print evt_lst_pkt_arr

    evt_lst_pkt_arr = np.array(evt_lst_pkt_arr)
    sorted_evt_lst_pkt_arr = np.sort(evt_lst_pkt_arr)

    # print sorted_evt_lst_pkt_arr

    collision_course = False
    num_pkts = len(sorted_evt_lst_pkt_arr)
    dropped_pkts = 0

    for i in range( num_pkts - 1):
        if sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i] < pkt_len :
            if collision_course:
                dropped_pkts += 1
            else:
                dropped_pkts += 2
            collision_course = True
        else:
            collision_course = False

    S = ((num_pkts - dropped_pkts)*1./sim_time) * pkt_len
    G = rate * pkt_len
    # print "G: ", G
    # print "S: ", S

    return S


def aloha_slotted(rate, slot_size):
    evt_lst_pkt_arr = []
    for i in range(int(rate * sim_time)):
        evt_lst_pkt_arr.append(random.uniform(0, sim_time))
    # print evt_lst_pkt_arr

    evt_lst_pkt_arr = np.array(evt_lst_pkt_arr)
    sorted_evt_lst_pkt_arr = np.sort(evt_lst_pkt_arr)
    num_pkts = len(sorted_evt_lst_pkt_arr)

    # print sorted_evt_lst_pkt_arr

    for i in range(num_pkts):
        sorted_evt_lst_pkt_arr[i] = round_to_slot(sorted_evt_lst_pkt_arr[i], slot_size)

    collision_course = False

    dropped_pkts = 0

    for i in range( num_pkts - 1):
        if round(sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i], 2) < pkt_len :
            #print sorted_evt_lst_pkt_arr[i+1], " , ", sorted_evt_lst_pkt_arr[i], " , ", sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i]
            if collision_course:
                dropped_pkts += 1
            else:
                dropped_pkts += 2
            collision_course = True
        else:
            collision_course = False

    S = ((num_pkts - dropped_pkts)*1./sim_time) * pkt_len
    G = rate * pkt_len
    # print "G: ", G
    # print "S: ", S

    return S

def CSMA_1P(rate):
    """

    :param rate: analogous to 'Lambda'
    :return: Throughput
    """
    evt_lst_pkt_arr = []
    evt_lst_pkt_sent = []

    if rate == 0:
        return 0

    for i in range(int(rate * sim_time)):
        evt_lst_pkt_arr.append(random.uniform(0, sim_time))

    # print evt_lst_pkt_arr

    evt_lst_pkt_arr = np.array(evt_lst_pkt_arr)
    sorted_evt_lst_pkt_arr = np.sort(evt_lst_pkt_arr)

    # print sorted_evt_lst_pkt_arr

    collision_course = False
    num_pkts = len(sorted_evt_lst_pkt_arr)
    dropped_pkts = 0

    evt_lst_pkt_sent.append(sorted_evt_lst_pkt_arr[0])           # send first packet unconditionally
    for i in range( num_pkts - 1):
        if sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[i] < 0:
            evt_lst_pkt_sent.append(evt_lst_pkt_sent[i])
        elif not sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[i] < pkt_len :
            evt_lst_pkt_sent.append(sorted_evt_lst_pkt_arr[i+1])
        elif sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[i] < pkt_len :
            evt_lst_pkt_sent.append(evt_lst_pkt_sent[i]+pkt_len)

    # print (evt_lst_pkt_arr)
    # print "###########################################################################################################"
    # print (sorted_evt_lst_pkt_arr)
    # print (evt_lst_pkt_sent)

    sorted_evt_lst_pkt_arr = evt_lst_pkt_sent

    for i in range( num_pkts - 1):
        if sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i] < pkt_len-0.001 :
            if collision_course:
                dropped_pkts += 1
            else:
                dropped_pkts += 2
            collision_course = True
            # print "#####"
            # print sorted_evt_lst_pkt_arr[i]
            # print sorted_evt_lst_pkt_arr[i+1]
            # print sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i]
            # print "#####"


        else:
            collision_course = False

    S = ((num_pkts - dropped_pkts)*1./sim_time) * pkt_len
    G = rate * pkt_len
    print "G: ", G
    print "S: ", S
    print "dropped_pkts = ", dropped_pkts

    return S

def CSMA_pP(rate, p):
    """

    :param rate: analogous to 'Lambda'
    :return: Throughput
    """

    if rate == 0:
        return 0
    evt_lst_pkt_arr = []
    evt_lst_pkt_sent = []

    for i in range(int(rate * sim_time)):
        evt_lst_pkt_arr.append(random.uniform(0, sim_time))

    # print evt_lst_pkt_arr

    evt_lst_pkt_arr = np.array(evt_lst_pkt_arr)
    sorted_evt_lst_pkt_arr = np.sort(evt_lst_pkt_arr)

    # print sorted_evt_lst_pkt_arr

    collision_course = False
    num_pkts = len(sorted_evt_lst_pkt_arr)
    dropped_pkts = 0

    evt_lst_pkt_sent.append(sorted_evt_lst_pkt_arr[0])           # send first packet unconditionally
    for i in range( num_pkts - 1):
        if not sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[-1] < pkt_len :
            evt_lst_pkt_sent.append(sorted_evt_lst_pkt_arr[i+1])
        elif sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[-1] < 0 :
            if random.random()<p:
                evt_lst_pkt_sent.append(evt_lst_pkt_sent[-1])
            else:
                np.append(sorted_evt_lst_pkt_arr, evt_lst_pkt_arr[i+1]+pkt_len)
                sorted_evt_lst_pkt_arr = np.sort(sorted_evt_lst_pkt_arr)
        elif sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[-1] < pkt_len :
            if random.random()<p:
                evt_lst_pkt_sent.append(evt_lst_pkt_sent[-1]+pkt_len)
            else:
                np.append(sorted_evt_lst_pkt_arr, evt_lst_pkt_arr[i+1]+pkt_len)
                sorted_evt_lst_pkt_arr = np.sort(sorted_evt_lst_pkt_arr)


    # print (evt_lst_pkt_arr)
    # print "###########################################################################################################"
    # print (sorted_evt_lst_pkt_arr)
    # print (evt_lst_pkt_sent)

    sorted_evt_lst_pkt_arr = evt_lst_pkt_sent

    num_pkts = len(sorted_evt_lst_pkt_arr)


    for i in range( num_pkts - 1):
        if sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i] < pkt_len-0.001 :
            if collision_course:
                dropped_pkts += 1
            else:
                dropped_pkts += 2
            collision_course = True
            # print "#####"
            # print sorted_evt_lst_pkt_arr[i]
            # print sorted_evt_lst_pkt_arr[i+1]
            # print sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i]
            # print "#####"


        else:
            collision_course = False

    S = ((num_pkts - dropped_pkts)*1./sim_time) * pkt_len
    G = rate * pkt_len
    print "G: ", G
    print "S: ", S
    print "dropped_pkts = ", dropped_pkts

    return S


def CSMA_0P(rate):
    """

    :param rate: analogous to 'Lambda'
    :return: Throughput
    """
    evt_lst_pkt_arr = []
    evt_lst_pkt_sent = []

    if rate == 0:
        return 0

    for i in range(int(rate * sim_time)):
        evt_lst_pkt_arr.append(random.uniform(0, sim_time))

    # print evt_lst_pkt_arr

    evt_lst_pkt_arr = np.array(evt_lst_pkt_arr)
    sorted_evt_lst_pkt_arr = np.sort(evt_lst_pkt_arr)

    # print sorted_evt_lst_pkt_arr

    collision_course = False
    num_pkts = len(sorted_evt_lst_pkt_arr)
    dropped_pkts = 0

    evt_lst_pkt_sent.append(sorted_evt_lst_pkt_arr[0])           # send first packet unconditionally
    for i in range( num_pkts - 1):
        # print i
        # print sorted_evt_lst_pkt_arr
        # print evt_lst_pkt_sent
        if not sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[-1] < pkt_len :
            evt_lst_pkt_sent.append(sorted_evt_lst_pkt_arr[i+1])
        elif sorted_evt_lst_pkt_arr[i+1] - evt_lst_pkt_sent[-1] < pkt_len :
            np.append(sorted_evt_lst_pkt_arr, evt_lst_pkt_arr[i+1]+pkt_len)
            sorted_evt_lst_pkt_arr = np.sort(sorted_evt_lst_pkt_arr)

    # print (evt_lst_pkt_arr)
    # print "###########################################################################################################"
    # print (sorted_evt_lst_pkt_arr)
    #print (evt_lst_pkt_sent)

    evt_lst_pkt_sent = np.array(evt_lst_pkt_sent)
    sorted_evt_lst_pkt_arr = np.sort(evt_lst_pkt_sent)
    num_pkts = len(sorted_evt_lst_pkt_arr)
    # print (sorted_evt_lst_pkt_arr)

    for i in range( num_pkts - 1):
        if sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i] < pkt_len-0.001:
            if collision_course:
                dropped_pkts += 1
            else:
                dropped_pkts += 2
            collision_course = True
            # print "#####"
            # print sorted_evt_lst_pkt_arr[i]
            # print sorted_evt_lst_pkt_arr[i+1]
            # print sorted_evt_lst_pkt_arr[i+1] - sorted_evt_lst_pkt_arr[i]
            # print "#####"


        else:
            collision_course = False

    S = ((num_pkts - dropped_pkts)*1./sim_time) * pkt_len
    G = rate * pkt_len
    print "G: ", G
    print "S: ", S
    print(num_pkts)
    print "dropped_pkts = ", dropped_pkts

    return S


pkt_len = 0.01      # (Tau)     in seconds
sim_time = 1000    #           in seconds

rate = 50           # (Lambda)  pkts per sec
Throughput_Pure = []
Throughput_Slotted = []
Throughput_CSMA_1P = []
Throughput_CSMA_080P = []
Throughput_CSMA_050P = []
Throughput_CSMA_0P = []
Load = []

table = [["Rate", "Pure ALOHA", "Slotted ALOHA", "CSMA_1P", "CSMA_0.8P", "CSMA_0.5P", "CSMA_0P"]]

for G in np.arange(0, 6, 0.1):
    Load.append(G)
    rate = G / pkt_len
    print "RATE = " , rate
    Throughput_Pure.append(aloha_pure(rate))
    Throughput_Slotted.append(aloha_slotted(rate, pkt_len))
    Throughput_CSMA_1P.append(CSMA_1P(rate))
    Throughput_CSMA_080P.append(CSMA_pP(rate, 0.8))
    Throughput_CSMA_050P.append(CSMA_pP(rate, 0.8))
    Throughput_CSMA_0P.append(CSMA_0P(rate))

table = [Load, Throughput_Pure, Throughput_Slotted, Throughput_CSMA_1P, Throughput_CSMA_080P, Throughput_CSMA_050P,
         Throughput_CSMA_0P]
table = zip(*table)
table.insert(0, ("Rate", "Pure ALOHA", "Slotted ALOHA", "CSMA_1P", "CSMA_0.8P", "CSMA_0.5P", "CSMA_0P"))

print table

ts = time.time()
with open('/Users/Krish/Google Drive/Sim_Results/aloha_csma_compare/'+
                  datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')+'Aloha_csma_compare.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    [writer.writerow(r) for r in table]

plt.plot(Load, Throughput_Pure, label="Pure ALOHA")
plt.plot(Load, Throughput_Slotted, label="Slotted ALOHA")
plt.plot(Load, Throughput_CSMA_1P, label="CSMA_1P")
plt.plot(Load, Throughput_CSMA_080P, label="CSMA_0.8P")
plt.plot(Load, Throughput_CSMA_050P, label="CSMA_0.5P")
plt.plot(Load, Throughput_CSMA_0P, label="CSMA_0P")

plt.xlabel("Channel Traffic - G")
plt.ylabel("Channel Throughput - S")
plt.legend()
plt.show()