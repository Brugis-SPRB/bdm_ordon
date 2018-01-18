# -*- coding: latin_1 -*-

import psycopg2
import os
import datetime
import platform
import  sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from shared.sendmail import send_mail
from shared.printAndLog import printAndLog

import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF

################################################################################

if __name__ == "__main__":
    wfstepId = OCONF.getWorkflowID()
    mode = OCONF.getExecMode()
    dlevel = OCONF.getDebugLevel()
    OCONF.tokenFileWriteRunning(wfstepId)
    try:
        logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
        with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
            dbName = DBRUC._db_dbname
            printAndLog("Startup diffusion query FDW", logFile)
            
            conn_s = "dbname='{}' user='{}' host='{}' password='{}'".format(DBRUC._db_dbname,
                                                                             DBRUC._db_user,
                                                                             DBRUC._diff_db_host,
                                                                             DBRUC._db_password)
            
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
                printAndLog("exit", logFile)                
            else:
                conn = psycopg2.connect(conn_s)
                if dlevel == 'V':
                    printAndLog("Before wf_intextinter_1synchro", logFile)    
                    cur = conn.cursor()
                    cur.execute("SELECT commonbrugis.wf_intextinter_1synchro()")
                    conn.commit()

                printAndLog( "{} done".format(wfstepId),logFile)
                if DBRUC._sendMail:
                    nodename = platform.node()
                    send_mail('%s - %s - log - %s' % (nodename, os.path.basename(__file__), str(datetime.datetime.today())), logFile.read())
        OCONF.tokenFileWriteDone(wfstepId)        
    except:
        pass
        OCONF.tokenFileWriteFail(wfstepId)
    
    
