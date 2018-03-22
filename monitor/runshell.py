#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @PROJECT : celery_monitor
# @Time    : 2018/3/20 13:43
# @Author  : Chen Yuelong
# @Mail    : yuelong.chen@oumeng.com.cn
# @File    : runshell.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import os
import sys,os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
# print(sys.path)

from monitor.utils import plotResult,Popen,memory_stat,writefile


def runshell(script,prefix,tmp):
    '''
    运行脚本流程
    :param script:
    :param prefix:
    :return:标准输入输出的文件大小
    '''
    cache={}
    p = Popen(script)
    pid = p.pid
    osuffix='.o.{pid}'.format(pid=pid)
    esuffix='.e.{pid}'.format(pid=pid)
    file,stdout,stderr,cache=memory_stat(p,pid,cache,tmp)
    plotResult(file,prefix)
    osize,ounit=writefile(stdout,'{prefix}{osuffix}'.format(prefix=prefix,osuffix=osuffix))
    esize,eunit=writefile(stderr, '{prefix}{esuffix}'.format(prefix=prefix, esuffix=esuffix))
    # rmcache(cache)
    return '{}{}'.format(osize,ounit),'{}{}'.format(esize,eunit)



def main():
    '''
    测试流程
    '''
    cmd = 'sh /tmp/monitor.sh'
    tmp = '/tmp'
    prefix='/tmp/monitor'
    run(cmd,prefix,tmp)


if __name__ == '__main__':
    main()
