# -*- coding: utf-8 -*-

import io
from setuptools import setup, find_packages
from collections import OrderedDict

version = "0.0.2"

readme = ''
with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='torstack',
    version=version,
    description='A full stack framework base on tornado.',
    long_description=readme,
    url='https://github.com/longniao/torstack',
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/longniao/torstack/tree/master/docs'),
        ('Issue tracker', 'https://github.com/longniao/torstack/issues'),
    )),
    author='Longniao',
    author_email='longniao@gmail.com',
    license='MIT',
    zip_safe=False,
    platforms='any',
    python_requires='>=3.5',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'redis',
        'sqlalchemy',
        'pyconvert',
    ])
