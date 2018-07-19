#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb


class DB_API(object):

    def __init__(self,host,*args):
        self.host = host
        self.ret = args

        try:
            self.conn = MySQLdb.connect(
                host = self.host,
                port = 3306,
                user = '',
                passwd = '',
                db = '',
                charset = 'utf8'
            )
        except MySQLdb.Error,e:
            errormag = 'Connot connect to server\nERROR (%s): %s' %(e.args[0],e.args[1])
            print errormag
            sys,exit()

    def query_db(self,select_sql):
        query_cursor = self.conn.cursor()
        query_cursor.execute(select_sql)
        query_result = query_cursor.fetchall()
        self.conn.commit()
        return query_result


    def insert_db(self,insert_sql):
        cursor = self.conn.cursor()
        cursor.execute(insert_sql)
        self.conn.commit()
        cursor.close()

    def delete_db(self,delete_sql):
        cursor = self.conn.cursor()
        cursor.execute(delete_sql)
        self.conn.commit()
        cursor.close()

    def update_db(self,update_sql):
        cursor = self.conn.cursor()
        cursor.execute(update_sql)
        self.conn.commit()
        cursor.close()


    def __del__(self):
        if self.host is not None:
            self.conn.close()