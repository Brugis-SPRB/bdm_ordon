# -*- coding: latin_1 -*-
# Python script for BruGIS Harvesting

import datetime
import os
import platform
import socket
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF
from shared.printAndLog import printAndLog
from shared.sendmail import send_mail


################################################################################
socket.setdefaulttimeout(120)





################################################################################
if __name__ == "__main__":
    wfstepId = OCONF.getWorkflowID()
    dlevel = OCONF.getDebugLevel()
    mode = OCONF.getExecMode()
    OCONF.tokenFileWriteRunning(wfstepId)
    # check for dbname
    dbname = DBRUC._db_dbname
    # check for schemaname
    schemas = DBRUC._diff_toharvest_schemas
    logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
    try:
        with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
            printAndLog( "{} running".format(wfstepId),logFile)
            printAndLog("Startup harvest.", logFile)
            nodename = platform.node()
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
                OCONF.tokenFileWriteDone(wfstepId) 
                exit()
            for sch in schemas:
                filename = "{}{}".format(dbname, sch)            
                printAndLog("Export schema %s." % sch, logFile)
                
                fullpath = os.path.join(DBRUC._dbexportpath, filename)
                if os.path.exists(fullpath):
                    if dlevel == 'V':
                        printAndLog("Cleaning %s of %s" % (DBRUC._dbexportpath, filename), logFile)
                    os.remove(fullpath)
                
                
                cmd1 = "pg_dump --host {} --port 5432 --username {} --no-password  --format custom --blobs --encoding UTF8 --schema {} --file {}".format(
                    DBRUC._diff_db_host,
                    DBRUC._db_userdump,
                    sch,
                    fullpath)
                printAndLog("Execute command %s" % cmd1, logFile)
                os.system(cmd1)
            printAndLog( "{} done".format(wfstepId),logFile)            
            if DBRUC._sendMail:
                send_mail('%s - %s - log - %s' % (nodename, os.path.basename(__file__), str(datetime.datetime.today())), logFile.read())
        OCONF.tokenFileWriteDone(wfstepId)    
    except:
        OCONF.tokenFileWriteFail(wfstepId)        