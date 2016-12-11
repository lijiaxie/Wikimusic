#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from parse import *
from test import *

def order():
    ks = range(1, MAX_K + 1)

    data = cPickle.load(open('../data/results/run_3.pickle'))

    results = data[0]

    colors = ['r','b','g','c','m','y','k','w']
    markers = ['+', '.', 'o', '*', 'p', 's', 'x', 'D', 'h', '^']

    f, axarr = plt.subplots(2, 1, sharex=True, sharey=True)

    norm_titles = ['Without normalization', 'With normalization']

    for normalize in [True, False]:
        for order in range(1, MAX_ORDER + 1):
            aps = [x[0] for x in results[(order,normalize,0,1)]]
            axarr[normalize].plot(ks, aps, label='Order = %d' % order, color=colors[order], marker=markers[0])
            axarr[normalize].set_title(norm_titles[int(normalize)])

    # plt.xlabel('k')
    # plt.ylabel('Average precision')
    # f.text(0.06, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')
    f.text(0.5, 0.04, 'k', ha='center')
    f.text(0.04, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')
    plt.legend(loc=4)

    plt.show()


def time():
    data = cPickle.load(open('../data/results/run_3.pickle'))
    times = data[1]

    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    markers = ['+', '.', 'o', '*', 'p', 's', 'x', 'D', 'h', '^']
    norm_titles = ['Without normalization', 'With normalization']

    f, axarr = plt.subplots(2, 1, sharex=True)

    # for normalize in [False]:
    time_ys = []
    fold_inc = []
    path_times = path_test()
    for order in range(1, MAX_ORDER + 1):
        time_ys.append(times[(order, False, 0, 1)][0])
        fold_inc.append(times[(order, False, 0, 1)][0] / times[(1, False, 0, 1)][0])
    axarr[0].plot(range(1, MAX_ORDER+1), time_ys, color=colors[5], marker=markers[0])
    axarr[0].set_title('Panther runtime')
    # axarr[0].set_ylabel('Time (s)')
    for i, ts in enumerate([5,10,20,50,100]):
        axarr[1].plot(range(1, MAX_ORDER+1), path_times[ts], label='T = %d' % ts, color=colors[i], marker=markers[0])
    # axarr[1].set_ylabel('Time (x)')
    axarr[1].set_title('Random path generation time')
    axarr[0].xaxis.set_ticks(np.arange(1, MAX_ORDER + 1, 1.0))
    axarr[1].xaxis.set_ticks(np.arange(1, MAX_ORDER + 1, 1.0))
    axarr[1].legend(loc=2)

    f.text(0.5, 0.04, 'Order', ha='center')
    f.text(0.04, 0.5, 'Time (s)', ha='center', va='center', rotation='vertical')


    plt.show()


def epsilon():
    ks = range(1, MAX_K + 1)

    data = cPickle.load(open('../data/results/run_4.pickle'))

    results = data[0]
    time = data[1]

    old_data = cPickle.load(open('../data/results/run_3.pickle'))
    old_results = data[0]
    old_time = data[1]

    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    markers = ['+', '.', 'o', '*', 'p', 's', 'x', 'D', 'h', '^']

    f, axarr = plt.subplots(2, 1, sharex=True)

    norm_titles = ['Time', 'With normalization']

    # plot MAP@k
    for i, order in enumerate([0.06, 0.03, 0.01, 0.006, 0.003, 0.001]):
        if order == 0.001:
            aps = [x[0] for x in old_data[0][(3, False, 0, 1)]]
        else:
            aps = [x[0] for x in data[0][(order, False, 0, 1)]]
        axarr[0].plot(ks, aps, label=u'ε = %.03f' % order, color=colors[i], marker=markers[0])

    # axarr[0].set_title('Panther runtime')
    # axarr[1].set_title('Average precision')

    axarr[0].set_ylabel('Mean average precision @ k')


    for i, order in enumerate([0.06, 0.03, 0.01, 0.006, 0.003, 0.001]):
        time_ys = []
        if order == 0.001:
            time_ys.append(old_data[1][(3, False, 0, 1)][0])
        else:
            time_ys.append(data[1][(order, False, 0, 1)][0])
        axarr[1].plot(ks, time_ys, color=colors[5], marker=markers[0])

    axarr[1].set_title('Panther runtime')

    axarr[1].set_ylabel('Time (s)')

    # plt.xlabel('k')
    # plt.ylabel('Average precision')
    # f.text(0.06, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')
    f.text(0.5, 0.04, 'k', ha='center')
    # f.text(0.04, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')
    plt.legend(loc=2)

    plt.show()


if __name__ == "__main__":
    epsilon()