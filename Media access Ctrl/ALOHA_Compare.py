__author__ = 'Krish'

import random
import numpy as np
from matplotlib import pyplot as plt


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




pkt_len = 0.01      # (Tau)     in seconds
sim_time = 100    #           in seconds

rate = 50           # (Lambda)  pkts per sec
Throughput_Pure = []
Throughput_Slotted = []
Throughput_CSMA_1P = []
Load = []

for G in np.arange(0, 7, 0.1):
    Load.append(G)
    rate = G / pkt_len
    print "RATE = " , rate
    Throughput_Pure.append(aloha_pure(rate))
    Throughput_Slotted.append(aloha_slotted(rate, pkt_len))
    Throughput_CSMA_1P.append(CSMA_1P(rate))

plt.plot(Load, Throughput_Pure, label="Pure")
plt.plot(Load, Throughput_Slotted, label="Slotted")
plt.plot(Load, Throughput_CSMA_1P, label="CSMA_1P")

plt.xlabel("Channel Traffic - G")
plt.ylabel("Channel Throughput - S")
plt.legend()
plt.show()