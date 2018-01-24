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
            printAndLog( "{} running".format(wfstepId),logFile)
            printAndLog("Startup restore staging schemas", logFile)
            if mode == "EMUL":
                printAndLog("EMULATION MODE", logFile)
            else:
        
                conn_s = "dbname='{}' user='{}' host='{}' password='{}'".format( DBRUC._db_dbname,
    																			 DBRUC._db_user, 
    																			 DBRUC._staging_db_host,
    																			 DBRUC._db_password)
                
                if dlevel == 'V':
                    printAndLog("Connection string {}".format(conn_s), logFile)
                conn = psycopg2.connect(conn_s)
                cur = conn.cursor()
                
                
                for schem in DBRUC._staging_torestore_schemas:            
                    filename = '{}{}.backup'.format(DBRUC._db_dbname,schem)
                    fullpath = os.path.join(DBRUC._backuppath, filename)
                    if not os.path.exists(fullpath):
                        printAndLog( "Missing backup file {}".format(filename),logFile)
                        raise Exception('Missing file')   
                
                for schem in DBRUC._staging_torestore_schemas:			
                    cur.execute("DROP SCHEMA if exists {} CASCADE".format(schem))
                    conn.commit()
                conn.close()
                
                for schem in DBRUC._staging_torestore_schemas:			
                    filename = '{}{}.backup'.format(DBRUC._db_dbname,schem)
                    sqllogfile = '{}{}.log'.format(DBRUC._db_dbname,schem)
                    fullpath = os.path.join(DBRUC._backuppath, filename)
                    cmd1 = "pg_restore --host {} --port 5432 --username {} --no-password  -d databrugis --verbose  {}  > {}".format(
                        DBRUC._staging_db_host,
                        DBRUC._db_userdump,
                        fullpath,
                        sqllogfile)
                    if dlevel == 'V':
                        printAndLog("Before Restore {}".format(cmd1), logFile)
                    os.system(cmd1)	
                    printAndLog( cmd1,logFile)
                
                if dlevel == 'V':
                    printAndLog("Before synchro_staging_tables()", logFile)
                conn2 = psycopg2.connect(conn_s)
                cur2 = conn2.cursor()
                cur2.execute("select commonbrugis.synchro_staging_tables()")
                conn2.commit()
                conn2.close()
                
                printAndLog( "{} done".format(wfstepId),logFile)
        OCONF.tokenFileWriteDone(wfstepId)    
    except:
        OCONF.tokenFileWriteFail(wfstepId)
    

    