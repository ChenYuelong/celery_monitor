#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/1/10 上午9:47
# @Author  : chenyuelong
# @Mail    : yuelong_chen@yahoo.com
# @File    : utils.py
# @Software: PyCharm

from __future__ import absolute_import, unicode_literals
import time
import subprocess
import argparse
import random
import string
import re
import pandas as pd
import matplotlib
import configparser
import os

matplotlib.use('Agg')
from chardet import detect
import seaborn as sns


def gtwArgs():
    '''
    go-to-work脚本提交
    :return: args
    '''
    parser = argparse.ArgumentParser(prog='go to work',
                                     description=
                                     '''
                                     基于celery的分布式脚本提交命令，功能尽量模仿SGE\n
                                     目前为测试版本：0.0.0    \n                                
                                     慢慢增加功能\n                                    
                                     --“完成比完美更重要”---     \n                              
                                     '''
                                     )
    parser.add_argument('-s', '--script', dest='script', type=str, required=True, action='store',
                        help=
                        '''
                        需要执行的脚本，shell脚本（required）
                        ''')
    parser.add_argument('-p', '--prefix', dest='prefix', type=str, required=True, action='store',
                        help=
                        '''
                        输出文件的prefix，例如 ~/tmp 输出则会是 ~/tmp.xxx
                        输出主要指log文件及性能统计文件（required）
                        ''')
    parser.add_argument('-t', '--tmp', dest='tmp', type=str, action='store',
                        help=
                        '''
                        tmp目录，e.g. /tmp/(option)
                        ''', default='/tmp/')
    args = parser.parse_args()
    if not os.path.exists(args.script):
        raise FileNotFoundError('脚本必须存在，最好检查一下是否为绝对路径')

    return args


def getConfig(config):
    cf = configparser.RawConfigParser()
    cf.read(config)
    return cf


def getFileSize(file):
    '''
    计算文件大小，具体用处暂时未定
    :param file: 文件名
    :return: 文件大小（数字），单位（b,Kb,Mb,Gb,Tb）
    '''
    fsize = os.path.getsize(file)
    unit = ['b', 'Kb', 'Mb', 'Gb', 'Tb']
    unitN = 0
    while fsize >= 1024 and unitN < 4:
        unitN += 1
        fsize /= 1024
    return round(fsize, 2), unit[unitN]


def writefile(context, file):
    '''
    写入文件
    :param context:写入内容
    :param file: 写入文件的文件名
    :return:文件大小，单位
    '''
    mkdirs(file)
    with open(file, 'a+') as fbuffer:
        fbuffer.write(str(context))
    fsize, unit = getFileSize(file)
    return fsize, unit


def mkdirs(file):
    '''
    方法中任意一个文件（生成），都会检查目录是否存在，不论是否存在都建立目录
    :param file:任意文件
    :return:True
    '''
    try:
        filepath = os.path.dirname(os.path.abspath(file))
        os.makedirs(filepath, mode=0o755, exist_ok=True)
        return True
    except Exception as err:
        raise ('目录建立错误：mkdirs(file)')


def Popen(cmd):
    '''
    只负责运行命令
    :param cmd:需要运行的命令
    :return:subprocess.Popen结果
    '''
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return p


def randomFileName(cache):
    '''
    生成随机20位长度的文件名，例如：KG9skf8s9fd0s0dfg.tmp
    :param cache: 所有生成的文件名都需要记录，最终进行统计及删除
    :return:文件名
    '''
    rf = '{}.tmp'.format(''.join(random.sample(string.ascii_letters + string.digits, 20)))
    cache[rf] = 1
    return rf, cache


def getpids(pid):
    '''
    由于有的程序会调用多进程，或者程序间的调用，会形成不同的子进程。这是一个利用pstree查找
    所有该进程相关子进程的方法
    :param pid: pid 父进程pid
    :return: pidlist 父进程及父进程所有子进程 pid
    '''
    p = Popen(getchildPidCmd(pid))
    stdout, _ = mntcmd(p)
    pidlist = pattern4pid(stdout)
    return pidlist


def pattern4pid(pidstr):
    '''
    通过pstree返回值，利用正则表达式找出所有pid
    :param pidstr:pstree返回结果
    :return: pidlist
    '''
    pattern = re.compile('\(([\d]+)\)')
    # print(pidstr)
    pidlist = pattern.findall(pidstr)
    return pidlist


def getchildPidCmd(pid):
    '''
    pstree cmd
    :param pid:
    :return: cmd
    '''
    cmd = 'pstree -p {}'.format(pid)
    return cmd


def rmcache(cache):
    cmd = 'rm {}'.format(' '.join(cache.keys()))
    # print(cmd)
    return mntcmd(Popen(cmd))


def getstatCmd(pid):
    '''
    生成pidstat命令
    :param pid: pid
    :return: cmd
    '''
    cmd = 'pidstat -urd -h -p {} 1 1'.format(pid)
    return cmd


def plotResult(file, outdir):
    '''
    以统计文件及图的形式输出结果
    :param file: pidstat统计结果文件（完成后会进行删除）
    :param outdir: 统计结果输出目录
    :return: 无
    '''

    data = pd.read_table(file, sep='\s+', skip_blank_lines=True, comment='#')
    # print(data.size)
    if data.size >= 2:
        data.columns = ['Time', 'UID', 'PID', 'pusr', 'psystem', 'pguest', 'pCPU', 'CPU', 'minflt/s',
                        'majflt/s', 'VSZ', 'RSS', '%MEM', 'kB_rd/s', 'kB_wr/s', 'kB_ccwr/s', 'Command']
        data['Time'] = data['Time'] - min(data['Time'])
        data['VSZ'] = data['VSZ'] / 1000000
        data['RSS'] = data['RSS'] / 1000000
        data.groupby('Command').describe().to_csv('{}.summary.csv'.format(outdir))
        # print(data)
        sns_plot = sns.pairplot(data, x_vars=["RSS", "VSZ"], y_vars=['Time'],
                                hue='Command', size=10)
        sns_plot.savefig("{}.Time_VSZ_RSS.pdf".format(outdir), dpi=300)
        p = Popen('rm {}'.format(file))
        mntcmd(p)


def mntcmd(sPopen):
    '''
    监控subprocess.Popen运行
    :param sPopen:subprocess.Popen实例
    :return:标准输出，标准错误
    '''
    stdout, stderr = sPopen.communicate()
    # print(type(stdout),stdout)
    # print(type(stderr),stderr)
    codetype = 'utf8'
    if stdout != None and detect(stdout)['encoding'] != None:

        codetype = detect(stdout)['encoding']

        stdout = stdout.decode(codetype)
    else:
        stdout = stdout.decode()
    if stderr != None and detect(stderr)['encoding'] != None:
        codetype = detect(stderr)['encoding']
        stderr = stderr.decode(codetype)
    else:
        stderr = stderr.decode()

    return stdout, stderr


def memory_stat(popen, pid, cache, tmp='/tmp/'):
    '''
    pidstat进行进程统计，并将结果输出到tmp目录中
    :param pid: pid
    :param cache: 文件名dict
    :param tmp: tmp目录
    :return: file,主程序标准输出，主程序标准错误，cache
    '''
    rf, cache = randomFileName(cache)
    file = '{}/{}'.format(tmp, rf)
    pidlist = getpids(pid)
    rstdout, rstderr = 0, 0
    while (len(pidlist) > 0):
        for cpid in pidlist:
            cmd = getstatCmd(cpid)
            p = Popen(cmd)
            stdout, _ = mntcmd(p)
            with open(file, 'a+') as f:
                f.write('#stdout:{}'.format(stdout))
        if popen.poll() != None:
            rstdout, rstderr = mntcmd(popen)
        else:
            time.sleep(10)
        pidlist = getpids(pid)
    return file, rstdout, rstderr, cache


def main():
    pass


if __name__ == '__main__':
    main()
