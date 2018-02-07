# -*- coding: latin_1 -*-

import os
import sys, getopt
from os.path import expanduser
from datetime import datetime
from datetime import timedelta


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

def getExecMode():
    md = "undefined"
    for t in sys.argv[1:]:
        if "mode" in t:
            md= t.split("=")[1]
    return md   

def getDebugLevel():
    dlevel = "undefined"
    for t in sys.argv[1:]:
        if "d" in t:
            dlevel= t.split("=")[1]
    return dlevel  

def tokenFileWriteRunning(step):
    tokenfile = open(_tokenFileName,'w+')
    tokenfile.write("{},running".format(step))
    tokenfile.close()

def tokenFileWriteDone(step):
    tokenfile = open(_tokenFileName,'w+')
    tokenfile.write("{},done".format(step))
    tokenfile.close()
    
def tokenFileWrite(filename,status,step):
    tokenfile = open(filename,'w+')
    tokenfile.write("{},{}".format(step,status))
    tokenfile.close()

def tokenFileWriteFail(step):
    tokenfile = open(_tokenFileName,'w+')
    tokenfile.write("{},fail".format(step))
    tokenfile.close()
    
def keepAliveFileWrite(filename,pid,reset):
    kfile = open(filename,'w+')
    if reset:
        kfile.write(" ")
    else:
        kfile.write("{},{}".format(datetime.now().strftime("%y-%m-%d-%H-%M"),pid))
    kfile.close()
    
def stateFileWrite(filename,state):
    kfile = open(filename,'w+')
    kfile.write("{}".format(state.trim_whitespace()))
    kfile.close()
    
def parseKeepAlive(filename):
    try:
        tokenfile = open(filename)
        tokencontent = tokenfile.read()
        parts = tokencontent.split(',')
        startTime = datetime.strptime(parts[0], '%y-%m-%d-%H-%M')
        startpid = parts[1]
        if (startTime + _processMaxDuration) < datetime.datetime.now():
            return startpid
        return -1
    except Exception:
        return -1
    

home = expanduser("~")

_dbexportpath                = os.path.join(expanduser("~"),"XXX/XXX/")

_mailDir                     = os.path.join(_dbexportpath, "mail/XXX/")
_ordopath                    = os.path.join(expanduser("~"),"XXX/XXX/XXX/")
_tokenFileName               = os.path.join(_ordopath,'token.txt')
_keepAliveFileName           = os.path.join(_ordopath,'keepalive.txt')
_processMaxDuration          = timedelta(minutes=40)





_dirDiff                      = '/XXX/XXX/'
_dirStaging                   = '/XXX/XXX/'
_dirProd                      = '/XXX/XXX/'



_ftpHOST = 'XXX'
_ftpLOGIN = 'XXX'
_ftpPASWD = 'XXX'

_sendMail = False