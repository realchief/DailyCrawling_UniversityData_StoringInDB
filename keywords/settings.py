from .config import Config
Config.load()

BOT_NAME = 'keywords'

SPIDER_MODULES = ['keywords.spiders']
NEWSPIDER_MODULE = 'keywords.spiders'
LOG_LEVEL = "DEBUG"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'keywords'

# set the fifo queue
DEPTH_LIMIT = Config.config['depth']
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'


# disable redirect from users login pages for faster crawling
REDIRECT_ENABLED = False
RETRY_ENABLED = False
COOKIES_ENABLED = False
LOG_ENABLED = True
CONCURRENT_ITEMS = 25
CONCURRENT_REQUESTS = 25
CONCURRENT_REQUESTS_PER_IP = 2
DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 120
DNSCACHE_ENABLED = True

AJAXCRAWL_ENABLED = True

ITEM_PIPELINES = {
    'keywords.pipelines.KeywordsPipeline': 300,
}

# spider middlewares
SPIDER_MIDDLEWARES = {
    # 'keywords.middlewares.RemoveDoctype': 543,
    # 'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None
}

# downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'keywords.middlewares.IgnoreExtensions': 543,
}

# CSV exporter
FEED_EXPORTERS = {
    'csv': 'keywords.exporters.keywordsCsvItemExporter'
}

FIELDS_TO_EXPORT = [
    'DOMAIN',
    'FQDN',
    'URL',
    'keywordInURL',
    'title',
    'description',
    'keywords',
    'hyperlinks'
]

CSV_DELIMITER = ','

