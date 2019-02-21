# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
from collections import OrderedDict

version = "0.0.8"

readme = ''
with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='torstack',
    version=version,
    description='Torstack is a bundle for Tornado. it is designed to make getting started quick and easy, so you can focus on writing your app without needing to reinvent the wheel.',
    long_description=readme,
    url='https://github.com/longniao/torstack',
    keywords='tornado torstack',
    author='Longniao',
    author_email='longniao@gmail.com',
    maintainer='Longniao',
    maintainer_email='longniao@gmail.com',
    license='MIT',
    zip_safe=False,
    platforms='any',
    python_requires='>=3.5',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'tornado',
        'redis',
        'aioredis',
        'aiomysql',
        'sqlalchemy',
        'pymysql',
        'motor',
        'pyconvert',
        'apscheduler',
        'elasticsearch',
        'elasticsearch_async',
        'python-memcached',
        'aiofiles',
        'psycopg2',
    ])
