# -*- coding: latin_1 -*-
# Drop brugis_publish schema
import datetime
import os
import sys
import psycopg2

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF
from shared.printAndLog import printAndLog
from shared.rollingFile import rollingFile


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
            printAndLog("Startup cleanup publish schemas", logFile)
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
            else:
                ##########################
                # Backup Publish
                filename = '{}{}.backup'.format(DBRUC._db_dbname, 'brugis_publish')
                fullpath = os.path.join(DBRUC._backuppath, filename)
                cmd1 = "pg_dump --host {} --port 5432 --username {} --no-password  --format custom --blobs --encoding UTF8 --schema {} --file {}".format(
                    DBRUC._diff_db_host,
                    DBRUC._db_userdump,
                    'brugis_publish',
                    fullpath)
                printAndLog("Dump {}".format(fullpath), logFile)
            
                
                os.system(cmd1)
                
                printAndLog("before rolling file", logFile)
            
                
                #rf = rollingFile()
                #rf.doRoll(DBRUC._dbexportpath, 'databrugisbrugis_publish', 'tdatabrugisbrugis_publish', 'backup', 8)
                
                printAndLog("after rolling file", logFile)
            
                
                conn_s = "dbname='{}' user='{}' host='{}' password='{}'".format(DBRUC._db_dbname,
                                                                                 DBRUC._db_user,
                                                                                 DBRUC._diff_db_host,
                                                                                 DBRUC._db_password)
                
                printAndLog("drop schema", logFile)
            
                ##########################
                # Recreate an empy schema
                conn = psycopg2.connect(conn_s)
                cur = conn.cursor()
                cur.execute("DROP SCHEMA if exists brugis_Publish CASCADE")
                cur.execute("CREATE SCHEMA brugis_publish AUTHORIZATION databrugis")
                conn.commit()
                conn.close()
                
                printAndLog( "{} done".format(wfstepId),logFile)
            OCONF.tokenFileWriteDone(wfstepId)
    except:
        OCONF.tokenFileWriteFail(wfstepId)
    
    
