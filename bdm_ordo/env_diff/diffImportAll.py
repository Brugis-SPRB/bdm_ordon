# -*- coding: latin_1 -*-
# restore external DB Schemas on diff

import datetime
import os

import psycopg2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF
from shared.printAndLog import printAndLog

################################################################################


if __name__ == "__main__":
    wfstepId = OCONF.getWorkflowID()
    dlevel = OCONF.getDebugLevel()
    mode = OCONF.getExecMode()
    OCONF.tokenFileWriteRunning(wfstepId)
    
    try:
        logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
        with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
            printAndLog("Startup restore diffusion schemas", logFile)
            conn_s = "dbname='{}' user='{}' host='{}' password='{}'".format(DBRUC._db_dbname,
                                                                             DBRUC._db_user,
                                                                             DBRUC._diff_db_host,
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
                    if dlevel == 'V':
                        printAndLog("Before DROP SCHEMA", logFile)
                        
                    cur.execute("DROP SCHEMA if exists {} CASCADE".format(schem))
                    conn.commit()
                conn.close()
                
                for schem in DBRUC._diff_torestore_schemas:			
                    filename = '{}{}.backup'.format(DBRUC._db_dbname, schem)
                    logfilename = '{}{}.log'.format(DBRUC._db_dbname, schem)
                    
                    fullpath = os.path.join(DBRUC._backuppath, filename)
                    try:
                        cmd1 = "pg_restore --host {} --port 5432 --username {} --no-password  -d databrugis --verbose  {}  > {}".format(
                            DBRUC._diff_db_host,
                            DBRUC._db_userdump,
                            fullpath,
                            logfilename)    
                        os.system(cmd1)	
                        printAndLog(cmd1, logFile)
                    except:
                        printAndLog("failure restoring {}".format(fullpath), logFile)
    
    
                printAndLog( "{} done".format(wfstepId),logFile)
            OCONF.tokenFileWriteDone(wfstepId)    
    except:
        OCONF.tokenFileWriteFail(wfstepId)
    
    
