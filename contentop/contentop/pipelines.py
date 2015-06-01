# -*- coding: utf-8 -*-
import os
from contentop.dbmodels import Crawled,LogError
from scrapy.exceptions import DropItem
from scrapy import log
from datetime import date, datetime
import hashlib

#today = date.today()


class ContentopPipeline(object):

    def process_item(self, item, spider):
        today = date.today()
        # filename = hashlib.md5(item['url']).hexdigest()
        if  item['description'] not in ([], '', None, ['']):

            # title = [str(x) for x in item['title']]
            # description =  [str(x) for x in item['description']]
            # category =  [str(x) for x in item['category']]

            try:
                Crawled.create(url=item['url'], domain=item['domain'], title=item['title'], description=item['description'] , category=item['category'], date = today)
                # path = os.path.join('data', item['domain'].split('.')[0])
                # if not os.path.exists(path):
                #     os.makedirs(path)
                # with open( os.path.join(path, filename), 'w+') as f:
                #     content = u''.join(item['description'])
                #     log (content, level=log.ERROR)
                #     f.write(content)
                # log.msg('--------Content found at %s and added to database ---' % item['url'], level=log.ERROR)
            except:
                log.msg('Error updating scrape to Database', level=log.ERROR)
        else:
            LogError.create(url=item['url'], errorcode=0, datetime=datetime.now())
            raise DropItem ('-------00000------Empty Item Found, URL logged in LogErrors ------------')
        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        if (item['url'] in self.urls_seen):
            raise DropItem("Duplicate item found: %s" % item['url'])
        else:
            self.urls_seen.add(item['url'])
        return item
