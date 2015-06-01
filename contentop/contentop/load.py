import subprocess


from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from csvLoader import loadCsv

from dbmodels import clearSession, LogCrawler

#################################################################################

# Cleanup before starting a new crawl

# clear all the old spiders from the directory
try:
    subprocess.call('touch spiders/__init__.py; \
        rm spiders/*.py*; touch spiders/__init__.py; rm -R *.pyc', shell=True)
except:
    print 'Could not clean old Spiders or there were no \
        Spiders to start with'
clearSession()

##################################################################################

spiderfilename = ""
TO_CRAWL = []
RUNNING_CRAWLERS = []


csvLoad = loadCsv()  # load csv into Session Database and Create Spiders


#unpack csv specs and feed to Crawler Initator
for key, value in csvLoad.iteritems():
    importString = "from spiders." + key + ' import ' + value
    exec(importString)
    TO_CRAWL.append(value)


def spider_closing(spider):
    global spiderfilename

    """
    Activates on spider closed signal
    """
    log.msg("Spider closed: %s" % spider, level=log.INFO)
    RUNNING_CRAWLERS.remove(spider)
    deleteSpiderFile()
    #logentry = LogCrawler.get().where(LogC.domain=spiderfilename).orderby().update(status = 'Finished')
    log.msg(RUNNING_CRAWLERS, level=log.ERROR)
    if not RUNNING_CRAWLERS:
        reactor.stop()
        clearSession()


# End of a glorius life of spider # deletes spider files
def deleteSpiderFile():
    delete_command = 'rm spiders/%s.py*' % spiderfilename
    log.msg('--------------Spider - %s ,had an eventful life ---\
        -------------' % spiderfilename, level=log.WARNING)
    subprocess.call(delete_command, shell=True)



# start logger
log.start(loglevel=log.DEBUG)


# set up the crawler and start to crawl one spider at a time
for spider in TO_CRAWL:
    spiderfilename = csvLoad.keys()[csvLoad.values().index(spider)]
    log.msg(spiderfilename, level=log.INFO)
    settings = get_project_settings()

    # crawl responsibly
    settings.set("USER_AGENT", "AAA")
    crawler = Crawler(settings)
    crawler_obj = eval(spider+'()')
    RUNNING_CRAWLERS.append(crawler_obj)

    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(crawler_obj)
    crawler.start()

# blocks process; so always keep as the last statement
reactor.run()
