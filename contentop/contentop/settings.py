# -*- coding: utf-8 -*-

# Scrapy settings for contentop project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'contentop'

SPIDER_MODULES = ['contentop.spiders']
NEWSPIDER_MODULE = 'contentop.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'contentop (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'contentop.pipelines.DuplicatesPipeline': 175,
    'contentop.pipelines.ContentopPipeline': 800,
}
#DUPEFILTER_CLASS = 'contentop.dupfilter.SeenURLFilter'
#DUPEFILTER_CLASS = 'scrapy.dupefilter.RFPDupeFilter'

LOG_LEVEL = 'ERROR'
AJAXCRAWL_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'contentop.myMiddleware.DuplicateInDb': 150,
}

SPIDER_MIDDLEWARES = {
    'contentop.myMiddleware.RequestErrorLog': 49,
}


TELNETCONSOLE_ENABLED = False

###################SCAPRERA TWEAKS###################

# CONCURRENT_REQUESTS = 32
# CONCURRENT_REQUESTS_PER_DOMAIN = 32
# AUTOTHROTTLE_ENABLED = False
# DOWNLOAD_TIMEOUT = 600