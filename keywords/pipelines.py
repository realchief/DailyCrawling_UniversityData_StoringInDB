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
        if not self.checkTableExists('std_univ_crawl_courses'):
            self.cursor.execute("""CREATE TABLE std_univ_crawl_courses ( std_univ_crawl_id int(11) NOT NULL AUTO_INCREMENT, UNITID int(10) NOT NULL, SCHOOLID int(10) DEFAULT NULL, CRAWL_COURSE_TYPE tinyint(1) NOT NULL COMMENT 'graduate , undergraduate or phd courses', SCHOOL_NAME varchar(500) DEFAULT NULL, COURSE_URL varchar(2000) DEFAULT NULL, COURSE_NAME varchar(800) DEFAULT NULL, DEGREE_NAME varchar(800) DEFAULT NULL, CIP_CODE_SEARCH varchar(300) DEFAULT NULL, MATCHING_CIPS varchar(800) DEFAULT NULL COMMENT 'CIPS which have been matched', MATCH_KEYWORDS varchar(800) DEFAULT NULL, STATUS tinyint(1) NOT NULL DEFAULT '1', KEYWORD_GRE varchar(300) DEFAULT '0', KEYWORD_COURSE varchar(300) DEFAULT '0', KEYWORD_SCHOLAR varchar(300) DEFAULT '0', CREATED_DATE timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (std_univ_crawl_id) ) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8;""")
        if not self.checkTableExists('std_univ_courses_py'):
            self.cursor.execute("""CREATE TABLE std_univ_courses_py ( STD_UNIV_PY_ID int(10) NOT NULL AUTO_INCREMENT, STD_UNIV_CRAWL_COURSES_ID int(11) DEFAULT NULL, DOMAIN varchar(2000) NOT NULL, FQDN varchar(500) NOT NULL, COURSE_URL varchar(2000) NOT NULL, KEY_BOOL varchar(50) NOT NULL, TITLE varchar(2000) DEFAULT NULL, DESCRIPTION varchar(2000) DEFAULT NULL, KEYWORD varchar(2000) DEFAULT NULL, HYPERLINK tinyint(1) DEFAULT NULL, COLUMN_1 int(4) DEFAULT NULL, COLUMN_2 int(4) DEFAULT NULL, COLUMN_3 int(4) DEFAULT NULL, COLUMN_4 int(4) DEFAULT NULL, COLUMN_5 int(4) DEFAULT NULL, UNITID int(10) DEFAULT NULL, CIPCODE varchar(50) DEFAULT NULL COMMENT 'what cip. ', KEYWORD_SEARCH_1 varchar(200) DEFAULT NULL COMMENT 'update with keywords this data was searched for. ', KEYWORD_SEARCH_2 varchar(200) DEFAULT NULL, KEYWORD_SEARCH_3 varchar(200) DEFAULT NULL, KEYWORD_SEARCH_4 varchar(200) DEFAULT NULL, ACTIVE tinyint(1) NOT NULL DEFAULT '1', UPDATED_DATE timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (STD_UNIV_PY_ID) ) ENGINE=InnoDB AUTO_INCREMENT=56641 DEFAULT CHARSET=utf8;""")
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

    def checkTableExists(self, tablename):
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM Driver.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        if self.cursor.fetchone()[0] == 1:
            return True

        return False

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        with open('./logs/time_log.log', 'a') as time_log:
            time_log.write('{0}\n'.format(str(datetime.now())))
