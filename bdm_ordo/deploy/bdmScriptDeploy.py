# -*- coding: latin_1 -*-
# Deployement of bdm scripts (to be launched from developper WS), overiding of dummy config parameters is included

import ftplib
import os
import socket
from datetime import datetime
import  sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

sys.path.append("C:/scripts/custom")

from shared.printAndLog import printAndLog
import databrugisconf as DBRUC
import zipfile
import pysftp
import paramiko


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
	path_to_zip_file = os.pardir
	
	
	custom_config_dir = "C:/scripts/custom/"
	
	
	logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.now().strftime('%d_%m_%Y'))
	with open(os.path.join(os.path.dirname(__file__), logFileName), 'a') as logFile:
		doLog('Startup deploy BDM Scripts ', logFile)
		
		zipfilename = os.path.join(os.path.dirname(__file__),'bdmscripts.zip')
		zipf = zipfile.ZipFile(zipfilename, 'w', zipfile.ZIP_DEFLATED)
		zipdir(os.path.join(os.path.dirname(__file__), os.pardir), zipf)
		zipf.close()
		
		
		try:
			f = ftplib.FTP(DBRUC._ftpHOST, DBRUC._ftpLOGIN, DBRUC._ftpPASWD)
		except (socket.error, socket.gaierror), e:
			printAndLog('ERROR: cannot reach {}'.format(DBRUC._ftpHOST), logFile)
		else:
			printAndLog('*** Connected to host {}'.format(DBRUC._ftpHOST), logFile)

			ROOT = f.pwd()
			###############################
			# deploy
			
			try:
				filename= 'bdmscripts.zip'
				srcInstallScript = os.path.join(os.path.dirname(__file__),'bdmScriptInstall.py')
				srcdataconfig = os.path.join(custom_config_dir,'databrugisconf.py')
				srcordoconfig = os.path.join(custom_config_dir,'ordoconf.py')
				##############################
				# force remote install
				srcrinstall = os.path.join(custom_config_dir,'rinstall')
				
				localFile = zipfilename
				
				pardir = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))				
				ordodir = os.path.join(pardir,'ordonnancement')
				
				
				if os.path.exists(localFile):
					f.cwd(DBRUC._dirDiff)
					f.storbinary('STOR {}'.format(filename), open(localFile, 'rb'))
					srcConf = os.path.join(ordodir,'localConf_diff.py')
					f.storbinary('STOR {}'.format('localConf.py'), open(srcConf, 'rb'))
					f.storbinary('STOR {}'.format('bdmScriptInstall.py'), open(srcInstallScript, 'rb'))						
					f.storbinary('STOR {}'.format('databrugisconf.py'), open(srcdataconfig, 'rb'))
					f.storbinary('STOR {}'.format('ordoconf.py'), open(srcordoconfig, 'rb'))
					f.storbinary('STOR {}'.format('rinstall'), open(srcrinstall, 'rb'))
					
					
		
					
					f.cwd(DBRUC._dirStaging)
					f.storbinary('STOR {}'.format(filename), open(localFile, 'rb'))
					srcConf = os.path.join(ordodir,'localConf_staging.py')						
					f.storbinary('STOR {}'.format('localConf.py'), open(srcConf, 'rb'))						
					f.storbinary('STOR {}'.format('bdmScriptInstall.py'), open(srcInstallScript, 'rb'))	
					f.storbinary('STOR {}'.format('databrugisconf.py'), open(srcdataconfig, 'rb'))
					f.storbinary('STOR {}'.format('ordoconf.py'), open(srcordoconfig, 'rb'))
					f.storbinary('STOR {}'.format('rinstall'), open(srcrinstall, 'rb'))
					
					
					


					cnopts = pysftp.CnOpts()
					cnopts.hostkeys = None

					sftp = pysftp.Connection(DBRUC._sftpHOST, username=DBRUC._sftpLOGIN, password=DBRUC._sftpPASWD, cnopts=cnopts)
					with sftp.cd(DBRUC._sftpROOT):
						sftp.put(localFile)
						srcConf = os.path.join(ordodir,'localConf_prod.py')
						sftp.put(srcConf)
						try:
							sftp.remove('localConf.py')
						except:
							pass						
						sftp.rename('localConf_prod.py', 'localConf.py')
						sftp.put(srcInstallScript)	
						sftp.put(srcdataconfig)
						sftp.put(srcordoconfig)
						try:
							sftp.put(srcrinstall)
						except:
							pass
						
					
					
					f.cwd(ROOT)
					doLog('Scripts deployed', logFile)
			except ftplib.error_perm:
				printAndLog('FTP permission error', logFile)
				
			f.quit()
		
		if os.path.exists(zipfilename):
			os.remove(zipfilename)
			doLog('Zip file removed', logFile)
		doLog('Done', logFile)
					
			






