ZMySQLDA: Zope Mysql adatper product.

Egg packages should be available from http://pypi.python.org/pypi

Note that ./Products/ZMySQLDA is a sym-link to the ZMySQLDA as per the setup in
the SVN repository. So make sure you have it as well if you with to build your
own egg packages.

To create egg package run something along the lines of:

$ python setup.py egg_info -RDb "" sdist bdist_egg


See setuptool documentation for more.

http://peak.telecommunity.com/DevCenter/setuptools#making-official-non-snapshot-releases

