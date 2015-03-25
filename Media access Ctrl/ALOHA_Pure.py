__author__ = 'Krish'
import random
import numpy as np
from matplotlib import pyplot as plt

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

def aloha_pure(rate):
    """

    :param rate: analogous to 'Lambda'
    :return: Throughput
    """
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
    print "G: ", G
    print "S: ", S

    return S


pkt_len = 0.01      # (Tau)     in seconds
sim_time = 10000    #           in seconds

rate = 0           # (Lambda)  pkts per sec
Throughput = []
Load = []

for G in np.arange(0, 4, 0.1):
    Load.append(G)
    rate = G / pkt_len
    # print "RATE = " , rate
    Throughput.append(aloha_pure(rate))

plt.plot(Load, Throughput)
plt.xlabel("Channel Traffic - G")
plt.ylabel("Channel Throughput - S")
plt.show()