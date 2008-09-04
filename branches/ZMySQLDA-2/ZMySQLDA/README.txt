Z MySQL DA

  This is the Z MySQL database adapter product for the 
  Z Object Publishing Environment (ZOPE) version 2.
  
  ** NOTE **

  Note that the Z MySQL database adapter is compatible with MySQL
  versions 3.22 and later (including MySQL 3.23, 4.0, 4.1 and 5.0).
  
  You need version 4.1 or higher for unicode support.

  ** IMPORTANT **
  
  This product is distributed as a NON-BINARY release!
  
  This product requires compiled Python extensions that are
  NOT included as a binary with this release. You must build
  or install the required extensions using the instructions 
  below before the product will work properly!
    
  Installation

    The Z MySQL database adapter uses the MySQLdb package.  
    This must be installed before you can use the Z MySQL DA.
    You can find this at::

        http://sourceforge.net/projects/mysql-python

    You need at least version 1.2.1; 1.2.2 is recommended. If you are
    compiling this yourself, you must use the same python executable
    as your Zope installation uses, otherwise Zope will not find it.

  Connection Strings
  
    The connection string used for Z MySQL Database Connection
    are of the form::

       database[@host[:port]] [user [password [unix_socket]]]

    or typically just::

       database user password

    to use the default server.
