#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @PROJECT : celery_monitor
# @Time    : 2018/3/21 13:48
# @Author  : Chen Yuelong
# @Mail    : yuelong.chen@oumeng.com.cn
# @File    : apptasks.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from monitor.celery import app
import subprocess
from monitor.utils import randomFileName
from monitor.runshell import runshell



@app.task
def generateFileDirs():
    file, _ = randomFileName({})
    cmd = 'perl /home/PROJECTS/celery_monitor/tests/test.pl /home/PROJECTS/TMP/{file} {file}'.format(
        file=file
    )
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    return cmd


@app.task
def go_to_work(script, prefix, tmp='/tmp/'):
    '''
    提交脚本，并指明log输出前缀（.o,.e,.csv,.pdf）
    :param script: 需要执行的脚本
    :param prefix: 输出log的前缀
    :return:
    '''
    osize, esize = runshell(script, prefix, tmp)
    return osize


def main():
    '''
    测试流程
    '''
    pass


if __name__ == '__main__':
    main()
