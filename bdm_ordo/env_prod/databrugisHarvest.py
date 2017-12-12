# -*- coding: latin_1 -*-
# Python script for BruGIS Harvesting

import os
import datetime
import socket
import platform
import  sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from  shared.sendmail import send_mail
from   shared.printAndLog import printAndLog
import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF

################################################################################
socket.setdefaulttimeout(120)



if __name__ == "__main__":
    wfstepId = OCONF.getWorkflowID() 
    OCONF.tokenFileWriteRunning(wfstepId)
    # check for dbname
    
    dbname = DBRUC._db_dbname
    
    #check for schemaname
    schemas = DBRUC._prod_toharvest_schemas
    logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
    try:
        with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
            printAndLog( "{} running".format(wfstepId),logFile)
            printAndLog("Startup harvest.", logFile)
            nodename =  platform.node()
            for sch in schemas:
                filename= "{}{}".format(dbname, sch)
                printAndLog("Export schema %s." % sch, logFile)
                
                fullpath = os.path.join(DBRUC._dbexportpath, filename)
                if os.path.exists(fullpath):
                    printAndLog("Cleaning %s of %s" % (DBRUC._dbexportpath, filename), logFile)
                    os.remove(fullpath)
                
                cmd = "pg_dump --host {} --port 5432 --username {} --no-password  --format custom --blobs --encoding UTF8 --schema {} --file {}".format( 
                    DBRUC._prod_db_host,
                    DBRUC._db_userdump,
                    sch,
                    fullpath)
                printAndLog("Execute command %s" % cmd, logFile)                                                                                                                                          
                os.system(cmd)
            printAndLog( "{} done".format(wfstepId),logFile)            
            if DBRUC._sendMail:
                send_mail('%s - %s - log - %s' % (nodename,os.path.basename(__file__), str(datetime.datetime.today())), logFile.read())
        OCONF.tokenFileWriteDone(wfstepId)        
    except:
        OCONF.tokenFileWriteFail(wfstepId)       