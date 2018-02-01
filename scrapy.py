import csv
import os
import time
import tldextract
from keywords.config import Config

for dirpath, dirnames, files in os.walk('./logs/'):
    if files:
        os.system('rm ./logs/*')

with open('schools1.txt', 'r') as roch:
    Config.load()
    domains = csv.reader(roch, delimiter=",")
    for line in domains:
        if line[0] != 'domain':
            fqdn = ''
            domain = tldextract.extract(line[0])
            result = domain.domain
            if line[0].startswith('http'):
                fqdn = line[0]
            else:
                fqdn = 'http://{0}/'.format(line[1])
            with open('crawling.txt', 'w') as dom:
                dom.write(fqdn)

            if Config.config['write_file']:
                os.system('scrapy crawl fw -o results_gre3.csv')
            if Config.config['write_table']:
                os.system('scrapy crawl fw')
            time.sleep(20)


os.system('rm crawling.txt')
