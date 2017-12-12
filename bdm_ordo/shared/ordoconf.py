# -*- coding: latin_1 -*-

import os
import sys, getopt
from os.path import expanduser
#_dbexportpath                = "c:\\test"


def parseTokenFile(filename):
    try:
        tokenfile = open(filename)
        tokencontent = tokenfile.read()
        parts = tokencontent.split(',')
        return {'step':parts[0],'state':parts[1]}
    except Exception:
        return {'step':'undefined','state':'undefined'}

def getWorkflowID():
    wfid = "undefined"
    for t in sys.argv[1:]:
        if "wf" in t:
            wfid= t.split("=")[1]
    return wfid   
    
def getContextID():
    ctxid = "undefined"
    for t in sys.argv[1:]:
        if "ctx" in t:
            ctxid= t.split("=")[1]
    return ctxid   

def tokenFileWriteRunning(step):
    tokenfile = open(_tokenFileName,'w')
    tokenfile.write("{},running".format(step))
    tokenfile.close()

def tokenFileWriteDone(step):
    tokenfile = open(_tokenFileName,'w')
    tokenfile.write("{},done".format(step))
    tokenfile.close()
    
def tokenFileWrite(filename,status,step):
    tokenfile = open(filename,'w')
    tokenfile.write("{},{}".format(step,status))
    tokenfile.close()

def tokenFileWriteFail(filename,step):
    tokenfile = open(filename,'w')
    tokenfile.write("{},fail".format(step))
    tokenfile.close()
    

home = expanduser("~")

_dbexportpath                = os.path.join(expanduser("~"),"XXX/XXX/")

_mailDir                     = os.path.join(_dbexportpath, "mail/XXX/")
_ordopath                    = os.path.join(expanduser("~"),"XXX/XXX/XXX/")
_tokenFileName               = os.path.join(_ordopath,'token.txt')


_diff_torestore_schemas      = ["XXX", "XXX", "XXX", "XXX"]
_staging_torestore_schemas   = ["XXX", "XXX", "XXX", "XXX", "XXX"]

_diff_toharvest_schemas      = ["XXX","XXX", "XXX","XXX"]
_prod_toharvest_schemas      = ["XXX", "XXX", "XXX", "XXX"]

_prod_todownload_schemas     = ["XXX","XXX", "XXX","XXX"]
_staging_todownload_schemas  = ["XXX"]




_dirDiff                      = '/XXX/XXX/'
_dirStaging                   = '/XXX/XXX/'
_dirProd                      = '/XXX/XXX/'


_allschemasdown               = ["XXX","XXX"]
_alldumpsdown                 = ["XXX.backup","XXX.backup"]


_fileinter                    = 'XXX'
_fileexterninter              = 'XXX'


 
_stagingserver               = "XXX"
_prodserver                  = "XXX"
                                  
                                
_prod_db_host                  = 'XXX'
_diff_db_host                  = 'XXX'
_staging_db_host              = 'XXX'



_db_user                     = 'XXX'
_db_userdump                   = 'XXX'
_db_password                 = 'XXX'
_db_dbname                     = 'XXX'

_ftpHOST = 'XXX'
_ftpLOGIN = 'XXX'
_ftpPASWD = 'XXX'

_sendMail = False