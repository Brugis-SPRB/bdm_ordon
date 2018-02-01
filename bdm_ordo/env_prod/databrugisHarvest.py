# -*- coding: latin_1 -*-
# Bdm Harvesting in PROD

import os
import datetime
import socket
import  sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from   shared.printAndLog import printAndLog
import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF

################################################################################
socket.setdefaulttimeout(120)



if __name__ == "__main__":
    wfstepId = OCONF.getWorkflowID() 
    dlevel = OCONF.getDebugLevel()
    OCONF.tokenFileWriteRunning(wfstepId)
    mode = OCONF.getExecMode()
    # check for dbname
    
    dbname = DBRUC._db_dbname
    
    #check for schemaname
    schemas = DBRUC._prod_toharvest_schemas
    logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
    try:
        with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
            printAndLog( "{} running".format(wfstepId),logFile)
            printAndLog("Startup harvest.", logFile)
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
            else:
                for sch in schemas:
                    filename= "{}{}.backup".format(dbname, sch)
                    printAndLog("Export schema {}.".format(sch), logFile)
                    
                    fullpath = os.path.join(DBRUC._dbexportpath, filename)
                    if os.path.exists(fullpath):
                        printAndLog("Cleaning {} of {}".format(DBRUC._dbexportpath, filename), logFile)
                        os.remove(fullpath)
                    
                    cmd = "pg_dump --host {} --port 5432 --username {} --no-password  --format custom --blobs --encoding UTF8 --schema {} --file {}".format( 
                        DBRUC._prod_db_host,
                        DBRUC._db_userdump,
                        sch,
                        fullpath)
                    if dlevel == 'V':
                        printAndLog("Execute command {}".format(cmd), logFile)                                                                                                                                          
                    os.system(cmd)
                printAndLog( "{} done".format(wfstepId),logFile)            
        OCONF.tokenFileWriteDone(wfstepId)        
    except:
        OCONF.tokenFileWriteFail(wfstepId)       