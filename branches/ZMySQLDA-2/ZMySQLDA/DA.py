##############################################################################
# 
# Zope Public License (ZPL) Version 1.0
# -------------------------------------
# 
# Copyright (c) Digital Creations.  All rights reserved.
# 
# This license has been certified as Open Source(tm).
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions in source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 
# 3. Digital Creations requests that attribution be given to Zope
#    in any manner possible. Zope includes a "Powered by Zope"
#    button that is installed by default. While it is not a license
#    violation to remove this button, it is requested that the
#    attribution remain. A significant investment has been put
#    into Zope, and this effort will continue if the Zope community
#    continues to grow. This is one way to assure that growth.
# 
# 4. All advertising materials and documentation mentioning
#    features derived from or use of this software must display
#    the following acknowledgement:
# 
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
# 
#    In the event that the product being advertised includes an
#    intact Zope distribution (with copyright and license included)
#    then this clause is waived.
# 
# 5. Names associated with Zope or Digital Creations must not be used to
#    endorse or promote products derived from this software without
#    prior written permission from Digital Creations.
# 
# 6. Modified redistributions of any form whatsoever must retain
#    the following acknowledgment:
# 
#      "This product includes software developed by Digital Creations
#      for use in the Z Object Publishing Environment
#      (http://www.zope.org/)."
# 
#    Intact (re-)distributions of any official Zope release do not
#    require an external acknowledgement.
# 
# 7. Modifications are encouraged but must be packaged separately as
#    patches to official Zope releases.  Distributions that do not
#    clearly separate the patches from the original work must be clearly
#    labeled as unofficial distributions.  Modifications which do not
#    carry the name Zope may be packaged in any form, as long as they
#    conform to all of the clauses above.
# 
# 
# Disclaimer
# 
#   THIS SOFTWARE IS PROVIDED BY DIGITAL CREATIONS ``AS IS'' AND ANY
#   EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#   PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL CREATIONS OR ITS
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
#   USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#   ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
#   OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#   SUCH DAMAGE.
# 
# 
# This software consists of contributions made by Digital Creations and
# many individuals on behalf of Digital Creations.  Specific
# attributions are listed in the accompanying credits file.
# 
##############################################################################
database_type='MySQL'
__doc__='''%s Database Connection

$Id$''' % database_type
__version__='$Revision$'[11:-2]

import os
from db import DBPool, DB
from thread import allocate_lock

import DABase
from ImageFile import ImageFile
import Globals

manage_addZMySQLConnectionForm=Globals.HTMLFile('connectionAdd',globals())

def manage_addZMySQLConnection(self, id, title,
                                connection_string,
                                check=None,
                                use_unicode=False,
                                auto_create_db=False,
                                REQUEST=None):
    """Add a DB connection to a folder"""
    use_unicode = bool(use_unicode)
    auto_create_db = bool(auto_create_db)
    self._setObject(id,
            Connection(id, title, connection_string, check,
                use_unicode=use_unicode,
                auto_create_db=auto_create_db))
    if REQUEST is not None: return self.manage_main(self,REQUEST)

# Connection Pool for connections to MySQL.
# Maps one mysql client connection to one DA object instance.
database_connection_pool_lock = allocate_lock()
database_connection_pool = {}

# Combining connection pool with the DB pool gets you
# one DA/connection per connection with 1 DBPool with 1 DB/thread
# pool_id -> DA -> DBPool -> thread id -> DB
# dc_pool[pool_id] == DBPool_instance
# DBPool_instance[thread id] == DB instance

class Connection(DABase.Connection):
    """ ZMySQL Database Adapter Connection.
    """
    database_type=database_type
    id='%s_database_connection' % database_type
    meta_type=title='Z %s Database Connection' % database_type
    icon='misc_/Z%sDA/conn' % database_type

    auto_create_db = True
    use_unicode = False
    _v_connected = ''

    manage_properties=Globals.HTMLFile('connectionEdit', globals())

    def factory(self):
        """ Base API. Returns factory method for DB connections.
        """
        return DB
    
    def _pool_key(self):
        """ Return key used for DA pool.
        """
        return self.getPhysicalPath()

    def connect(self, s):
        """ Base API. Opens connection to mysql. Raises if problems.
        """
        database_connection_pool_lock.acquire()
        try:
            pool_key = self._pool_key()
            connection = database_connection_pool.get(pool_key)
            if connection is not None and connection.connection == s:
                self._v_database_connection = connection
                self._v_connected = connection.connected_timestamp
            else:
                if connection is not None:
                    connection.closeConnection()
                DB = self.factory()
                DB = DBPool(DB, create_db=self.auto_create_db)
                database_connection_pool[pool_key] = connection = DB(s)
                self._v_database_connection = connection
                connection.setUnicode(self.use_unicode)
                # XXX If date is used as such, it can be wrong because an 
                # existing connection may be reused. But this is suposedly
                # only used as a marker to know if connection was successfull.
                self._v_connected = connection.connected_timestamp
        finally:
            database_connection_pool_lock.release()
        return self
        
    def sql_quote__(self, v, escapes={}):
        """ Base API. Used to message strings for use in queries.
        """
        if self.use_unicode:
            return self._v_database_connection.unicode_literal(v)
        else:
            return self._v_database_connection.string_literal(v)

    def __init__(self, id, title, connection_string, check,
                    use_unicode=False,
                    auto_create_db=False):
        """ Instance setup. Optionally opens the connection (check arg).
        """
        self.use_unicode = bool(use_unicode)
        self.auto_create_db = bool(auto_create_db)
        return DABase.Connection.__init__(self, id, title, connection_string,
            check)

    def __setstate__(self,state):
        """ Skip super's __setstate__ as it connects which we don't want
            due to pool_key depending on acquisition.
        """
        Globals.Persistent.__setstate__(self, state)

    def manage_edit(self, title, connection_string,
                    check=None,
                    use_unicode=False,
                    auto_create_db=False):
        """ Zope management API.
        """
        self.use_unicode = bool(use_unicode)
        self.auto_create_db = bool(auto_create_db)
        return DABase.Connection.manage_edit(self, title, connection_string,
                    check=None)


classes=('DA.Connection',)

meta_types=(
    {'name':'Z %s Database Connection' % database_type,
     'action':'manage_addZ%sConnectionForm' % database_type,
     },
    )

folder_methods={
    'manage_addZMySQLConnection':
    manage_addZMySQLConnection,
    'manage_addZMySQLConnectionForm':
    manage_addZMySQLConnectionForm,
    }

__ac_permissions__=(
    ('Add Z MySQL Database Connections',
     ('manage_addZMySQLConnectionForm',
      'manage_addZMySQLConnection')),
    )

misc_={'conn': ImageFile(
    os.path.join('Shared','DC','ZRDB','www','DBAdapterFolder_icon.gif'))}

for icon in ('table', 'view', 'stable', 'what',
        'field', 'text','bin','int','float',
        'date','time','datetime'):
    misc_[icon]=ImageFile(os.path.join('icons','%s.gif') % icon, globals())

