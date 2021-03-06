# -*- coding: utf-8 -*-
# local management of state machine : determine the step to execute, launch step related script, when required ask broadcast to Postmaster

import os
import sys
import datetime
import signal
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from shared.printAndLog import printAndLog
import shared.ordoconf as OCONF
import localConf as LCONF
import globalConf as GCONF






import csv



################################################################################

def prepareMessage(myLine):
    with open(os.path.join(OCONF._ordopath, "ordo.msg"), 'a') as notifyFile:
        print (myLine)
        if myLine is None:
            notifyFile.write("{}\n".format(datetime.datetime.now()) )
        else:
            notifyFile.write("{} : {}\n".format(datetime.datetime.now(),myLine) )

def prepareStageChange(myLine):
    with open(os.path.join(OCONF._ordopath, "ordo.state"), 'w+') as stateFile:
        print (myLine)
        if myLine is None:
            stateFile.write("{}\n".format(datetime.datetime.now()) )
        else:
            stateFile.write("{} : {}\n".format(datetime.datetime.now(),myLine) )


if __name__ == "__main__":
    logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
    
    parentDir = os.path.join(os.path.dirname(__file__), os.pardir)
    print (parentDir)
    
    with open(os.path.join(OCONF._ordopath, logFileName), 'a') as logFile:
        printAndLog("Start Local Ordo on {}".format(LCONF._envName), logFile)
        
        csvpath = os.path.join(os.path.dirname(__file__),'globalordo.csv')        
        csvfile = open(csvpath)            
        tokencontent = OCONF.parseTokenFile(OCONF._tokenFileName)
            
        
        printAndLog("State is {} Step is {}".format(tokencontent['state'], tokencontent['step']), logFile)
                
        reader = csv.DictReader(csvfile)
        newstep = 'undefined'
        newstate = 'pending'
        
        ##############################################
        # Evaluation du next step sur base du step actif dans le fichier csv et de l'�tat actuel
        for row in reader:
            if row['STIN'] == tokencontent['step'] and row['SRVIN'] == LCONF._envName:                     
                printAndLog("Step found", logFile)
                if tokencontent['state'] == 'running':
                    printAndLog("State running stop local ordo", logFile)
                    startpid = OCONF.parseKeepAlive(OCONF._keepAliveFileName)
                    
                    if startpid < 0 :
                        #Times remains let the process doing the job 
                        exit(0)
                    else:
                        #Kill process 
                        os.kill(startpid, signal.SIG_DFL)
                        msg = "Kill process step {}".format(tokencontent['step'])
                        prepareMessage(msg)
                        
                        if row['SRVOUT'] != LCONF._envName:
                            newstate = 'transit'
                        else:
                            newstate = 'done'
                        newstep = row['STOUTNOK']
                    break
                    
                elif tokencontent['state'] == 'pending':
                    startpid = OCONF.parseKeepAlive(OCONF._keepAliveFileName)
                    
                    if startpid < 0 :
                        #Times remains let the process doing the job 
                        newstep = tokencontent['step']
                    else:
                        #Kill process 
                        os.kill(startpid, signal.SIG_DFL)
                        msg = "Kill process step {}".format(tokencontent['step'])
                        prepareMessage(msg)
                        
                        if row['SRVOUT'] != LCONF._envName:
                            newstate = 'transit'
                        else:
                            newstate = 'done'
                        newstep = row['STOUTNOK']
                    break
                elif tokencontent['state'] == 'done':
                    OCONF.keepAliveFileWrite(OCONF._keepAliveFileName,-1,True)
                    printAndLog("SRVOUT == {}".format(row['SRVOUT']), logFile)
                    if row['SRVOUT'] != LCONF._envName:
                        printAndLog("State is done transit required", logFile)
                        newstate = 'transit'
                    else:
                        printAndLog("State is done force pending", logFile)
                        newstate = 'pending'
                    newstep = row['STOUTOK']
                    printAndLog("new step  == {}".format(newstep), logFile)
                    if newstep == "END":
                        prepareStageChange("step is [END] no more script to process".format(newstep))
                    break
                elif tokencontent['state'] == 'fail':
                    msg = "Failure at step {}".format(tokencontent['step'])
                    prepareMessage(msg)
                    
                    if row['SRVOUT'] != LCONF._envName:
                        newstate = 'transit'
                    else:
                        newstate = 'pending'
                    newstep = row['STOUTNOK']
                    printAndLog("new step  == {}".format(newstep), logFile)
                    break            
            else:
                continue
            
        csvfile = open(csvpath)
        reader = csv.DictReader(csvfile)
        ###############################################
        # Recheche du next step dans le fichier csv
        for row in reader:
            ###########################
            ## On continue tant que le newstep n'apparait pas dans la configuration
            if row['STIN'] != newstep:
                continue
            ###########################
            ## Le script doit s'exécuter en local
            if row['SRVIN'] == LCONF._envName: 
                if newstep == "END":
                    prepareStageChange("step is [END] no more script to process".format(newstep))
                else:    
                    script = row['SCRIPT']
                    printAndLog("launch script {}".format(script), logFile)
                    
                    
                    OCONF.tokenFileWrite(OCONF._tokenFileName, newstate, newstep)
                    
                    
                    parentScriptDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))                
                    scriptpath = os.path.join(parentScriptDir, LCONF._envScript)
                    
                    pythonexec = sys.executable
                    
                    printAndLog("python runtime found", logFile)
                    #Run the script
                    
                    try:
                        printAndLog("Step {} Env {}".format(newstep, LCONF._envName), logFile)
                        
                        cmd = "{} {} -wf={} -ctx={} -mode={} -d={}".format(pythonexec, os.path.join(scriptpath,script),newstep,LCONF._envName,GCONF._executionMode,GCONF._debugLevel)
                    
                        printAndLog("Script is {}".format(cmd), logFile)
                        args = cmd.split()
                        p = subprocess.Popen(args)
                        
                        OCONF.keepAliveFileWrite(OCONF._keepAliveFileName,p.pid,False)
                        prepareStageChange("Script [{}] launched".format(newstep))
                        #subprocess.call(cmd)
                        #os.system(cmd)
                    except Exception:
                        printAndLog("Exception {}".format(sys.exc_info()[0]), logFile)
            
                    printAndLog("Script started", logFile)
                    
                break
            ###########################
            ## Le script doit s'exécuter sur un autre serveur
            else:
                printAndLog("Run {} on another server".format(newstate), logFile)
                OCONF.tokenFileWrite(OCONF._tokenFileName, newstate, newstep)
                
        ####
        # Voir comment g�rer le step final !!!!
        
        
