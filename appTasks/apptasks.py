#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @PROJECT : celery_monitor
# @Time    : 2018/3/21 13:48
# @Author  : Chen Yuelong
# @Mail    : yuelong.chen@oumeng.com.cn
# @File    : apptasks.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
from monitor.celery import app
import subprocess
from monitor.utils import randomFileName


@app.task
def generateFileDirs():
    file=randomFileName()
    cmd='perl /home/PROJECTS/celery_monitor/tests/test.pl /home/PROJECTS/TMP/{file} {file}'.format(
        file=file
    )
    # cmd='touch /home/gogogo.txt'
    # cmd='mkdir -p /home/TMP/{}'.format(file)
    p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.communicate()
    # return file
    return cmd


def main():
    '''
    测试流程
    '''
    pass


if __name__ == '__main__':
    main()