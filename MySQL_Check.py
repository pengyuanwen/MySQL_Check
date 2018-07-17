#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from conf.MySQLApi import DB_API
from conf.Read_Write_File import Handler_file



class MySQL_Check():

    def __init__(self):
        self.file_op = Handler_file(filepath)

    def get_host(self):
        self.all_host = self.file_op.Read_File()

    def Check_Slave_Status(self):
        sql = "show slave status;"
        for ip_list in self.all_host:
            ip = ip_list.strip()
            print ip
            self.mysql_op = DB_API(ip)
            res = self.mysql_op.query_db(sql)
            for re in res:
                #print re
                master_host = re[1]
                Master_Log_File = re[5]
                Read_Master_Log_Pos = re[6]
                Relay_Master_Log_File = re[9]
                Exec_Master_Log_Pos = re[21]
                Slave_IO_Running = re[10]
                Slave_SQL_Running = re[11]
                Seconds_Behind_Master = re[32]
                print "master_host:%s,Master_Log_File:%s,Read_Master_Log_Pos:%s,Relay_Master_Log_File:%s,Exec_Master_Log_Pos:%s,Slave_IO_Running:%s,Slave_SQL_Running:%s" \
                % (master_host,Master_Log_File,Read_Master_Log_Pos,Relay_Master_Log_File,Exec_Master_Log_Pos,Slave_IO_Running,Slave_SQL_Running)



if __name__ == '__main__':
    filepath = sys.argv[1]
    mysql_health = MySQL_Check()
    mysql_health.get_host()
    mysql_health.Check_Slave_Status()




