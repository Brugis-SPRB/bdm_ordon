import psycopg2
import os
import datetime
import platform
import  sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from shared.sendmail import send_mail

# -*- coding: latin_1 -*-

from shared.printAndLog import printAndLog

import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF

################################################################################

if __name__ == "__main__":
    wfstepId = OCONF.getWorkflowID()
    dlevel = OCONF.getDebugLevel()
    mode = OCONF.getExecMode()
    OCONF.tokenFileWriteRunning(wfstepId)
    try:
        logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
        with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
            printAndLog( "{} running".format(wfstepId),logFile)
            dbName = DBRUC._db_dbname
            printAndLog("Startup restore diffusion schemas", logFile)
            
            conn_s = "dbname='{}' user='{}' host='{}' password='{}'".format(dbName,
                                                                             DBRUC._db_user,
                                                                             DBRUC._prod_db_host,
                                                                             DBRUC._db_password)
            
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
            else:
                conn = psycopg2.connect(conn_s)
                cur = conn.cursor()
                
                # Check that all expected files are present
                for schem in DBRUC._diff_torestore_schemas:            
                    filename = '{}{}.backup'.format(DBRUC._db_dbname, schem)
                    fullpath = os.path.join(DBRUC._backuppath, filename)
                    if not os.path.exists(fullpath):
                        printAndLog("Missing backup file {}".format(filename), logFile)
                        raise Exception('Missing file')   
                
                
                for schem in DBRUC._diff_torestore_schemas:            
                    cur.execute("DROP SCHEMA if exists {} CASCADE".format(schem))
                    conn.commit()
                conn.close()
                
                for schem in DBRUC._diff_torestore_schemas:            
                    filename = '{}{}.backup'.format(dbName, schem)
                    logfilename = '{}{}.log'.format(dbName, schem)
                    fullpath = os.path.join(DBRUC._backuppath, filename)
                    cmd = "pg_restore --host {} --port 5432 --username {} --no-password  -d databrugis --verbose  {}  > {}".format(
                        DBRUC._prod_db_host,
                        DBRUC._db_userdump,
                        fullpath,
                        logfilename)
                    if dlevel == 'V':
                        printAndLog(cmd, logFile)
                    os.system(cmd)    
                conn2 = psycopg2.connect(conn_s)
                cur2 = conn2.cursor()
                if dlevel == 'V':
                    printAndLog("Before wf_intextinter_2integration", logFile)
                cur2.execute("SELECT commonbrugis.wf_intextinter_2integration()")
                if dlevel == 'V':
                    printAndLog("Before synchro_publish_tables", logFile)
                cur2.execute("select commonbrugis.synchro_publish_tables()")
                conn2.commit()
    
                printAndLog( "{} done".format(wfstepId),logFile)
            OCONF.tokenFileWriteDone(wfstepId)    
    except:
        OCONF.tokenFileWriteFail(wfstepId)
    

    
