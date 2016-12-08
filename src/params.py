from math import *
import scipy.special as sp

BINARY = '../data/wikidata/indexbi.bin'
DB = '../data/wikidata/xindex-nocase.db'

LOC_BINARY = 'data/wikidata/indexbi.bin'
LOC_DB = 'data/wikidata/xindex-nocase.db'

c = 0.5
delta = 0.1
T = 5
D = 50
epsilon = 0.001
R = (c / (epsilon ** 2)) * (log(sp.binom(T, 2), 2) + 1 + log(1 / delta))
score_update = 1. / R

k = 10