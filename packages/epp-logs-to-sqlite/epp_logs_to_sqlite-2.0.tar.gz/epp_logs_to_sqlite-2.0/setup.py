# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='epp_logs_to_sqlite',
    version='2.0',
    description='A tool to parse Eggplant Performance test logs into a SQLite database',
    packages=find_packages(),
    install_requires=[
        'epp_event_log_reader>=2.0,<3.0',
    ],
)
