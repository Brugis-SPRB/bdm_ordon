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

def prepareMessage(myLine):
    with open(os.path.join(OCONF._ordopath, "ordo.msg"), 'a') as notifyFile:
        print (myLine)
        if myLine is None:
            notifyFile.write("{}\n".format(datetime.datetime.now()) )
        else:
            notifyFile.write("{} : {}\n".format(datetime.datetime.now(),myLine) )

if __name__ == "__main__":
    wfstepId = OCONF.getWorkflowID() 
    mode = OCONF.getExecMode()
    dlevel = OCONF.getDebugLevel()
    OCONF.tokenFileWriteRunning(wfstepId)
    logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
    with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
        try:
            dbName = DBRUC._db_dbname
            printAndLog( "{} running".format(wfstepId),logFile)
            printAndLog("Startup queryFDW", logFile)
            
            conn_s = "dbname='{}' user='{}' host='{}' password='{}'".format(dbName,
                                                                             DBRUC._db_user,
                                                                             DBRUC._prod_db_host,
                                                                             DBRUC._db_password)
            
            if dlevel == 'V':
                printAndLog("Connection string {}".format(conn_s), logFile)
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
            else:
                conn = psycopg2.connect(conn_s)
                
                if dlevel == 'V':
                    printAndLog("After connect", logFile)
                      
                cur = conn.cursor()
                cur.execute("SELECT commonbrugis.wf_intextintra_1synchro()")
                
                rows = cur.fetchall()
                for row in rows:
                    msg = row[0]
                    print(msg)
                    if len(msg) > 10:
                        prepareMessage("DB Error {}".format(msg))
                
                conn.commit()
    
                printAndLog( "{} done".format(wfstepId),logFile)
            OCONF.tokenFileWriteDone(wfstepId)    
        except:
            printAndLog( "failure {}".format(sys.exc_info()[0]),logFile)
            OCONF.tokenFileWriteFail(wfstepId)
    
    
