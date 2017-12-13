# -*- coding: latin_1 -*-

import datetime
import os
import sys
import ftplib
from shutil import copyfile

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


import shared.ordoconf as OCONF
import shared.databrugisconf as DBRUC
from shared.printAndLog import printAndLog





################################################################################

def ftpDownload(ftpConn, localdir, remotedir, localfilename, distfilemename ):
    ftpConn.cwd(remotedir)
    localFile = os.path.join(localdir, localfilename)
    if os.path.exists(localFile):
        os.remove(localFile)                
    with open(localFile, "wb") as gFile:
        f.retrbinary('RETR {}'.format(distfilemename), gFile.write)


def parseTokenFile(filename):
    try:
        tokenfile = open(filename)
        tokencontent = tokenfile.read()
        parts = tokencontent.split(',')
        return {'step':parts[0],'state':parts[1]}
    except Exception:
        return {'step':'undefined','state':'undefined'}

if __name__ == "__main__":
    logFileName = "{}-{}.log".format(os.path.basename(__file__).replace('.py', ''),datetime.date.today().strftime('%d_%m_%Y'))
    with open(os.path.join(OCONF._ordopath, logFileName), 'a') as logFile:
        printAndLog("Start postMaster", logFile)
        
    
        ########################################
        # Retrieve all distributed TOKENS
        # Analyse content
        # 1° Check consitency (only one tokens replica should be done at the same time) 
        # 2° Check for notification request.. (transit)
        # 3° Broadcast the token 
       
        
        #########################################
        # set path
        dirndiff = "{}ordo/".format(OCONF._dirDiff)
        dirnstaging = "{}ordo/".format(OCONF._dirStaging)
        
        localDirn = "{}replica/".format(OCONF._ordopath) 
        
        ################################
        # Get all token replicas
        
          
        try:
            printAndLog("connect ftp", logFile)
            f = ftplib.FTP(DBRUC._ftpHOST, DBRUC._ftpLOGIN, DBRUC._ftpPASWD)
        
            ROOT = f.pwd()

            ########################################
            # copy diff and staging to local replica
            printAndLog("download diff ", logFile)
            ftpDownload(f, localDirn, dirndiff, "diff_token.txt", "token.txt" )    
            
            printAndLog("download staging", logFile)
            ftpDownload(f, localDirn, dirnstaging, "staging_token.txt", "token.txt" )
            
            f.close()
            f.cwd(ROOT)
            f.quit()
        except Exception, e:
            f.close()
            print "Exception {}"
        
        ########################################
        # copy prod to local replica        
        prodtokenfile = os.path.join(OCONF._ordopath,'token.txt')
        localFile = os.path.join(localDirn, "prod_token.txt")
        if os.path.exists(localFile):
            os.remove(localFile)
        try:
            copyfile(prodtokenfile, localFile)
        except Exception, e:
            print "Exception({}): {}".format(e.errno, e.strerror)
        
        
        
        ######################################
        # Parse TOKENS content
        
        printAndLog("Parse TOKENS content", logFile)
        
        difftoken = parseTokenFile(os.path.join(localDirn,'diff_token.txt'))
        stagingtoken = parseTokenFile(os.path.join(localDirn,'staging_token.txt'))
        prodtoken = parseTokenFile(os.path.join(localDirn,'prod_token.txt'))
        
        
        ######################################
        # consistency check >>> TODO
        
        ######################################
        # Check if any state == transit
        # if transit state doesnt exists... nothing to do 
        # if exist prepare token content
        
        printAndLog("check TOKENS content", logFile)
        
        tokentoprocess = None
        if difftoken["state"] == "transit":
            tokentoprocess = difftoken
        elif stagingtoken["state"] == "transit":
            tokentoprocess = stagingtoken
        elif prodtoken["state"] == "transit":
            tokentoprocess = prodtoken             
        
        if tokentoprocess == None:
            #########################
            # Nothing to do            
            printAndLog("Nothing to broadcast", logFile)
        
            exit(0)
        else:            
            tokencontent = "{},pending".format(tokentoprocess["step"])
        #####################################
        # Broadcast new TOKEN
        
        printAndLog("Broadcast new TOKEN", logFile)
        
        
        newtokenfileName = os.path.join(localDirn,'token.txt')
        newtokenfile = open(newtokenfileName,'w')
        newtokenfile.write(tokencontent)
        newtokenfile.close()
        
        printAndLog("Broadcast TOKEN [{}]".format(tokencontent), logFile)
        
        try:
            f = ftplib.FTP(DBRUC._ftpHOST, DBRUC._ftpLOGIN, DBRUC._ftpPASWD)
            ROOT = f.pwd()
            
            ########################################
            # copy to diff/staging/prod
            
            printAndLog("Push diff {}".format(dirndiff), logFile)
            
            f.cwd(dirndiff)
            f.storbinary('STOR token.txt', open(newtokenfileName, 'rb'))
            
            printAndLog("Push staging {}".format(dirnstaging), logFile)
            
            f.cwd(dirnstaging)
            f.storbinary('STOR token.txt', open(newtokenfileName, 'rb'))
            
            f.close()
            printAndLog("Remove prod", logFile)
            
            prodtokenfileName = os.path.join(OCONF._ordopath,'token.txt')
            if os.path.exists(prodtokenfileName):
                os.remove(prodtokenfileName)
            printAndLog("Copy prod {} {} ".format(newtokenfileName, prodtokenfileName), logFile)
            copyfile(newtokenfileName, prodtokenfileName)
            printAndLog("Broadcast is done", logFile)            
        except Exception, e:
            try:
                f.close()
            except:
                pass
            printAndLog("Exception({}): {}".format(e.errno, e.strerror), logFile)
                
        

    
        
        
        
        