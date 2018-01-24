# -*- coding: latin_1 -*-
# Python script for downloads

import ftplib
import os
import socket
import datetime
import sys
import platform

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from shared.sendmail import send_mail
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
			nodename = platform.node()
			if mode == "EMUL":
				printAndLog("EMULATION MODE", logFile)
			else:
				try:
					f = ftplib.FTP(DBRUC._ftpHOST, DBRUC._ftpLOGIN, DBRUC._ftpPASWD)
				except (socket.error, socket.gaierror), e:
					printAndLog('ERROR: cannot reach "%s"' % DBRUC._ftpHOST, logFile)
				else:
					printAndLog('*** Connected to host "%s"' % DBRUC._ftpHOST, logFile)
					ROOT = f.pwd()
		
					#########################################
					# Copy to prod
					dirn = DBRUC._dirDiff
					localDirn = DBRUC._dirProd 
					schemas = DBRUC._prod_todownload_schemas
					try:
						f.cwd(dirn)
					except ftplib.error_perm:
						printAndLog('ERROR: cannot CD to "%s"' % dirn, logFile)
						f.quit()
					else:
						printAndLog('*** Changed to "%s" folder' % dirn, logFile)
						for schem in schemas:
							filename = "{}{}.backup".format(DBRUC._db_dbname, schem)
							
							printAndLog('Download file "%s"' % filename, logFile)
							localFile = os.path.join(localDirn, filename)
							printAndLog('Local file "%s"' % localFile, logFile)
							if os.path.exists(localFile):
								os.remove(localFile)
							try:
								with open(localFile, "wb") as gFile:
									f.retrbinary('RETR %s' % filename , gFile.write)
							except Exception:
								print "Exception"
						f.cwd(ROOT)
					f.quit()
		
				printAndLog( "{} done".format(wfstepId),logFile)
		OCONF.tokenFileWriteDone(wfstepId)		
	except:
		OCONF.tokenFileWriteFail(wfstepId)   		
