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
E = 168096214
R = (c / (epsilon ** 2)) * (log(sp.binom(T, 2), 2) + 1 + log(1 / delta))
score_update = 1. / R

# Experimental constants
MAX_K = 100
K_TRIALS = [5, 10, 25, 50]
ORDERS = [1,2,3,4,5]
MAX_ORDER = 5
N_TRIALS = 3