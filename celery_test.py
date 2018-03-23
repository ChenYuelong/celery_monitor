#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @PROJECT : celery_monitor
# @Time    : 2018/3/21 16:05
# @Author  : Chen Yuelong
# @Mail    : yuelong.chen@oumeng.com.cn
# @File    : celery_test.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
from monitor.monitorTasks.apptasks import generateFileDirs

def main():
    '''
    测试流程
    '''
    testlist = []
    for i in range(100):
        testlist.append(generateFileDirs.delay())
    for i in testlist:
        print(i.status)
    for i in testlist:
        print(i.info)
    pass


if __name__ == '__main__':
    main()