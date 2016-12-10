import sqlite3
import numpy as np
import random
import time
from collections import Counter as ct


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
        return list(self.array[start:end])

    def page_bi_links(self, pos):
        page_int = pos / 4
        bi_link_count = self.array[page_int + 2]
        start = page_int + self.header_size
        end = start + bi_link_count
        return list(self.array[start:end])

    def page_un_links(self, pos):
        page_int = pos / 4
        link_count = self.array[page_int + 1]
        bi_link_count = self.array[page_int + 2]
        start = page_int + self.header_size + bi_link_count
        end = page_int + self.header_size + link_count
        return list(self.array[start:end])

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

    def check_meta(self, pos):
        meta = self.meta(pos)
        return (meta >> 8) & 7 == 0

    def get_namespace(self, pos):
        m = self.meta(pos)
        return (m >> 8) & 7

    def get_nodes(self):
        return [node[0] for node in self.cur.execute("SELECT offset FROM pages")]


    def get_path(self, length, order=1, affine=0, meta=False):
        path = []
        nodes = 0
        # 0 through order, where 0 is immediate history
        hist = []
        alphas = []
        if order > 1:
            for i in range(1, order + 1):
                hist.append([])
                # linear positive
                if affine == 1:
                    alphas.append(i)
                # poly pos
                elif affine == 2:
                    alphas.append(i ** 2)
                # expo pos
                elif affine == 3:
                    alphas.append(2 ** i)
                # unif neg
                elif affine == 4:
                    if i == order:
                        alphas.append(order)
                    else:
                        alphas.append(-1)
                # lin neg
                elif affine == 5:
                    if i == order:
                        alphas.append(sum(range(1, order + 1)))
                    else:
                        alphas.append(-i)
                # poly neg
                elif affine == 6:
                    if i == order:
                        alphas.append(sum([(i ** 2) for i in range(1, order + 1)]))
                    else:
                        alphas.append(-(i ** 2))
                # expo neg
                elif affine == 7:
                    if i == order:
                        alphas.append(sum([(2 ** i) for i in range(1, order + 1)]))
                    else:
                        alphas.append(-(2 ** i))
                # unif pos
                else:
                    continue

        while nodes != length:
            seed = random.sample(self.nodes, 1)[0]
            if meta:
                while not self.check_meta(seed):
                    seed = random.sample(self.nodes, 1)[0]
            path = [seed]
            cur_node = seed
            nodes = 1
            while nodes != length:
                with ExecTimer() as t:
                    links = self.page_links(cur_node)
                # print "Getting links: %.05f" % t.interval
                with ExecTimer() as t1:
                    if meta:
                        links = [x for x in links if self.check_meta(x)]
                    if order > 1:
                        # update state histories
                        hist.append(links)
                        hist.pop(0)
                        # non-affine
                        if affine == 0:
                            samples = [item for sublist in hist for item in sublist]

                        # stupid coding
                        # else:
                        #     ps = np.cumsum([alphas[i] * len(state) for i, state in enumerate(hist)])
                        #     total_p = ps[-1:]
                        #     some_int = random.randint(0,total_p)
                        #     negs = [int(x - some_int >= 0) for x in ps]
                        #
                        #     ind1 = negs.index(1)
                        #     ind2 = some_int - ps[ind1-1]
                        #     try:
                        #         next_node = hist[ind1][ind2]
                        #     except IndexError:
                        #         break

                        # negative affine cases
                        elif affine > 3:
                            counters = [ct(x * abs(alphas[i])) for i, x in enumerate(hist)]
                            counters.reverse()
                            ctr_sum = ct()
                            for i in range(len(counters)):
                                if alphas[len(counters) - i - 1] > 0:
                                    ctr_sum += counters[i]
                                else:
                                    ctr_sum -= counters[i]
                            samples = list(ctr_sum.elements())
                        # positive cases
                        else:
                            samples = list(sum([ct(x * alphas[i]) for i, x in enumerate(hist)], ct()).elements())

                    else:
                        samples = links
                        # print "Getting samples: %.05f" % t1.interval
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
