import matplotlib.pyplot as plt
from parse import *


def order():
    ks = range(1, MAX_K + 1)

    data = cPickle.load(open('../data/results/run_2.pickle'))

    results = data

    colors = ['r','b','g','c','m','y','k','w']
    markers = ['+', '.', 'o', '*', 'p', 's', 'x', 'D', 'h', '^']

    for order in range(1, MAX_ORDER + 1):
        aps = [np.array([x[0] for x in results[(order,True,trial,1)]]) for trial in range(1, N_TRIALS + 1)]
        trial_avg = sum(aps) / N_TRIALS
        plt.plot(ks, trial_avg, label='Order = %d' % order, color=colors[order], marker=markers[0])

    plt.xlabel('k')
    plt.ylabel('Average precision')
    plt.legend(loc=4)
    plt.show()


def time():
    data = cPickle.load(open('../data/results/run_1.pickle'))
    times = data[1]

    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'w']
    markers = ['+', '.', 'o', '*', 'p', 's', 'x', 'D', 'h', '^']

    time_ys = []

    for order in range(1, MAX_ORDER + 1):
        time = [times[(order, False, trial)][0] for trial in range(1, N_TRIALS + 1)]
        trial_avg = sum(time) / N_TRIALS
        time_ys.append(trial_avg)

    plt.plot(range(1, MAX_ORDER+1), time_ys, label='Time', color=colors[1], marker=markers[0])


if __name__ == "__main__":
    order()