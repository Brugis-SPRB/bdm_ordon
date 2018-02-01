# -*- coding: latin_1 -*-
# Bdm diff Harvesting

import datetime
import os
import platform
import socket
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF
from shared.printAndLog import printAndLog


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
    with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
        try:
            printAndLog( "{} running".format(wfstepId),logFile)
            printAndLog("Startup harvest.", logFile)
            nodename = platform.node()
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
            else:
                for sch in schemas:
                    filename = "{}{}.backup".format(dbname, sch)            
                    printAndLog("Export schema {}".format(sch), logFile)
                    
                    fullpath = os.path.join(DBRUC._dbexportpath, filename)
                    if os.path.exists(fullpath):
                        if dlevel == 'V':
                            printAndLog("Cleaning {} of {}".format(DBRUC._dbexportpath, filename), logFile)
                        os.remove(fullpath)
                    
                    
                    cmd1 = "pg_dump --host {} --port 5432 --username {} --no-password  --format custom --blobs --encoding UTF8 --schema {} --file {}".format(
                        DBRUC._diff_db_host,
                        DBRUC._db_userdump,
                        sch,
                        fullpath)
                    printAndLog("Execute command {}".format(cmd1), logFile)
                    os.system(cmd1)
                printAndLog( "{} done".format(wfstepId),logFile)            
            OCONF.tokenFileWriteDone(wfstepId)    
            printAndLog( "write is done",logFile) 
        except:
            printAndLog( "failure {}".format(sys.exc_info()[0]),logFile)
            OCONF.tokenFileWriteFail(wfstepId)   
            printAndLog( "write failure",logFile)     