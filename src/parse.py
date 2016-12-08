import csv
from xml.etree import ElementTree as etree
from panther import *
from params import *
import cPickle
import json
import urllib
import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import lxml.html

XML_ARTISTS = '../data/discogs_20160201_artists.xml'
XML_RELEASES = '../data/discogs_20160101_releases.xml.gz'

TASTEKID_OUT = '../data/tastekid_recs_json.pickle'
IFYOUDIG_OUT = '../data/ifyoudig_10000.pickle'


def xml(filename):
    with open(filename) as xmlfile:
        root = etree.parse(xmlfile).getroot()
        print(root)


def parse_musicians(filename):
    musicians = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        for row in reader:
            string = row[0].split("/")[-1].replace('_', ' ')
            try:
                uni_str = unicode(string)
                musicians.append(uni_str)
            except UnicodeDecodeError:
                continue

    return musicians


def scrape_tastekid():
    key = '250576-Finalpro-3926RW4Q'
    data = {}
    musicians = parse_musicians('../data/10000_dbpedia_rank.tsv')
    widgets = ['Scraping: ', Percentage(), Bar(), ETA()]
    bar = ProgressBar(widgets=widgets, maxval=200).start()
    for i, musician in enumerate(musicians):
        url = "https://www.tastekid.com/api/similar?q="
        params = {'k': key, 'type': 'music'}
        url += str('+'.join(musician.split(' ')))

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urllib.urlencode(query)

        response = urllib.urlopen(urlparse.urlunparse(url_parts))
        data[musician] = json.loads(response.read())
        bar.update(i)
        if i == 200:
            break

    bar.finish()

    with open(TASTEKID_OUT, 'wb') as f:
        cPickle.dump(data, f)


def parse_tastekid(filename):
    data = cPickle.load(open(filename))
    sim = {}
    for musician, results in data.iteritems():
        try:
            sim[musician] = [item['Name'] for item in data[musician]['Similar']['Results']]
        except KeyError:
            continue

    return sim


def init_driver():
    opts = webdriver.ChromeOptions()
    opts.add_extension('../misc/Adblock-Plus-development-build_v1.12.4.1697.crx')
    driver = webdriver.Chrome(chrome_options=opts)
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    url = "http://ifyoudig.net/" + query
    driver.get(url)
    results = []

    root = lxml.html.fromstring(driver.page_source)
    for row in root.xpath('.//table[@class="correlations"]//tbody//tr'):
        artist = row.xpath('.//td/a/text()')
        lh = row.xpath('.//td[@class="lh"]/text()')
        if artist and lh:
            results.append((unicode(artist[0]), unicode(lh[0])))
    return results


def scrape_ifyoudig():
    driver = init_driver()
    musicians = parse_musicians('../data/10000_dbpedia_rank.tsv')
    results = {}
    times = []
    widgets = ['Scraping: ', Percentage(), Bar(), ETA()]
    bar = ProgressBar(widgets=widgets, maxval=len(musicians)).start()
    for i, musician in enumerate(musicians):
        name = musician.split(' (')[0]
        query = "-".join(name.split(" ")).lower()
        try:
            with ExecTimer() as t:
                result = lookup(driver, query)
        finally:
            # print "Lookup time: %.03f" % t.interval
            times.append(t.interval)
        results[musician] = result
        bar.update(i)

    # print "Average lookup time: %.05f" % (float(sum(times)) / len(times))

    bar.finish()

    with open(IFYOUDIG_OUT, 'wb') as f:
        cPickle.dump(results, f)

    driver.quit()


def train():
    musicians = parse_musicians('../data/10000_dbpedia_rank.tsv')
    g = Graph(BINARY, DB)

    scores = panther(musicians)
    with open('../data/panther_scores_dicts.pickle', 'wb') as f:
        cPickle.dump(scores, f)

    # scores = cPickle.load(open('../data/panther_scores_dicts.pickle'))
    top_k_sim = {}
    key_errors = 0
    for node in musicians:
        offset = g.find(node)
        if offset is not None:
            try:
                top_k = scores[offset].most_common()
                top_k_trans = [(g.name(offset), score) for offset, score in top_k]
                top_k_sim[node] = top_k_trans
            except KeyError:
                key_errors += 1

    print "Total errors: %d" % key_errors

    with open('../data/top_%d_sim.pickle' % k, 'wb') as f:
        cPickle.dump(top_k_sim, f)


def main():
    parse_tastekid(TASTEKID_OUT)


if __name__ == "__main__":
    scrape_ifyoudig()
