#!/usr/bin/python2.4
from setuptools import setup, find_packages

# See MANIFEST.in for filelist

setup(
    name="Products.ZMySQLDA",
    version="3.0",
    license="Zope Public License (ZPL) Version 1.0",
    author="John Eikenberry",
    author_email="jae@zhar.net",
    url="http://sourceforge.net/projects/mysql-python",
    description="MySQL Zope2 adapter.",
    long_description=("MySQL Database Adapter for Zope 2. Extensively "
        "reworked for stability and compatibility with versions 2.8+ and "
        "modern MySQL versions. New features from auto-creating database "
        "to limited Unicode support."),
    packages=find_packages(),
    include_package_data=True,
    namespace_packages=['Products'],
    zip_safe=False,
    install_requires = "MySQL-python >= 1.2.1",
    )

