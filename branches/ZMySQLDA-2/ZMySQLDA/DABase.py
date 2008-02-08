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
__doc__='''Database Connection

$Id$'''
__version__='$Revision$'[11:-2]

import Shared.DC.ZRDB.Connection, sys
from Globals import HTMLFile
from ExtensionClass import Base
import Acquisition

class Connection(Shared.DC.ZRDB.Connection.Connection):
    _isAnSQLConnection=1

    manage_options=Shared.DC.ZRDB.Connection.Connection.manage_options+(
        {'label': 'Browse', 'action':'manage_browse'},
        )

    manage_browse=HTMLFile('browse',globals())

    info=None
        
    def tpValues(self):
        r=[]
        try:
            c = self._v_database_connection
        except AttributeError:
            self.connect(self.connection_string)
            c = self._v_database_connection
        for d in c.tables(rdb=0):
            try:
                name = d['table_name']
                b = TableBrowser()
                b.__name__ = name
                b._d = d
                b._c = c
                b.icon = table_icons.get(d['table_type'],'text')
                r.append(b)
            except:
                pass
        return r


class Browser(Base):
    def __getattr__(self, name):
        try: return self._d[name]
        except KeyError: raise AttributeError, name

class values:

    def len(self): return 1

    def __getitem__(self, i):
        try: return self._d[i]
        except AttributeError: pass
        self._d = self._f()
        return self._d[i]

class TableBrowser(Browser, Acquisition.Implicit):
    icon='what'
    description=check=''
    info=HTMLFile('table_info',globals())

    def tpValues(self):
        v=values()
        v._f=self.tpValues_
        return v

    def tpValues_(self):
        r=[]
        tname=self.__name__
        for d in self._c.columns(tname):
            b=ColumnBrowser()
            b._d=d
            b.icon=d['icon']
            b.table_name=tname
            r.append(b)
        return r
            
    def tpId(self): return self._d['table_name']
    def tpURL(self): return "Table/%s" % self._d['table_name']
    def name(self): return self._d['table_name']
    def type(self): return self._d['table_type']

class ColumnBrowser(Browser):
    icon='field'

    def check(self):
        return ('\t<input type=checkbox name="%s.%s">' %
                (self.table_name, self._d['name']))
    def tpId(self): return self._d['name']
    def tpURL(self): return "Column/%s" % self._d['name']
    def description(self): return " %s" % self._d['description']

table_icons={
    'table': 'table',
    'view':'view',
    'system_table': 'stable',
    }

