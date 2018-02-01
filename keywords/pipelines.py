from datetime import datetime
import logging
import MySQLdb


class KeywordsPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='Driver',
            charset="utf8",
            use_unicode=True
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """INSERT INTO currency 
                (DOMAIN, FQDN, URL, title, description, keywords, hyperlinks, keywordInURL) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                    item['DOMAIN'].encode('utf-8'), item['FQDN'].encode('utf-8'),
                    item['URL'].encode('utf-8'), item['title'].encode('utf-8'),
                    item['description'].encode('utf-8'), item['keywords'].encode('utf-8'),
                    item['hyperlinks'].encode('utf-8'), item['keywordInURL'].encode('utf-8')
                )
            )

            self.conn.commit()

        except MySQLdb.Error, e:
            print("Error %d: %s" % (e.args[0], e.args[1]))

        return item

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):

        with open('./logs/time_log.log', 'a') as time_log:
            time_log.write('{0}\n'.format(str(datetime.now())))
