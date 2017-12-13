# -*- coding: latin_1 -*-
# Python script for Urbanalysis transfer of DB and templates to staging

import ftplib
import os
import socket
import datetime
import  sys
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
	nodename =  platform.node()
	
	dbname = DBRUC._db_dbname
	logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
	try:
		with open(os.path.join(DBRUC._mailDir, logFileName), 'a') as logFile:
			printAndLog( "{} running".format(wfstepId),logFile)
			printAndLog('Startup dispatch ', logFile)
			if mode == "EMUL":
				printAndLog("EMULATION MODE", logFile)
				OCONF.tokenFileWriteDone(wfstepId)
				exit()
			try:
				f = ftplib.FTP(DBRUC._ftpHOST, DBRUC._ftpLOGIN, DBRUC._ftpPASWD)
			except (socket.error, socket.gaierror), e:
				printAndLog('ERROR: cannot reach "%s"' % DBRUC._ftpHOST, logFile)
			else:
				printAndLog('*** Connected to host "%s"' % DBRUC._ftpHOST, logFile)
	
				ROOT = f.pwd()
				###############################
				# dispatch to diff
				schemanames = DBRUC._diff_torestore_schemas
				dirn = DBRUC._dirDiff
				
				try:
					f.cwd(dirn)
				except ftplib.error_perm:
					printAndLog('ERROR: cannot CD to "%s"' % dirn, logFile)
					f.quit()
				else:
					printAndLog('*** Changed to "%s" folder' % dirn, logFile)
					for schem in schemanames:
						filename= "{}{}.backup".format(DBRUC._db_dbname, schem)
						localFile = os.path.join(DBRUC._dbexportpath, filename)
					
						if os.path.exists(localFile):
							try:
								f.storbinary('STOR %s' % filename, open(localFile, 'rb'))
							except:
								printAndLog('ERROR: cannot upload file "%s on %s"' % (filename, dirn), logFile)
							else:
								printAndLog('*** Uploaded "%s" to %s' % (filename, dirn), logFile)
						else:
							printAndLog('%s is not present, no dispatching' % localFile, logFile)
					f.cwd(ROOT)
				
				###############################
				# dispatch to staging
				schemanames = DBRUC._staging_torestore_schemas
				dirn = DBRUC._dirStaging
				
				try:
					f.cwd(dirn)
				except ftplib.error_perm:
					printAndLog('ERROR: cannot CD to "%s"' % dirn, logFile)
					f.quit()
				else:
					printAndLog('*** Changed to "%s" folder' % dirn, logFile)
					for schem in schemanames:
						filename= "{}{}.backup".format(DBRUC._db_dbname, schem)
						localFile = os.path.join(DBRUC._dbexportpath, filename)
					
						if os.path.exists(localFile):
							try:
								f.storbinary('STOR %s' % filename, open(localFile, 'rb'))
							except:
								printAndLog('ERROR: cannot upload file "%s on %s"' % (filename, dirn), logFile)
							else:
								printAndLog('*** Uploaded "%s" to %s' % (filename, dirn), logFile)
						else:
							printAndLog('%s is not present, no dispatching' % localFile, logFile)
					f.cwd(ROOT)
				
				f.quit()
	
			try:
				for schem in schemanames:
					filename= "{}{}.backup".format(DBRUC._db_dbname, schem)
					if dlevel == 'V':
						printAndLog("Remove if exist {}".format(filename), logFile)
					localFile = os.path.join(DBRUC._dbexportpath, filename)
					if os.path.exists(localFile):
						os.remove(localFile)
						printAndLog('%s removed' % localFile, logFile)
			except:
				printAndLog('An error occurs when removing backup files', logFile)
			else:
				printAndLog('All backup files are removed', logFile)
			printAndLog( "{} done".format(wfstepId),logFile)
			if DBRUC._sendMail:
				send_mail('%s - %s - log - %s' % (nodename,os.path.basename(__file__), str(datetime.datetime.today())), logFile.read())
		OCONF.tokenFileWriteDone(wfstepId)
	except:
		OCONF.tokenFileWriteFail(wfstepId)
			
