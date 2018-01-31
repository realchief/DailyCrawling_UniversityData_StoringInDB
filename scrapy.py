import csv
import os
import time
import tldextract
import requests

for dirpath, dirnames, files in os.walk('./logs/'):
    if files:
        os.system('rm ./logs/*')

with open('schools.txt', 'r') as roch:
    domains = csv.reader(roch, delimiter=",")
    for line in domains:
        if line[0] != 'domain':
            fqdn = ''
            domain = tldextract.extract(line[0])
            result = domain.domain
            if line[0].startswith('http'):
                fqdn = line[0]
            else:
                fqdn = 'https://{0}/'.format(line[1])
            with open('crawling.txt', 'w') as dom:
                dom.write(fqdn)
            os.system('scrapy crawl fw -o results_gre11.csv')

            time.sleep(10000)

os.system('rm crawling.txt')
