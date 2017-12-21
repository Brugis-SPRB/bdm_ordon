# -*- coding: latin_1 -*-
# Python script for Urbanalysis transfer of DB and templates to staging

import os
import sys
import traceback
import platform
import shutil
from crontab import CronTab
import psutil
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import zipfile

################################################################################

def doLog(myLine, myFile):
	print (myLine)
	if myLine is None:
		myFile.write("{}\n".format(datetime.today()) )
	else:
		myFile.write("{} : {}\n".format(datetime.today(),myLine) )

if __name__ == "__main__":
	##running script
	ordorunning = False
	nodename =  platform.node()
	## Copy zip and localConf from ftp directory
	
	src_zipfilename = os.path.join(os.path.expanduser("~"),'ftp_root/databrugis_transfer/bdmscripts.zip')
	dest_zipfilename = os.path.join(os.path.expanduser("~"),'bdmscripts.zip')
	
	
	script_dir = os.path.join(os.path.expanduser("~"),'bdmscripts') 
	
	
				
	## Unzip the file if exist
	
	logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.now().strftime('%d_%m_%Y'))
	with open(os.path.join(os.path.dirname(__file__), logFileName), 'a') as logFile:
		try:
			doLog('Startup install BDM Scripts ', logFile)
			try:
				os.stat(src_zipfilename)
			except:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)

			if os.path.exists(src_zipfilename):
				doLog('Zip exist', logFile)
				
				## Remove ORDO related CRON
				cron = CronTab(True)
				lstJobs = cron.remove_all(comment='Bdm Ordo Process')
				doLog('Cron entry removed', logFile)
			
				## Check no more bdmscript are running
				for pid in psutil.pids():
					p = psutil.Process(pid)
					if 'ordonnancement' in p.cmdline():
						doLog('Process to kill', logFile)
						p.kill()
				
				## remove old zip
				if os.path.exists(dest_zipfilename):
					os.remove(dest_zipfilename)
				
				## remove old directory ... and recreate it
				if os.path.exists(script_dir):
					shutil.rmtree(script_dir)
				os.mkdir(script_dir)
				
				## Copy files to installation directory
				shutil.move(src_zipfilename,dest_zipfilename)
				doLog('Zip file moved', logFile)
				
				## decompress new installation
				zipf = zipfile.ZipFile(dest_zipfilename, 'r', zipfile.ZIP_DEFLATED)
				zipf.extractall(path=script_dir)
				zipf.close
				doLog('Zip file extract done', logFile)
	
				## copy custom localConf.py at the right place
				src_localConf = os.path.join(os.path.dirname(__file__),'localConf.py')
				dest_localConf = os.path.join(script_dir,'ordonnancement/localConf.py')
				dest_OrdoDir = os.path.join(script_dir,'ordonnancement/')
				shutil.move(src_localConf,dest_localConf)
				
				
				## copy restricted config at the right place
				##     ordoconf
				src_ordoConf = os.path.join(os.path.dirname(__file__),'ordoconf.py')
				dest_ordoConf = os.path.join(script_dir,'shared/ordoconf.py')
				shutil.move(src_ordoConf,dest_ordoConf)
				
				##     databrugisconf
				src_databrugisConf = os.path.join(os.path.dirname(__file__),'databrugisconf.py')
				dest_databrugisConf = os.path.join(script_dir,'shared/databrugisconf.py')
				shutil.move(src_databrugisConf,dest_databrugisConf)
				
				
				
				
				doLog('Conf file moved', logFile)
				
				if os.path.exists(dest_zipfilename):
					os.remove(dest_zipfilename)
				if os.path.exists(src_zipfilename):
					os.remove(src_zipfilename)
				doLog('Zip file removed', logFile)
		
				## Add ORDO RELATED CRON
				job = cron.new(command='~/bdm_env/bin/python  ./bdmscripts/ordonnancement/startup.py >> ./bdmscripts/startup.log 2>&1',comment='Bdm Ordo Process')			
				job.hour.on(21)
				job2 = cron.new(command='~/bdm_env/bin/python  ./bdmscripts/ordonnancement/localOrdo.py >> ./bdmscripts/localOrdo.log 2>&1',comment='Bdm Ordo Process')			
				job2.minute.every(5)
				
				## Post master scheduled only for prod
				## retrieve config 
				sys.path.append(dest_OrdoDir)
				import localConf
				## add cron
				if localConf._envName == "PROD":
					doLog('Add postmaster Cron', logFile)
					job3 = cron.new(command='~/bdm_env/bin/python  ./bdmscripts/ordonnancement/postMaster.py >> ./bdmscripts/postMaster.log 2>&1',comment='Bdm Ordo Process')			
					job3.minute.every(6)
				else:
					doLog('Not PROD', logFile)
					
				
				doLog('Job added', logFile)
	
				
				cron.write_to_user()	
				doLog('CronTab write done', logFile)
			else:
				doLog('{} not found'.format(src_zipfilename), logFile)
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)






