# -*- coding: latin_1 -*-

import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


import shared.ordoconf as OCONF
from shared.printAndLog import printAndLog

if __name__ == '__main__':
    logFileName = os.path.basename(__file__).replace('py', 'log')
    logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
    
    with open(os.path.join(OCONF._ordopath, logFileName), 'w') as logFile:
        try:
            printAndLog("Exec Startup", logFile)
            ################
            ## Just ask transfer
            tokenfile = open(OCONF._tokenFileName,'w')
            tokenfile.write("STARTUP,transit")
            tokenfile.close()
            
            printAndLog("Startup Done", logFile)
        except:
            pass