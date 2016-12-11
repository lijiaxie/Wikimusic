#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from parse import *
from test import *

def order():
    ks = range(1, MAX_K + 1)

    data = cPickle.load(open('../data/results/run_3.pickle'))

    results = data[0]
    times = data[1]

    colors = ['r','b','g','c','m','y','k','w']
    markers = ['+', '.', 'o', '*', 'p', 's', 'x', 'D', 'h', '^']

    f, axarr = plt.subplots(1, 3)

    norm_titles = ['Without normalization', 'With normalization']

    for normalize in [False,True]:
        for order in range(1, MAX_ORDER + 1):
            aps = [x[0] for x in results[(order,normalize,0,1)]]
            axarr[normalize].plot(ks, aps, label='Order = %d' % order, color=colors[order], marker=markers[0])

        axarr[normalize].set_title(norm_titles[normalize])
        axarr[normalize].set_ylabel('Mean average precision @ k')
        axarr[normalize].set_xlabel('k')
        axarr[normalize].legend(loc=4)

    time_ys = []
    for order in range(1, MAX_ORDER + 1):
        time_ys.append(times[(order, False, 0, 1)][0])
    axarr[2].plot(range(1, MAX_ORDER + 1), time_ys, color=colors[5], marker=markers[0])
    axarr[2].set_title('Panther runtime')
    axarr[2].set_ylabel('Time (s)')
    axarr[2].set_xlabel('Order')
    axarr[2].xaxis.set_ticks(np.arange(1, MAX_ORDER + 1, 1.0))

    # plt.xlabel('k')
    # plt.ylabel('Average precision')
    # f.text(0.06, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')
    # f.text(0.5, 0.04, 'k', ha='center')
    # f.text(0.04, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')


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

    data = cPickle.load(open('../data/results/epsilon_test.pickle'))

    old_data = cPickle.load(open('../data/results/run_3.pickle'))

    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    markers = ['+', '.', 'x', '^', 's', 's', 'x', 'D', 'h', '^']

    f, axarr = plt.subplots(1,2)

    # plot MAP@k
    lines = []
    for i, affine in enumerate([0.06, 0.03, 0.01, 0.006, 0.003]):
        for order_i in [1, 2, 3, 4, 5]:
            if affine == 0.001:
                aps = [x[0] for x in old_data[0][(order_i, False, 0, 1)]]
            else:
                # for affine in [0.06, 0.03, 0.01, 0.006, 0.003, 0.001]:
                aps = [x[0] for x in data[0][(order_i, False, affine, 1)]]
            line, = axarr[0].plot(ks, aps, label=u'order = %d' % order_i, color=colors[i], marker=markers[order_i])
            lines.append(line)

    axarr[0].set_title('Mean average precision')
    axarr[0].set_ylabel('Mean average precision @ k')
    axarr[0].set_xlabel('k')
    axarr[0].legend(loc=2, handles=[lines[x] for x in [0,1,2,3,4]])

    # blue_line = mlines.Line2D([], [], color='blue', marker='*',
    #                           markersize=15, label='Blue stars')
    # plt.legend(handles=[blue_line])


    for i, affine in enumerate([0.06, 0.03, 0.01, 0.006, 0.003]):
        time_ys = []
        for order in [1,2,3,4,5]:
            if affine == 0.001:
                time_ys.append(old_data[1][(order, False, 0 , 1)][0])
            else:
                time_ys.append(data[1][(order, False, affine, 1)][0])
        axarr[1].plot([1,2,3,4,5], time_ys, label=u'ε = %.03f' % affine, color=colors[i], marker=markers[0])

    axarr[1].set_title('Panther runtime')
    axarr[1].set_ylabel('Time (s)')
    axarr[1].set_xlabel('Order')
    axarr[1].xaxis.set_ticks(np.arange(1, MAX_ORDER + 1, 1.0))
    axarr[1].legend(loc=2)

    plt.show()


def affine():
    ks = range(1, MAX_K + 1)

    data = cPickle.load(open('../data/results/affine.pickle'))

    results = data[0]
    times = data[1]

    results_unif, times_unif = cPickle.load(open('../data/results/run_3.pickle'))

    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    markers = ['+', '.', 'o', '*', 'p', 's', 'x', 'D', 'h', '^']

    f, axarr = plt.subplots(1, 2)

    norm_titles = ['Without normalization', 'With normalization']

    # for normalize in [False]:
    #     for order in range(1, 4):
    #         aps = [x[0] for x in results[(order, normalize, 1, 1)]]
    #         axarr[0].plot(ks, aps, label='Order = %d' % order, color=colors[order], marker=markers[0])
    #
    #     axarr[0].set_title('Linear convex transition combination')
    #     axarr[0].set_ylabel('Mean average precision @ k')
    #     axarr[0].set_xlabel('k')
    #     axarr[0].legend(loc=4)

    for order in range(1, 4):
        aps = [x[0] for x in results[(order, False, 1, 1)]]
        axarr[0].plot(ks, aps, label='Order = %d, %s' % (order, 'Linear'), color=colors[order], marker='s')
        aps = [x[0] for x in results_unif[(order, False, 0, 1)]]
        axarr[0].plot(ks, aps, label='Order = %d, %s' % (order, 'Uniform'), color=colors[order], marker='+')

    axarr[0].set_title('Linear vs uniform combination')
    axarr[0].set_ylabel('Mean average precision @ k')
    axarr[0].set_xlabel('k')
    axarr[0].legend(loc=4)

    time_ys = []
    times_old = []
    for order in range(1, 4):
        time_ys.append(times[(order, False, 1, 1)][0])
        times_old.append(times_unif[(order, False, 0, 1)][0])
    axarr[1].plot(range(1, 4), time_ys, label= 'Linear', color=colors[5], marker='s')
    axarr[1].plot(range(1, 4), times_old, label = 'Uniform',color=colors[5], marker='+')
    axarr[1].set_title('Panther runtime')
    axarr[1].set_ylabel('Time (s)')
    axarr[1].set_xlabel('Order')
    axarr[1].xaxis.set_ticks(np.arange(1, 4, 1.0))
    axarr[1].legend(loc=2)



    # plt.xlabel('k')
    # plt.ylabel('Average precision')
    # f.text(0.06, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')
    # f.text(0.5, 0.04, 'k', ha='center')
    # f.text(0.04, 0.5, 'Average precision', ha='center', va='center', rotation='vertical')


    plt.show()


def T():
    ks = range(1, MAX_K + 1)

    data = cPickle.load(open('../data/results/run_5.pickle'))

    # old_data = cPickle.load(open('../data/results/run_3.pickle'))

    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    markers = ['+', '.', 'x', '^', 's', 's', 'x', 'D', 'h', '^']

    f, axarr = plt.subplots(1, 2)

    # plot MAP@k
    lines = []
    for i, order in enumerate([5, 10, 20]):
        aps = [x[0] for x in data[0][(order, False, 0, 1)]]
        line, = axarr[0].plot(ks, aps, label='T = %d' % order, color=colors[i], marker=markers[0])
        lines.append(line)

    axarr[0].set_title('Mean average precision vs path length, order 3')
    axarr[0].set_ylabel('Mean average precision @ k')
    axarr[0].set_xlabel('k')
    axarr[0].legend(loc=4)

    # blue_line = mlines.Line2D([], [], color='blue', marker='*',
    #                           markersize=15, label='Blue stars')
    # plt.legend(handles=[blue_line])

    # for normalize in [False]:
    path_times = path_test()
    for i, ts in enumerate([5, 10, 20, 50, 100]):
        axarr[1].plot(range(1, MAX_ORDER + 1), path_times[ts], label='T = %d' % ts, color=colors[i], marker=markers[0])
    axarr[1].set_title('Random path generation time vs path length')
    axarr[1].xaxis.set_ticks(np.arange(1, MAX_ORDER + 1, 1.0))
    axarr[1].legend(loc=2)

    plt.show()

if __name__ == "__main__":
    # epsilon()
    # affine()
    # order()
    T()