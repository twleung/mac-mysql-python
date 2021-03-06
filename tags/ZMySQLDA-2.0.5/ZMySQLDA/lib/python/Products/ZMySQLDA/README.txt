Z MySQL DA

  This is the Z MySQL database adapter product for the 
  Z Object Publishing Environment.
  
  ***** NOTE *****

  Note that the Z MySQL database adapter is compatible with MySQL
  versions 3.22 and later (including MySQL 3.23).
  
  ***** IMPORTANT *****
  
  This product is distributed as a NON-BINARY release!
  
  This product requires compiled Python extensions that are
  NOT included as a binary with this release. You must build
  or install the required extensions using the instructions 
  below before the product will work properly!
    
  Installation

    The Z MySQL database adapter uses the MySQLdb package.  
    This must be installed before you can use the Z MySQL DA.

    Instructions on building the extension modules are given in the
    the README.txt file in the source directory.

  Connection Strings
  
    The connection string used for Z MySQL Database Connection
    are of the form::

       database[@host[:port]] [user [password [unix_socket]]]

    or typically just::

       database user password

    to use the default server.
