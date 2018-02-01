# -*- coding: latin_1 -*-
# Bdm Downloads in Prod

import ftplib
import os
import socket
import datetime
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from shared.printAndLog import printAndLog
import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF

################################################################################


if __name__ == "__main__":
	wfstepId = OCONF.getWorkflowID()
	dlevel = OCONF.getDebugLevel()
	mode = OCONF.getExecMode()
	OCONF.tokenFileWriteRunning(wfstepId)
	logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
	try:
		with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
			printAndLog( "{} running".format(wfstepId),logFile)
			printAndLog('Startup ftp download', logFile)		
			if mode == "EMUL":
				printAndLog("EMULATION MODE", logFile)
			else:
				try:
					f = ftplib.FTP(DBRUC._ftpHOST, DBRUC._ftpLOGIN, DBRUC._ftpPASWD)
				except (socket.error, socket.gaierror), e:
					printAndLog('ERROR: cannot reach {} '.format(DBRUC._ftpHOST), logFile)
				else:
					printAndLog('*** Connected to host {} '.format(DBRUC._ftpHOST), logFile)
					ROOT = f.pwd()
		
					#########################################
					# Copy to prod
					dirn = DBRUC._dirDiff
					localDirn = DBRUC._backuppath 
					#localDirn = DBRUC._dirProd 
					schemas = DBRUC._prod_todownload_schemas
					try:
						f.cwd(dirn)
					except ftplib.error_perm:
						printAndLog('ERROR: cannot CD to  {} '.format(dirn), logFile)
						f.quit()
					else:
						printAndLog('*** Changed to {} folder'.format(dirn), logFile)
						for schem in schemas:
							filename = "{}{}.backup".format(DBRUC._db_dbname, schem)
							
							printAndLog('Download file {} '.format(filename) , logFile)
							localFile = os.path.join(localDirn, filename)
							printAndLog('Local file {}'.format(localFile), logFile)
							if os.path.exists(localFile):
								print ("remove local file")
								os.remove(localFile)
							try:
								print ("before open {}".format(localFile))
								with open(localFile, "wb") as gFile:
									print ("retrieve {}".format(filename))
									f.retrbinary('RETR {}'.format(filename) , gFile.write)
							except Exception:
								print ("Exception")
								printAndLog ("Exception {}".format(sys.exc_info()[0]))
						f.cwd(ROOT)
					f.quit()
		
				printAndLog( "{} done".format(wfstepId),logFile)
		OCONF.tokenFileWriteDone(wfstepId)		
	except:
		OCONF.tokenFileWriteFail(wfstepId)   		
