__author__ = 'Krish'
import random
import numpy as np
from matplotlib import pyplot as plt
import random

global pkt_len
global sim_time

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

np.set_printoptions(threshold='nan', precision=4, suppress=True)

pkt_len = 0.01      # (Tau)     in seconds
sim_time = 100    #           in seconds

rate = 0           # (Lambda)  pkts per sec
Throughput = []
Load = []

for G in np.arange(0, 4, 0.1):
    Load.append(G)
    rate = G / pkt_len
    # print "RATE = " , rate
    Throughput.append(CSMA_pP(rate, 0.8))

plt.plot(Load, Throughput)
plt.xlabel("Channel Traffic - G")
plt.ylabel("Channel Throughput - S")
plt.show()

# G = 1
# rate = G / pkt_len
# aloha_pure(rate)