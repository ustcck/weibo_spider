# encoding=utf-8
import dj_database_url
import MySQLdb

from twisted.internet import defer
from twisted.enterprise import adbapi
from scrapy.exceptions import NotConfigured

from items import InformationItem, TweetsItem


class MySQLPipeline(object):
    """
    A spider that writes to MySQL databases
    """

    @classmethod
    def from_crawler(cls, crawler):
        """Retrieves scrapy crawler and accesses pipeline's settings"""

        # Get MySQL URL from settings
        mysql_url = crawler.settings.get('MYSQL_PIPELINE_URL', None)

        # If doesn't exist, disable the pipeline
        if not mysql_url:
            raise NotConfigured

        # Create the class
        return cls(mysql_url)

    def __init__(self, mysql_url):
        """Opens a MySQL connection pool"""

        # Store the url for future reference
        self.mysql_url = mysql_url
        # Report connection error only once
        self.report_connection_error = True

        # Parse MySQL URL and try to initialize a connection
        conn_kwargs = MySQLPipeline.parse_mysql_url(mysql_url)
        self.dbpool = adbapi.ConnectionPool('MySQLdb', charset='utf8', use_unicode=True, connect_timeout=5,
                                            **conn_kwargs)
        # self.Information = db["Information"]
        # self.Tweets = db["Tweets"]

    def close_spider(self, spider):
        """Discard the database pool on spider close"""
        self.dbpool.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        """Processes the item. Does insert into MySQL"""

        logger = spider.logger

        if isinstance(item, InformationItem):
            try:
                yield self.dbpool.runInteraction(self.do_replace_information, item)
            except MySQLdb.OperationalError:
                if self.report_connection_error:
                    logger.error("Can't connect to MySQL: %s" % self.mysql_url)
                    self.report_connection_error = False

            defer.returnValue(item)

        if isinstance(item, TweetsItem):
            try:
                yield self.dbpool.runInteraction(self.do_replace_tweet, item)
            except MySQLdb.OperationalError:
                if self.report_connection_error:
                    logger.error("Can't connect to MySQL: %s" % self.mysql_url)
                    self.report_connection_error = False

            defer.returnValue(item)

            # except:
            #     print traceback.format_exc()

            # Return the item for the next stage

    @staticmethod
    def do_replace_tweet(tx, item):
        """Does the actual REPLACE INTO"""

        sql = """REPLACE INTO Tweets (ID, Comment, Likes, Tranfer, Content, PubTime, Tools, WeiboID, Co_oridinates, Topic)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        args = (
            item["ID"],
            item["Comment"],
            item["Likes"],
            item["Transfer"],
            item["Content"],
            item["PubTime"],
            item["Tools"],
            item["WeiboID"],
            item["Co_oridinates"],
            item["Topic"],
        )

        tx.execute(sql, args)

    @staticmethod
    def do_replace_information(tx, item):
        """Does the actual REPLACE INTO"""

        sql = """REPLACE INTO Information (WeiboID, NickName, Gender, Province, City, Signature, Birthday, Num_Tweets, Num_Follows, Num_Fans, Marriage, URL)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        args = (
            item["Weibo_ID"],
            item["NickName"],
            item["Gender"],
            item["Province"],
            item["City"],
            item["Signature"],
            item["Birthday"],
            item["Num_Tweets"],
            item["Num_Follows"],
            item["Num_Fans"],
            item["Marriage"],
            item["URL"],
        )

        tx.execute(sql, args)

    @staticmethod
    def parse_mysql_url(mysql_url):
        """
        Parses mysql url and prepares arguments for
        adbapi.ConnectionPool()
        """

        params = dj_database_url.parse(mysql_url)

        conn_kwargs = {}
        conn_kwargs['host'] = params['HOST']
        conn_kwargs['user'] = params['USER']
        conn_kwargs['passwd'] = params['PASSWORD']
        conn_kwargs['db'] = params['NAME']
        conn_kwargs['port'] = params['PORT']

        # Remove items with empty values
        conn_kwargs = dict((k, v) for k, v in conn_kwargs.iteritems() if v)

        return conn_kwargs
