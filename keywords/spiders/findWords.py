import scrapy
import re
import tldextract
import logging

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.exceptions import DontCloseSpider
from datetime import datetime
from keywords.items import KeywordsItem
from keywords.config import Config


class FindWords(CrawlSpider):
    Config.load()
    name = "fw"

    # set logger
    logger = logging.getLogger('keywords')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('logs/scrapy' + str(datetime.utcnow().date()) + '.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # config variables
    exclude_urls = Config.config['exclude_urls']
    min_keywords = Config.config['keywords'][0]['min']
    min_keyword_s = Config.config['keywords'][1]['min']
    keywords_conf = Config.config['keywords'][0]['words']
    keywords_s_conf = Config.config['keywords'][1]['words']
    check_hyperlinks = Config.config['hyperlink_check']
    all_urls = []
    allowed_domains = []
    start_urls = []
    current_url = 0
    start_time = ""
    finished_time = ""

    for w in keywords_conf:
        if w in exclude_urls:
            exclude_urls.remove(w)

    with open('./logs/time_log.log', 'a') as time_log:
        time_log.write('Crawled domain,Started,Finished\n')

    # load urls from file
    with open('./crawling.txt', 'r') as ad:
        all_urls = ad.readline()

    allowed_domains_regex = []
    # creating rexeg for crawler
    extracted_url = tldextract.extract(all_urls)
    if extracted_url.subdomain != "":
        allowed_domains_regex.append(r'(.+|^)http://{0}.{1}.{2}(/.+)'.format(extracted_url.subdomain, extracted_url.domain, extracted_url.suffix))
    else:
        allowed_domains_regex.append(r'(.+|^)http://{0}.{1}(/.+)'.format(extracted_url.domain, extracted_url.suffix))

    # test code
    # if extracted_url.subdomain != "":
    #     allowed_domains_regex.append('{0}.{1}.{2}'.format(extracted_url.subdomain, extracted_url.domain, extracted_url.suffix))
    # else:
    #     allowed_domains_regex.append('{0}.{1}'.format(extracted_url.domain, extracted_url.suffix))

    # crawling rules
    rules = (Rule(LxmlLinkExtractor(allow=(allowed_domains_regex), deny=(exclude_urls)), callback="parse_items", follow=True), )

    start_urls.append(all_urls)
    logger.info('start crawling: {0}'.format(all_urls))

    with open('./logs/time_log.log', 'a') as time_log:
        time_log.write('{0},{1},'.format(all_urls, str(datetime.now())))

    # regex patterns for keywords
    if check_hyperlinks:
        pattern = {
            'keywords': [
                r'.*<a.*>.* (%s).*</a>.*' % '|'.join(keywords_conf),
                r'.*<a.*>.* (%s).*</a>.*' % '|'.join(keywords_s_conf),
            ]
        }
    else:
        pattern = {
            'keywords': [
                r'\b(%s)\b' % '|'.join(keywords_conf),
                r'\b(%s)' % '|'.join(keywords_s_conf),
            ]
        }

    remove_hyperlinks = re.compile(r'<a\s.*</a>', re.IGNORECASE)

    def parse_items(self, response):
        min_words = False
        min_words_s = False

        response_body_text = response.body.decode('utf-8')

        if self.check_hyperlinks:
            body_text = response_body_text
        elif not self.check_hyperlinks:
            body_text = self.remove_hyperlinks.sub('', response_body_text)

        # search with regex for all keywords in response body
        response_keywords = []
        response_with_score = []
        response_keywords = re.findall(self.pattern['keywords'][0], body_text, re.IGNORECASE)
        response_with_score = re.findall(self.pattern['keywords'][1], body_text, re.IGNORECASE)

        all_keywords = self.keywords_conf
        all_keywords.extend(self.keywords_s_conf)

        hasKeywordInURL = False
        for kw in all_keywords:
            if kw in response.url:
                hasKeywordInURL = True

        counters = {}
        # setting counters for first regex
        for conf in self.keywords_conf:
            conf = conf.lower().strip()
            counters[conf] = 0
        # count keywords from response body
        for word in response_keywords:
            word = word.lower().strip()
            counters[word] += 1

        counters_s = {}
        # setting counters for secund regex
        for conf in self.keywords_s_conf:
            conf = conf.lower().strip()
            counters_s[conf] = 0
        # count keywords with score
        for word in response_with_score:
            word = word.lower().strip()
            counters_s[word] += 1

        # checking conditions for min keywords in counters
        for counter in counters:
            if counters[counter] >= self.min_keywords:
                min_words = True

        if counters_s:
            for counter in counters_s:
                if counters_s[counter] >= self.min_keyword_s:
                    min_words_s = True
        else:
            min_words_s = True

        # if conditions is confirmed
        if (min_words and min_words_s) or hasKeywordInURL:
            extracted_domain = tldextract.extract(response.url)
            source_domain = '{0}.{1}'.format(extracted_domain.domain, extracted_domain.suffix)
            source_subdomain = extracted_domain.subdomain
            source_url = response.url

            try:
                hxs = Selector(response)
            except:
                self.logger.error('Error link: {0}\n'.format(response.url))
                return

            item = KeywordsItem()

            item['DOMAIN'] = source_domain
            item['FQDN'] = '{0}.{1}'.format(source_subdomain, source_domain)
            item['URL'] = source_url
            item['title'] = hxs.xpath('//title/text()').extract()
            item['description'] = hxs.xpath('//meta[@name=\'description\']/@content').extract()
            item['keywords'] = hxs.xpath('//meta[@name=\'keywords\']/@content').extract()
            item['hyperlinks'] = 0
            item['keywordInURL'] = hasKeywordInURL
            if self.check_hyperlinks:
                item['hyperlinks'] = len(response_keywords)

            for result in counters:
                item[result] = counters[result]

            for result in counters_s:
                item[result] = counters_s[result]

            return item
