#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @PROJECT : celery_monitor
# @Time    : 2018/3/20 13:43
# @Author  : Chen Yuelong
# @Mail    : yuelong.chen@oumeng.com.cn
# @File    : runshell.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import subprocess
import sys, os
from chardet import detect


def mkdirs(file):
    '''
    方法中任意一个文件（生成），都会检查目录是否存在，不论是否存在都建立目录
    :param file:任意文件
    :return:True
    '''
    try:
        filepath = os.path.dirname(os.path.abspath(file))
        print(file)
        print(filepath)
        os.makedirs(filepath,mode=0o755,exist_ok=True)
        return True
    except Exception as err:
        raise('目录建立错误：mkdirs(file)')




def Popen(cmd):
    '''
    只负责运行命令
    :param cmd:需要运行的命令
    :return:subprocess.Popen结果
    '''
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return p

def mntcmd(sPopen):
    '''
    监控subprocess.Popen运行
    :param sPopen:subprocess.Popen实例
    :return:标准输出，标准错误
    '''
    stdout, stderr = sPopen.communicate()
    codetype = detect(stdout)['encoding']
    return stdout.decode(codetype), stderr.decode(codetype)

def main():
    '''
    测试流程
    '''
    cmd = 'dir'
    print(Popen(cmd))
    # print(mkdirs(''))
    pass


if __name__ == '__main__':
    main()
