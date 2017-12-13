# -*- coding: latin_1 -*-
import os
from os.path import expanduser


_dbexportpath                = os.path.join(expanduser("~"),"ftp_root/xxx/")
_backuppath                  = os.path.join(expanduser("~"),"ftp_root/xxx/")   

_mailDir                     = os.path.join(_dbexportpath, "mail/brugis/")


_diff_torestore_schemas      = ["xxx", "xxx", "xxx", "xxx"]
_staging_torestore_schemas   = ["xxx", "xxx", "xxx", "xxx", "xxx"]

_diff_toharvest_schemas      = ["xxx","xxx", "xxx","xxx"]
_prod_toharvest_schemas      = ["xxx", "xxx", "xxx", "xxx"]

_prod_todownload_schemas     = ["xxx","xxx", "xxx","xxx"]
_staging_todownload_schemas  = ["xxx"]



_dirDiff                      = ['/xxx/xxx/']
_dirStaging                   = ['/xxx/xxx/']
_dirProd                      = ['/xxx/xxx/']


_allschemasdown               = ["xxx","xxx"]
_alldumpsdown                 = ["xxx.backup","xxx.backup"]


_fileinter                    = 'xxx'
_fileexterninter              = 'xxx'


_stagingserver                = 'xxx'
_prodserver                   = 'xxx'
                                 
                                
_prod_db_host                  = 'xxx'
_diff_db_host                  = 'xxx'
_staging_db_host               = 'xxx'

_db_user                       = 'xxx'
_db_userdump                   = 'xxx'
_db_password                   = 'xxx'
_db_dbname                     = 'xxx'

_ftpHOST = 'xxx'
_ftpLOGIN = 'xxx'
_ftpPASWD = 'xxx'

_sendMail = False