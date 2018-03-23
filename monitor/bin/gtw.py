#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @PROJECT : celery_monitor
# @Time    : 2018/3/23 15:11
# @Author  : Chen Yuelong
# @Mail    : yuelong.chen@oumeng.com.cn
# @File    : gtw.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import sys, os

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from monitor.utils.utils import gtwArgs
from monitor.monitorTasks.apptasks import go_to_work


def main():
    '''
    测试流程
    '''
    args = gtwArgs()
    task = go_to_work.delay(args.script,args.prefix,args.tmp)
    print('耐心等待结果')
    print('886')


if __name__ == '__main__':
    main()