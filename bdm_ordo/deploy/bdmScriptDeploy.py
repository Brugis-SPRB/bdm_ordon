# -*- coding: latin_1 -*-
# Python script for Urbanalysis transfer of DB and templates to staging

import ftplib
import os
import socket
from datetime import datetime
import  sys
import platform
from distutils.tests.test_install_scripts import InstallScriptsTestCase

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from shared.printAndLog import printAndLog
import shared.databrugisconf as DBRUC
import zipfile

################################################################################
def zipdir(path, ziph):
	# Iterate all the directories and files
	for root, dirs, files in os.walk(path):
		# Create a prefix variable with the folder structure inside the path folder. 
		# So if a file is at the path directory will be at the root directory of the zip file
		# so the prefix will be empty. If the file belongs to a containing folder of path folder 
		# then the prefix will be that folder.
		if root.replace(path,'') == '':
			prefix = ''
		else:
			# Keep the folder structure after the path folder, append a '/' at the end 
			# and remome the first character, if it is a '/' in order to have a path like 
			# folder1/folder2/file.txt
			prefix = root.replace(path, '') + '/'
			if (prefix[0] == '/'):
				prefix = prefix[1:]
		for filename in files:
			actual_file_path = root + '/' + filename
			zipped_file_path = prefix + filename
			zipf.write( actual_file_path, zipped_file_path)

def doLog(myLine, myFile):
	print myLine
	if myLine is None:
		myFile.write("{}\n".format(datetime.today()) )
	else:
		myFile.write("{} : {}\n".format(datetime.today(),myLine) )

if __name__ == "__main__":
	nodename =  platform.node()
	path_to_zip_file = os.pardir
	
	
	logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
	with open(os.path.join(os.path.dirname(__file__), logFileName), 'a') as logFile:
		doLog('Startup deploy BDM Scripts ', logFile)
		
		zipfilename = os.path.join(os.path.dirname(__file__),'bdmscripts.zip')
		zipf = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
		zipdir(os.path.join(os.path.dirname(__file__), os.pardir), zipf)
		zipf.close()
		
		
		try:
			f = ftplib.FTP(DBRUC._ftpHOST, DBRUC._ftpLOGIN, DBRUC._ftpPASWD)
		except (socket.error, socket.gaierror), e:
			printAndLog('ERROR: cannot reach "%s"' % DBRUC._ftpHOST, logFile)
		else:
			printAndLog('*** Connected to host "%s"' % DBRUC._ftpHOST, logFile)

			ROOT = f.pwd()
			###############################
			# deploy
			
			
			try:
				filename= 'bdmscripts.zip'
				srcInstallScript = os.path.join(os.path.dirname(__file__),'/deploy/bdmScriptsInstall.py')
				localFile = zipfilename
				
				if os.path.exists(localFile):
					f.cwd(DBRUC._dirDiff)
					f.storbinary('STOR %s' % filename, open(localFile, 'rb'))
					srcConf = os.path.join(os.path.dirname(__file__),'/ordonnancement/localConf_diff.py')
					f.storbinary('STOR %s' % 'localConf.py', open(srcConf, 'rb'))
					f.storbinary('STOR %s' % 'bdmScriptInstall.py', open(srcInstallScript, 'rb'))						
					f.cwd(DBRUC._dirStaging)
					f.storbinary('STOR %s' % filename, open(localFile, 'rb'))
					srcConf = os.path.join(os.path.dirname(__file__),'/ordonnancement/localConf_staging.py')						
					f.storbinary('STOR %s' % 'localConf.py', open(srcConf, 'rb'))						
					f.storbinary('STOR %s' % 'bdmScriptInstall.py', open(srcInstallScript, 'rb'))	
					f.cwd(ROOT)
			
			except ftplib.error_perm:
				printAndLog('FTP permission error', logFile)
				
			f.quit()
		
		if os.path.exists(zipfilename):
			os.remove(zipfilename)
					
			






