import csv
from xml.etree import ElementTree as etree
from models import *

XML_ARTISTS = '../data/discogs_20160201_artists.xml'
XML_RELEASES = '../data/discogs_20160101_releases.xml.gz'

BINARY = '../data/wikidata/indexbi.bin'
DB = '../data/wikidata/xindex-nocase.db'


def xml(filename):
    with open(filename) as xmlfile:
        root = etree.parse(xmlfile).getroot()
        print(root)


def parse(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            print row

def main():
    g = Graph(binary=BINARY, db_path=DB)
    pass

if __name__ == "__main__":
    main()
