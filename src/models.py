import sqlite3
import numpy as np

class Graph:
    def __init__(self, binary, db_path, dbg = False):
        if dbg:
        #     TODO: initialize logging
            print "Loading file"

        self.header_size = 4
        self.array = np.fromfile(binary, dtype='<i4')

        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()

    def at(self, pos, offset):
        return self.array[pos / 4 + offset]

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
        return self.cur.fetchone()

    def find(self, string):
        self.cur.execute("SELECT offset FROM pages WHERE title =:title LIMIT 1", {"title": string})
        return self.cur.fetchone()