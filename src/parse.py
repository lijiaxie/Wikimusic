import csv

def parse(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            print row

def main():
    parse('../data/10000_dbpedia_rank.tsv')
    pass

if __name__ == "__main__":
    main()