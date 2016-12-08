import sqlite3
import numpy as np
import random
import time
import operator
import math


class Graph:
    def __init__(self, bin_path, db_path, dbg=False):
        if dbg:
            # TODO: initialize logging
            print "Loading file"

        self.header_size = 4
        self.array = np.fromfile(bin_path, dtype='<i4')

        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()

        self.nodes = self.get_nodes()

    def at(self, pos, int_offset):
        return self.array[pos / 4 + int_offset]

    def link_count(self, pos):
        return self.at(pos, 1)

    def bi_link_count(self, pos):
        return self.at(pos, 2)

    def meta(self, pos):
        return self.at(pos, 3)

    def page_links(self, pos):
        page_int = pos / 4
        link_count = self.array[page_int + 1]
        start = page_int + self.header_size
        end = start + link_count
        return self.array[start:end]

    def page_bi_links(self, pos):
        page_int = pos / 4
        bi_link_count = self.array[page_int + 2]
        start = page_int + self.header_size
        end = start + bi_link_count
        return self.array[start:end]

    def page_un_links(self, pos):
        page_int = pos / 4
        link_count = self.array[page_int + 1]
        bi_link_count = self.array[page_int + 2]
        start = page_int + self.header_size + bi_link_count
        end = page_int + self.header_size + link_count
        return self.array[start:end]

    def name(self, pos):
        self.cur.execute("SELECT title FROM pages WHERE offset =:offset LIMIT 1", {"offset": int(pos)})
        retval = self.cur.fetchone()
        if retval is not None:
            return retval[0]
        return retval

    def find(self, string):
        self.cur.execute("SELECT offset FROM pages WHERE title =:title LIMIT 1", {"title": string})
        retval = self.cur.fetchone()
        if retval is not None:
            return retval[0]
        return retval

    def get_namespace(self, pos):
        m = self.meta(pos)
        return (m >> 8) & 7

    def get_nodes(self):
        return [node[0] for node in self.cur.execute("SELECT offset FROM pages")]


    def get_path(self, length, order=1, affine=False):
        path = []
        nodes = 0
        # 0 through order, where 0 is immediate history
        hist = []
        alphas = []
        if order > 1:
            for i in range(order):
                hist.append([])
                if affine:
                    alphas.append(float(i + 1) / sum(range(1, order + 1)))

        while nodes != length:
            seed = random.sample(self.nodes, 1)[0]
            path = [seed]
            cur_node = seed
            nodes = 1
            while nodes != length:
                links = self.page_links(cur_node)
                if order > 1:
                    # update state histories
                    hist.append(links)
                    hist.pop(0)
                    samples = []
                    if affine:
                        for i in range(order):
                            quant = reduce(operator.mul, [len(state) for state in hist[:i] + hist[i + 1:]], 1)
                            samples += [item for sublist in [[x] * int(math.floor(alphas[i] * quant))
                                                             for x in hist[i]] for item in sublist]
                    else:
                        samples = [item for sublist in hist for item in sublist]
                else:
                    samples = links

                try:
                    next_node = random.sample(samples, 1)[0]
                except ValueError:
                    break
                path.append(next_node)
                cur_node = next_node
                nodes += 1

        return path

    def total_links(self):
        links = 0
        cur = self.header_size
        while cur < len(self.array):
            links += self.array[cur + 1]
            cur += self.header_size + self.array[cur + 1]

        return links


class ExecTimer:
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
