from setuptools import setup

setup(
    name='celery_monitor',
    version='v0.0.0.1_alpha_20180323',
    packages=['tests', 'monitor', 'monitor.utils', 'monitor.monitorTasks'],
    url='',
    license='',
    author='yuelong.chen',
    author_email='yuelong.chen@oumeng.com.cn',
    description='celery_monitor',
    scripts=['bin/gtw.py'],
)
