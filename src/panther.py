from models import *
from params import *
from collections import Counter
from progressbar import *


def panther(query_nodes):
    g = Graph(bin_path=BINARY, db_path=DB)
    # node_paths = {}
    scores = {}

    query_node_offsets = set(g.find(node) for node in query_nodes)

    widgets = ['Sampling: ', Percentage(), Bar(), ETA()]
    bar = ProgressBar(widgets=widgets, maxval=R).start()
    for i in range(int(ceil(R))):
        with Timer() as t:
            path = g.get_path(T + 1, 1)
        print t.interval
        relevant_query_nodes = query_node_offsets & set(path)
        for node in relevant_query_nodes:
            if node not in scores:
                scores[node] = Counter()
            for node2 in path:
                if node2 != node:
                    scores[node][node2] += score_update
        bar.update(i)
    bar.finish()

    # for node in query_node_offsets:
    #     scores[node] = Counter()
    #     if node in node_paths:
    #         for path in node_paths[node]:
    #             for node2 in path:
    #                 scores[node][node2] += 1. / R

    return scores

