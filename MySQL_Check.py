#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from MySQL_conf.MySQLApi import DB_API
from MySQL_conf.Read_Write_File import Handler_file


class MessageUint(object):
    help = \
        """
    --------------------------------------------------------
    MySQL_Check.py Tools Are Userd to Check MySQL BaseInfo 
    
    Usage: MySQL_Check.py [filepath|filename]              
    
    OPTIONS:                                               
        Check_Slave_Status 检查主从状态                      
        Get_priv_sql       获取数据库权限表
    
    Example:
        MySQL_Check.py iplist 
    
    --------------------------------------------------------
        """


class MySQL_Check(object):
    def __init__(self):
        self.file_op = Handler_file(filepath)

        self.all_user_info = []

    def get_host(self):
        self.all_host = self.file_op.Read_File()

    # 查看数据库主从复制状态
    def Check_Slave_Status(self):
        sql = "show slave status;"
        for ip_list in self.all_host:
            ip = ip_list.strip()
            self.mysql_op = DB_API(ip)
            res = self.mysql_op.query_db(sql)
            for re in res:
                master_host = re[1]
                Master_Log_File = re[5]
                Read_Master_Log_Pos = re[6]
                Relay_Master_Log_File = re[9]
                Exec_Master_Log_Pos = re[21]
                Slave_IO_Running = re[10]
                Slave_SQL_Running = re[11]
                Seconds_Behind_Master = re[32]
                if Master_Log_File == Relay_Master_Log_File and Read_Master_Log_Pos == Exec_Master_Log_Pos and Slave_IO_Running == "Yes" and Slave_SQL_Running == "Yes":
                    print "复制状态正常，主库IP:%s,从库IP:%s,延迟时间：%s" % (master_host, ip, Seconds_Behind_Master)
                else:
                    print "复制状态错误，请检查！！！"

    # 获取数据库权限
    def Get_priv_sql(self):
        sql = "select substr(version(),1,3);"
        for ip_list in self.all_host:
            ip = ip_list.strip()
            print ip
            self.mysql_op = DB_API(ip)
            vers = self.mysql_op.query_db(sql)
            if vers[0][0] == "5.7":
                user_sql = "SELECT USER,HOST,AUTHENTICATION_STRING FROM mysql.user where AUTHENTICATION_STRING != '';"
                user_info = self.mysql_op.query_db(user_sql)
                for item in user_info:
                    user = item[0]
                    host = item[1]
                    passwd = item[2]
                    create_user = "CREATE USER \'%s\'@\'%s\' IDENTIFIED BY PASSWORD \'%s\';" % \
                                  (user, host, passwd)
                    print create_user
                    grant_sql = "show grants for \'%s\'@\'%s\';" % (user, host)
                    res_all = self.mysql_op.query_db(grant_sql)
                    for res in res_all:
                        print res[0] + ';'
            elif vers[0][0] == "5.6" or vers[0][0] == "5.5":
                user_sql = "select user,host,password from mysql.user where password != '';"
                user_info = self.mysql_op.query_db(user_sql)
                for item in user_info:
                    user = item[0]
                    host = item[1]
                    passwd = item[2]
                    grant_sql = "show grants for \'%s\'@\'%s\';" % (user, host)
                    res_all = self.mysql_op.query_db(grant_sql)
                    format_result = "%s\'%s\'; " % (res_all[0][0][:-8], passwd)
                    print format_result


def input_result():
    if len(sys.argv) != 2:
        print MessageUint.help
    else:
        mysql_health = MySQL_Check()
        mysql_health.get_host()
        while True:
            print MessageUint.help
            option = raw_input('请输出需要检查的参数:')
            if option == "Check_Slave_Status":
                mysql_health.Check_Slave_Status()

                continue
            if option == "Get_priv_sql":
                mysql_health.Get_priv_sql()

            if option in ("exit", "quit"):
                exit()


if __name__ == '__main__':
    filepath = sys.argv[1]
    input_result()



