import unicodecsv
from panther import *
import _pickle as cPickle
import json
import urllib
import urllib.parse as urlparse
# from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#import lxml.html

XML_ARTISTS = '../data/discogs_20160201_artists.xml'
XML_RELEASES = '../data/discogs_20160101_releases.xml.gz'

TASTEKID_OUT = '../data/tastekid_recs_json.pickle'
IFYOUDIG_ONE = '../data/ifyoudig1.pickle'
IFYOUDIG_TWO = '../data/ifyoudig2.pickle'
IFYOUDIG_OUT_OLD = '../data/ifyoudig_10000.pickle'

MUS_OFFSETS = '../data/musician_offsets.pickle'
MUS_NAMES = '../data/musician_names.pickle'
DBPEDIA = '../data/dbpedia/'

IYD = '../data/iyd.pickle'
IYDO = '../data/iyd_o.pickle'

# def init_graph(local=True):
#     return Graph(LOC_BINARY, LOC_DB)
#
#
# def dbpedia_offsets(dbpedia_dir = DBPEDIA, local=True):
#     import os
#     musicians = []
#     if local:
#         dbpedia_dir = dbpedia_dir[3:]
#     for file in os.listdir(dbpedia_dir):
#         if file.endswith(".tsv"):
#             with open(os.path.join(dbpedia_dir, file), 'r') as f:
#                 reader = unicodecsv.reader(f, delimiter='\t')
#                 next(reader)
#                 for row in reader:
#                     string = row[0][28:].replace('_', ' ')
#                     assert(type(string) == type(u''))
#                     tup = (string, float(row[1]))
#                     if tup not in musicians:
#                         musicians.append(tup)
#
#     if not local:
#         g = Graph(BINARY, DB)
#     else:
#         g = Graph(LOC_BINARY, LOC_DB)
#
#     from operator import itemgetter
#
#     return [x for x in sorted([(g.find(node), score) for node, score in musicians],
#                               reverse=True, key=itemgetter(1)) if x[0]]
#
#
# def scrape_tastekid():
#     key = '250576-Finalpro-3926RW4Q'
#     data = {}
#     musicians = parse_dbpedia('../data/10000_dbpedia_rank.tsv')
#     widgets = ['Scraping: ', Percentage(), Bar(), ETA()]
#     bar = ProgressBar(widgets=widgets, maxval=200).start()
#     for i, musician in enumerate(musicians):
#         url = "https://www.tastekid.com/api/similar?q="
#         params = {'k': key, 'type': 'music'}
#         url += str('+'.join(musician.split(' ')))
#
#         url_parts = list(urlparse.urlparse(url))
#         query = dict(urlparse.parse_qsl(url_parts[4]))
#         query.update(params)
#         url_parts[4] = urllib.urlencode(query)
#
#         response = urllib.urlopen(urlparse.urlunparse(url_parts))
#         data[musician] = json.loads(response.read())
#         bar.update(i)
#         if i == 200:
#             break
#
#     bar.finish()
#
#     with open(TASTEKID_OUT, 'wb') as f:
#         cPickle.dump(data, f)
#
#
# def parse_tastekid(filename):
#     data = cPickle.load(open(filename))
#     sim = {}
#     for musician, results in data.iteritems():
#         try:
#             sim[musician] = [item['Name'] for item in data[musician]['Similar']['Results']]
#         except KeyError:
#             continue
#
#     return sim
#
#
# def init_driver():
#     opts = webdriver.ChromeOptions()
#     opts.add_extension('../misc/Adblock-Plus-development-build_v1.12.4.1697.crx')
#     driver = webdriver.Chrome(chrome_options=opts)
#     driver.wait = WebDriverWait(driver, 5)
#     return driver
#
#
# def lookup(driver, query):
#     url = "http://ifyoudig.net/" + query
#     driver.get(url)
#     results = []
#
#     root = lxml.html.fromstring(driver.page_source)
#     for row in root.xpath('.//table[@class="correlations"]//tbody//tr'):
#         artist = row.xpath('.//td/a/text()')
#         # lh = row.xpath('.//td[@class="lh"]/text()')
#         if artist:
#             results.append(unicode(artist[0]))
#     return results
#
#
# def scrape_ifyoudig():
#     driver = init_driver()
#     musicians = cPickle.load(open(MUS_NAMES))
#     names = list(zip(*musicians)[0])
#     results = {}
#     old_data = cPickle.load(open(IFYOUDIG_OUT_OLD))
#     new_names = [x for x in names if x not in old_data]
#     assert(len(new_names) == 7770)
#     widgets = ['Scraping: ', Percentage(), Bar(), ETA()]
#     bar = ProgressBar(widgets=widgets, maxval=len(new_names)).start()
#     for i, musician in enumerate(new_names):
#         name = musician.split(' (')[0]
#         query = "-".join(name.split(" ")).lower()
#         result = lookup(driver, query)
#         results[musician] = result
#         bar.update(i)
#
#     bar.finish()
#
#     print("Cleaning up...")
#
#     data = {k: v for k, v in results.iteritems() if v}
#
#     with open(IFYOUDIG_TWO, 'wb') as f:
#         cPickle.dump(data, f)
#
#     driver.quit()


def train(order, trial, normalize, affine):
    iydo = cPickle.load(open(IYDO))
    mus = iydo.keys()

    with ExecTimer() as t:
        panther_scores = panther(mus, order=order, normalize=normalize, affine=affine)

    ordered_sim = {}
    key_errors = 0
    for node in mus:
        try:
            ordered = panther_scores[node].most_common()
            results = [key for key, _ in ordered if key in iydo]
            ordered_sim[node] = results
        except KeyError:
            key_errors += 1

    print('train(): Panther runtime: %f - Panther errors: %d' % (t.interval, key_errors))

    with open('../data/trials/sim_order_%d_norm_%d_affine_%d_trial_%d.pickle' % (order, normalize, affine, trial), 'wb') as f:
        cPickle.dump(ordered_sim, f)

    return ordered_sim, t.interval, key_errors


def main():
    results = {}
    times = {}
    iydo = cPickle.load(open(IYDO))
    for affine in [0, 1, 2, 4, 5, 6, 3, 7]:
        for normalize in [False]:
            max_order = MAX_ORDER
            if affine == 0:
                max_order = 10
            for order in range(1, 6):
                for trial in [1]:
                    print('main(): order = %d, normalize = %d, affine = %d - trial %d:' % (order, normalize, affine, trial))
                    ordered_sim, t_interval, key_errors = train(order, trial, normalize, affine)
                    results[(order, normalize, affine, trial)] = []
                    times[(order, normalize, affine, trial)] = (t_interval, key_errors)
                    for k in range(1, MAX_K + 1):
                        sample_size = 0
                        aps = []
                        zero_errors = 0
                        good_keys = []
                        for key, vals in ordered_sim.iteritems():
                            top_k_panther = vals[:k]
                            top_k_iyd = iydo[key][:k]
                            binary = [1 if x in top_k_iyd else 0 for x in top_k_panther]
                            prec = [(float(x) * binary[i]) / (i + 1) for i, x in enumerate(list(np.cumsum(binary)))]
                            try:
                                ap = sum(prec) / sum(binary)
                                if ap > 0.8:
                                    good_keys.append(key)
                                aps.append(ap)
                            except ZeroDivisionError:
                                zero_errors += 1
                                aps.append(0.0)
                                continue
                            sample_size += 1

                        print('main(): k: %d - Average precision: %.05f - Sample size: %d - ' \
                              'Zero errors: %d' % (k, float(np.mean(aps)), sample_size, zero_errors))

                        data = (float(np.mean(aps)), good_keys, sample_size, zero_errors)
                        results[(order, normalize, affine, trial)].append(data)

            with open('../data/results/run_%d_norm_%d_affine_%d.pickle' % (3, normalize, affine), 'wb') as f:
                cPickle.dump((results, times), f)

    with open('../data/results/run_%d.pickle' % 3, 'wb') as f:
        cPickle.dump((results,times), f)


if __name__ == "__main__":
    main()
