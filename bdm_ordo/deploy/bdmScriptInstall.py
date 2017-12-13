# -*- coding: latin_1 -*-
# Python script for Urbanalysis transfer of DB and templates to staging

import os
import  sys
import platform
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import zipfile

################################################################################


if __name__ == "__main__":
	nodename =  platform.node()
	## Copy zip and localConf from ftp directory
	src_zipfilename = os.path.join('~/ftp_root/databrugis_transfer/bdmscripts.zip')
	## Unzip the file if exist
	if os.path.exists(src_zipfilename):
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
					
			






