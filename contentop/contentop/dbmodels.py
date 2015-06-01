from peewee import *
#from playhouse.csv_loader import *


db = MySQLDatabase('contentop', user='root', threadlocals=True)

## base db template ###


def createDb(dbname):
    db = MySQLDatabase(dbname, user='root', threadlocals=True)
    _initiateDB()
    print 'Creating Database %s ' % dbname

#createDb()

class BaseDb(Model):
    class Meta:
        database = db

#### crawled data STORE MODEL #####


class Session(BaseDb):
    #url,domain,title,description,category,restriciton,crawled
    name = CharField()
    url = CharField()
    domain = CharField()
    title = CharField()
    description = CharField()
    category = CharField()
    allow = CharField(default='')
    restrict = CharField(null=True)
    crawled = BooleanField(default=False)


class Crawled(BaseDb):
    url = CharField(unique=True)
    domain = CharField()
    title = CharField()
    description = TextField()
    category= TextField()
    date = DateField()


class LogCrawler(BaseDb):
    url = CharField()
    domain = CharField()
    status = CharField()
    datetime = DateTimeField()


class LogError(BaseDb):
    url = CharField()
    errorcode = IntegerField()
    datetime = DateTimeField()


#########################################


#########################################

def clearSession():
    db.execute_sql('TRUNCATE TABLE session')

def _initiateDB():
    for item in [Session, Crawled, LogCrawler, LogError]:
        try:
            db.create_tables([item])
        except:
            try:
                db.drop_tables([item])
                db.create_tables([item])
            except:
                pass
    print "DB RESET : Database flushed and recreated"

if __name__ == '__main__':
    _initiateDB()
