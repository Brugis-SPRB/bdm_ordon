# -*- coding: latin_1 -*-
# Python script for Urbanalysis transfer of DB and templates to staging

import os
import datetime
import shared.sendmail as sendmail

import shared.databrugisconf as DBRUC
import shared.ordoconf as OCONF
import ConfigParser
import platform

################################################################################

					
def sendMailTo( logfolder, recipient):
	messagecontent = ""
	if len(recipient) < 1:
		return 
	lrecipient = recipient.split(';')
	for subdir, dirs, files in os.walk(logfolder):
		for fname in files:
			filepath = subdir + os.sep + fname
			with open(filepath, 'r') as logFile:
				messagecontent += '----- %s --------\r\n' % fname
				messagecontent += logFile.read()
				messagecontent += '\r\n'
			os.remove(filepath)
	
	if len(messagecontent) < 1:
		return 
	nodename =  platform.node()
	sendmail.send_mail_ext('%s - %s - log - %s' % (nodename,os.path.basename(__file__), str(datetime.datetime.today())), messagecontent,lrecipient)
	


if __name__ == "__main__":
	wfstepId = OCONF.getWorkflowID() 
	configFile = "mailconfig.properties"
	section = "mailtarget"
	config = ConfigParser.ConfigParser()
	config.read(os.path.join(DBRUC._mailDir, configFile))

	mailA40 = config.get(section, 'A40')
	mailA60 = config.get(section, 'A60')
	mailBRUGIS = config.get(section, 'BRUGIS')
	mailURBIS = config.get(section, 'URBIS')
	mailF10 = config.get(section, 'F10')
	
	sendMailTo( os.path.join(DBRUC._mailDir, 'a40'), mailA40 )
	sendMailTo( os.path.join(DBRUC._mailDir, 'a60'), mailA60 )
	sendMailTo( os.path.join(DBRUC._mailDir, 'f10'), mailF10 )
	sendMailTo( os.path.join(DBRUC._mailDir, 'brugis'), mailBRUGIS )
	sendMailTo( os.path.join(DBRUC._mailDir, 'urbis'), mailURBIS )
	
	
