from datetime import datetime
import logging


class KeywordsPipeline(object):

    # logfile_path = './logs/scrapy_log_' + str(datetime.utcnow().date()) + '.log'
    # logger = logging.getLogger('keywords')
    # logger.setLevel(logging.INFO)
    # fh = logging.FileHandler(logfile_path)
    # fh.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):

        with open('./logs/time_log.log', 'a') as time_log:
            time_log.write('{0}\n'.format(str(datetime.now())))
