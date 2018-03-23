#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @PROJECT : celery_monitor
# @Time    : 2018/3/21 13:13
# @Author  : Chen Yuelong
# @Mail    : yuelong.chen@oumeng.com.cn
# @File    : celery_app.py
# @Software: PyCharm

from __future__ import absolute_import,unicode_literals
from celery import Celery
import pymysql
pymysql.install_as_MySQLdb()

from monitor.utils.utils import getConfig



def createBacken(config):
    cf = getConfig(config)
    host='localhost'
    port=3306
    database='test'
    user='root'
    passwd=''
    if cf.has_option('mysql','host'):
        host = cf.get('mysql','host')
    if cf.has_option('mysql','port'):
        port = cf.get('mysql','port')
    if cf.has_option('mysql','database'):
        database = cf.get('mysql','database')
    if cf.has_option('mysql','user'):
        user = cf.get('mysql','user')
    if cf.has_option('mysql','passwd'):
        passwd = cf.get('mysql','passwd')
    backen = 'db+mysql://{user}:{passwd}@{host}/{database}'.format(
        user=user,
        passwd=passwd,
        host=host,
        database=database
    )
    return backen


def createApp(config):
    backend = createBacken(config)
    # backend='db+mysql://fangkc:kchi@bintest@localhost/celery_test'
    # print(backen)

    broker = 'pyamqp://guest@localhost//'
    # backen = 'pyamqp://guest@localhost//'
    app=Celery('monitor',
               broker=broker,
               backend=backend,
               include=['monitorTasks.apptasks'])
    return app

app = createApp('/home/PROJECTS/celery_monitor/configure.ini')

def main():
    # app.start()
    pass

if __name__ == '__main__':
    main()