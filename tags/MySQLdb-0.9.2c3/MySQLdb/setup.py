#!/usr/bin/env python

"""Setup script for the MySQLdb module distribution."""

import os, sys
from distutils.core import setup
from distutils.extension import Extension
import string

YES = 1
NO = 0

# set this to YES if you have the thread-safe mysqlclient library
thread_safe_library = YES

# You probably don't have to do anything past this point. If you
# do, please mail me the configuration for your platform. Don't
# forget to include the value of sys.platform and os.name.

name = "MySQL-%s" % os.path.basename(sys.executable)
version = "0.9.2c3"

mysqlclient = thread_safe_library and "mysqlclient_r" or "mysqlclient"

# include files and library locations should cover most platforms
include_dirs = [
    '/usr/include/mysql', '/usr/local/include/mysql',
    '/usr/local/mysql/include/mysql'
    ]
library_dirs = [
    '/usr/lib/mysql', '/usr/local/lib/mysql',
    '/usr/local/mysql/lib/mysql'
    ]

# MySQL-3.23 and newer need libz
libraries = [mysqlclient, "z"]

# On some platorms, this can be used to find the shared libraries
# at runtime, if they are in a non-standard location. Doesn't
# work for Linux gcc.
runtime_library_dirs = []

# This can be used to force linking against static libraries.
extra_objects = []

# Sometimes the compiler or linker needs an extra switch to make
# things work.
extra_compile_args = []
extra_link_args = []

if sys.platform == "netbsd1":
    include_dirs = ['/usr/pkg/include/mysql']
    library_dirs = ['/usr/pkg/lib/mysql']
elif sys.platform in ("freebsd4", "openbsd3"):
    LOCALBASE = os.environ.get('LOCALBASE', '/usr/local')
    include_dirs = ['%s/include/mysql' % LOCALBASE]
    library_dirs = ['%s/lib/mysql' % LOCALBASE]
elif sys.platform == "sunos5": # Solaris 2.8 + gcc
    runtime_library_dirs.append('/usr/local/lib:/usr/openwin/lib:/usr/dt/lib') 
    extra_compile_args.append("-fPIC")
elif sys.platform == "win32": # Ugh
    include_dirs = [r'c:\mysql\include']
    library_dirs = [r'c:\mysql\lib\opt']
    libraries = [mysqlclient, 'zlib', 'msvcrt', 'libcmt',
                 'wsock32', 'advapi32']
    extra_objects = [r'c:\mysql\lib\opt\mysqlclient.lib']
elif sys.platform == "cygwin":
    include_dirs = ['/c/mysql/include']
    library_dirs = ['/c/mysql/lib']
    extra_compile_args.append('-DMS_WIN32')
elif sys.platform[:6] == "darwin": # Mac OS X
    include_dirs.append('/sw/include')
    library_dirs.append('/sw/lib')
    extra_link_args.append('-flat_namespace')
elif sys.platform == 'linux2' and os.environ.get('HOSTTYPE') == 'alpha':
    libraries.extend(['ots', 'cpml'])
elif os.name == "posix": # UNIX-ish platforms not covered above
    pass # default should work
else:
    raise "UnknownPlatform", "sys.platform=%s, os.name=%s" % \
          (sys.platform, os.name)
    
long_description = \
"""Python interface to MySQL-3.23

MySQLdb is an interface to the popular MySQL database server for Python.
The design goals are:

-     Compliance with Python database API version 2.0 
-     Thread-safety 
-     Thread-friendliness (threads will not block each other) 
-     Compatibility with MySQL-3.23 and later

This module should be mostly compatible with an older interface
written by Joe Skinner and others. However, the older version is
a) not thread-friendly, b) written for MySQL 3.21, c) apparently
not actively maintained. No code from that version is used in
MySQLdb. MySQLdb is free software.

"""

setup (# Distribution meta-data
        name = name,
        version = version,
        description = "An interface to MySQL",
        long_description=long_description,
        author = "Andy Dustman",
        author_email = "andy@dustman.net",
        license = "GPL",
        platforms = "ALL",
        url = "http://sourceforge.net/projects/mysql-python",

        # Description of the modules and packages in the distribution

        py_modules = ["CompatMysqldb",
                      "_mysql_exceptions",
                      "MySQLdb.converters",
                      "MySQLdb.connections",
                      "MySQLdb.cursors",
                      "MySQLdb.sets",
                      "MySQLdb.times",
                      "MySQLdb.constants.CR",
                      "MySQLdb.constants.FIELD_TYPE",
                      "MySQLdb.constants.ER",
                      "MySQLdb.constants.FLAG",
                      "MySQLdb.constants.REFRESH",
                      "MySQLdb.constants.CLIENT",
                     ],

        ext_modules = [Extension(
                name='_mysql',
                sources=['_mysql.c'],
                include_dirs=include_dirs,
                library_dirs=library_dirs,
                runtime_library_dirs=runtime_library_dirs,
                libraries=libraries,
                extra_objects=extra_objects,
                extra_link_args=extra_link_args,
                extra_compile_args=extra_compile_args,
                )],
)
