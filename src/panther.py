from models import *
from params import *
from collections import Counter as ct
from progressbar import *


def panther(query_nodes, order=1, normalize=False):
    g = Graph(bin_path=BINARY, db_path=DB)
    scores = {}

    if normalize:
        counts = ct()

    query_nodes = set(query_nodes)

    widgets = ['panther(): sampling: ', Percentage(), Bar(), ETA()]
    bar = ProgressBar(widgets=widgets, maxval=int(ceil(R))).start()
    for i in range(int(ceil(R))):
        path = g.get_path(T + 1, order)
        relevant_query_nodes = query_nodes & set(path)
        for node in relevant_query_nodes:
            if node not in scores:
                scores[node] = ct()
            for node2 in path:
                if normalize:
                    counts[node2] += 1
                if node2 != node:
                    scores[node][node2] += 1

        if not relevant_query_nodes and normalize:
            for node in path:
                counts[node] += 1

        bar.update(i)
    bar.finish()

    widgets = ['panther(): normalizing: ', Percentage(), Bar(), ETA()]
    bar = ProgressBar(widgets=widgets, maxval=len(scores)).start()
    index = 0
    if normalize:
        for node1, nodes in scores.iteritems():
            for node2, val in nodes.iteritems():
                scores[node1][node2] = (scores[node1][node2] ** 2) / float(counts[node1] * counts[node2])
        bar.update(index)
        index += 1
    bar.finish()

    return scores

