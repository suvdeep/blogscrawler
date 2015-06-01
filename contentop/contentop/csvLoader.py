import subprocess
from playhouse.csv_loader import *
from dbmodels import Session, LogCrawler
from datetime import datetime


def loadCsv():
    SPIDERS = {}
    load_csv(Session, 'input/input.csv')

    for entry in Session.select():
        create_command = 'scrapy genspider -t multicrawl %s %s' % (entry.name, entry.domain)
        print create_command
        subprocess.call(create_command, shell=True)
        SPIDERS[entry.name] = entry.name.title()+'Spider'


        def logSession():
            LogCrawler.create(
                url=entry.url,
                domain=entry.name,
                status='Scheduled',
                datetime=datetime.now(),
            )

        #logSession()
    return SPIDERS
