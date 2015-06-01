from scrapy import log
from scrapy.exceptions import IgnoreRequest
from contentop.dbmodels import Crawled, LogError
from datetime import datetime


class DuplicateInDb(object):

    def process_request(self, request, spider):
        if Crawled.select().where(Crawled.url == request.url).exists():
            log.msg("-------------INFO : Page was earlier crawled and is already present in Database--------------- " + request.url, level=log.ERROR)
            raise IgnoreRequest()


class RequestErrorLog(object):

    def process_spider_input(self, response, spider):
            if response.status not in (200, 201, 202, 301, 302):
                LogError.create(url=response.url, errorcode = response.status, datetime = datetime.now() )
                log.msg(' ---------------------------------INFO : Page Retrieval Error Logged in Database--------------------------', level=log.ERROR)
