from models import *
from params import *
from progressbar import *
#
# GLOBAL_GRAPH = Graph(bin_path=LOC_BINARY, db_path=LOC_DB)

GLOBAL_GRAPH = Graph(bin_path=BINARY, db_path=DB)

def panther(query_nodes, order=1, normalize=False, affine=0):
    scores = {}

    if normalize:
        counts = ct()

    query_nodes = set(query_nodes)

    new_R = (c / (affine ** 2)) * (log(sp.binom(T, 2), 2) + 1 + log(1 / delta))

    # new_R = R

    widgets = ['panther(): sampling: ', Percentage(), Bar(), ETA()]
    bar = ProgressBar(widgets=widgets, maxval=int(ceil(new_R))).start()

    for i in range(int(ceil(new_R))):
        path = GLOBAL_GRAPH.get_path(T + 1, order=order, affine=0)
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

