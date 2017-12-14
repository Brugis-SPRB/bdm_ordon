# -*- coding: latin_1 -*-
# Python script for Urbanalysis transfer of DB and templates to staging

import os
import  sys
import platform
import shutil
from crontab import CronTab
import psutil

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import zipfile

################################################################################


if __name__ == "__main__":
	##running script
	ordorunning = False
	nodename =  platform.node()
	## Copy zip and localConf from ftp directory
	src_zipfilename = os.path.join('~/ftp_root/databrugis_transfer/bdmscripts.zip')
	## Unzip the file if exist
	if os.path.exists(src_zipfilename):
		## Remove ORDO related CRON
		lstJobs = CronTab.find_comment('Bdm Ordo Process').Remove()
		
		## Check no more bdmscript are running
		for pid in psutil.pids():
			p = psutil.Process(pid)
			if 'ordonnancement' in p.cmdline():
				p.kill()
		## Copy files to installation directory
		zipfilename = os.path.join('~/ftp_root/bdmscripts/bdmscripts.zip')
		shutil.move(src_zipfilename,zipfilename)
	
		zipf = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
		zipf.extractall()
		zipf.close
		## copy custom localConf.py at the right place
		src_localConf = os.path.join(os.path.dirname(__file__),'localConf.py')
		dest_localConf = os.path.join(os.path.dirname(__file__),'/ordonnancement/localConf.py')
		
		shutil.move(src_localConf,dest_localConf)
	
		if os.path.exists(zipfilename):
			os.remove(zipfilename)
			
		## Add ORDO RELATED CRON
		job = CronTab.new(command='./bdmscripts/bin/python  ./bdmscripts/synchro/ordonnancement/startup.py',comment='Bdm Ordo Process')			
		job.hour.on(21)
		job2 = CronTab.new(command='./bdmscripts/bin/python  ./bdmscripts/synchro/ordonnancement/localOrdo.py',comment='Bdm Ordo Process')			
		job2.minute.every(5)
		job3 = CronTab.new(command='./bdmscripts/bin/python  ./bdmscripts/synchro/ordonnancement/postMaster.py',comment='Bdm Ordo Process')			
		job3.minute.every(6)
		
		CronTab.write_to_user()	






