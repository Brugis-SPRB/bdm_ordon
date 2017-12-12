# -*- coding: latin_1 -*-
# Python script for BruGIS Harvesting

import os
import socket
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


import shared.ordoconf as OCONF
from shared.printAndLog import printAndLog



################################################################################
socket.setdefaulttimeout(120)





################################################################################
if __name__ == "__main__":
    prs = sys.argv[1:]
    prs2 = sys.argv[1:]
    
    print "params {}".format(prs)
    
    ctx = OCONF.getContextID()
    wfstepId = OCONF.getWorkflowID()
    
    print "wfstepId {}".format(wfstepId)
    print "ctx {}".format(ctx)