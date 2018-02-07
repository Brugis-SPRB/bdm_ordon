# -*- coding: latin_1 -*-
# PostMaster perform state machine exchange between servers : state change notification, token exchange, failure message dispatching,

import datetime
import os
import sys
import ftplib
from shutil import copyfile
import smtplib

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))


import shared.ordoconf as OCONF
import shared.databrugisconf as DBRUC
from shared.printAndLog import printAndLog


#########################################
#

def send_mail(subject, body):
    
    sender = DBRUC._mailSender
    receivers = DBRUC._mailReceivers
    msg = "\r\n".join([
        "From: " + sender,
        "To: " + ",".join(receivers),
        "Subject: " + subject,
        "",
        body
        ])
    try:
        server = smtplib.SMTP(DBRUC._smtpServer)
        server.ehlo()
        server.sendmail(sender, receivers, msg)
        print ("Successfully sent mail")
    except Exception:
        print ("Error : Unable to send email {}".format(sys.exc_info()[0]))

################################################################################

def ftpDownload(ftpConn, localdir, remotedir, localfilename, distfilemename ):
    ftpConn.cwd(remotedir)
    localFile = os.path.join(localdir, localfilename)
    if os.path.exists(localFile):
        os.remove(localFile)                
    with open(localFile, "wb") as gFile:
        try:
            f.retrbinary('RETR {}'.format(distfilemename), gFile.write)
        except:
            pass

def ftpDelete(ftpConn, remotedir, distfilemename ):
    ftpConn.cwd(remotedir)
    try:
        f.delete(distfilemename)
    except:
        pass



def parseTokenFile(filename):
    try:
        tokenfile = open(filename)
        tokencontent = tokenfile.read()
        parts = tokencontent.split(',')
        return {'step':parts[0],'state':parts[1]}
    except Exception:
        return {'step':'undefined','state':'undefined'}


def parseMsgFile(filename):
    try:
        msgfile = open(filename)
        msgcontent = msgfile.read()
        
        res = msgcontent.strip()
        
        if len(res) < 1:
            return None
        else:
            return msgcontent
    except Exception:
        pass
    return None


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
            #
            # Cleanup msgs replica
            oldprodmsg = os.path.join(localDirn, "prod_ordo.msg")
            olddiffmsg = os.path.join(localDirn, "diff_ordo.msg")
            oldstagingmsg = os.path.join(localDirn, "staging_ordo.msg")
            if os.path.exists(oldprodmsg):
                os.remove(oldprodmsg)
            if os.path.exists(olddiffmsg):
                os.remove(olddiffmsg)
            if os.path.exists(oldstagingmsg):
                os.remove(oldstagingmsg)        
            ########################################
            # copy diff and staging to local replica
            printAndLog("download diff ", logFile)
            ftpDownload(f, localDirn, dirndiff, "diff_token.txt", "token.txt" )
            ftpDownload(f, localDirn, dirndiff, "diff_ordo.msg", "ordo.msg" )  
            ftpDownload(f, localDirn, dirndiff, "diff_ordo.state", "ordo.state" )  
              
            ftpDelete(f, dirndiff, "ordo.msg" )
            ftpDelete(f, dirndiff, "ordo.state" )
            
            printAndLog("download staging", logFile)
            ftpDownload(f, localDirn, dirnstaging, "staging_token.txt", "token.txt" )
            ftpDownload(f, localDirn, dirnstaging, "staging_ordo.msg", "ordo.msg" )    
            ftpDownload(f, localDirn, dirnstaging, "staging_ordo.state", "ordo.state" )    
            
            ftpDelete(f, dirnstaging, "ordo.msg" )
            ftpDelete(f, dirnstaging, "ordo.state" )
            
            f.close()
            f.cwd(ROOT)
            f.quit()
        except Exception:
            try:
                f.close()
            except Exception:
                pass
            print ("Exception {}".format(sys.exc_info()[0]))
        
        ########################################
        # copy prod to local replica        
        prodtokenfile = os.path.join(OCONF._ordopath,'token.txt')
        prodmsgfile = os.path.join(OCONF._ordopath,'ordo.msg')
        prodstatefile = os.path.join(OCONF._ordopath,'ordo.state')
        
        
        localFile = os.path.join(localDirn, "prod_token.txt")
        localmsg = os.path.join(localDirn, "prod_ordo.msg")
        localstate = os.path.join(localDirn, "prod_ordo.state")
        
        if os.path.exists(localFile):
            os.remove(localFile)
        try:
            copyfile(prodtokenfile, localFile)
        except Exception:
            print ("Exception {}".format(sys.exc_info()[0]))
        
        if os.path.exists(localmsg):
            os.remove(localmsg)
        try:
            copyfile(prodmsgfile, localmsg)
            os.remove(prodmsgfile)
        except Exception:
            print ("Exception {}".format(sys.exc_info()[0]))
        
        
        if os.path.exists(localstate):
            os.remove(localstate)
        try:
            copyfile(prodstatefile, localstate)
            os.remove(prodstatefile)
        except Exception:
            print ("Exception {}".format(sys.exc_info()[0]))
            
        ######################################
        # Parse TOKENS content
        
        printAndLog("Parse TOKENS content", logFile)
        
        difftoken = parseTokenFile(os.path.join(localDirn,'diff_token.txt'))
        stagingtoken = parseTokenFile(os.path.join(localDirn,'staging_token.txt'))
        prodtoken = parseTokenFile(os.path.join(localDirn,'prod_token.txt'))
        
        
        ######################################
        # Parse msg content
        
        printAndLog("Parse MSGS content", logFile)
        
        diffmsg = parseMsgFile(os.path.join(localDirn,'diff_ordo.msg'))
        stagingmsg = parseMsgFile(os.path.join(localDirn,'staging_ordo.msg'))
        prodmsg = parseMsgFile(os.path.join(localDirn,'prod_ordo.msg'))
        
        ######################################
        # Send mail if required
        
        if diffmsg != None:
            if len(diffmsg) > 0:
                printAndLog("Diff message [{}]".format(diffmsg), logFile)
                #send_mail("Bdm ,Anomalie,diffusion", diffmsg)
        if stagingmsg != None:
            if len(stagingmsg) > 0:
                printAndLog("Staging message [{}]".format(stagingmsg), logFile)
                #send_mail("Bdm ,Anomalie,staging", stagingmsg)
        if prodmsg != None:
            if len(prodmsg) > 0:
                printAndLog("Prod message [{}]".format(prodmsg), logFile)
                #send_mail("Bdm ,Anomalie,production", prodmsg)
        
        
        ######################################
        # Parse state file content
        
        printAndLog("Parse State file content", logFile)
        
        diffstate = parseMsgFile(os.path.join(localDirn,'diff_ordo.state'))
        stagingstate = parseMsgFile(os.path.join(localDirn,'staging_ordo.state'))
        prodstate = parseMsgFile(os.path.join(localDirn,'prod_ordo.state'))
        
        ######################################
        # output state change on remote server
        
        stateChange = None
        
        if diffstate != None:
            if len(diffstate) > 0:
                stateChange = diffstate 
        if stagingstate != None:
            if len(stagingstate) > 0:
                stateChange = stagingstate
        if prodstate != None:
            if len(prodstate) > 0:
                stateChange = prodstate
        
        if stateChange != None:
            printAndLog("State change [{}]".format(stateChange), logFile)
        
        
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
            
            prodtokenfileName = os.path.join(OCONF._ordopath,'token.txt')
            if os.path.exists(prodtokenfileName):
                os.remove(prodtokenfileName)
            printAndLog("Push prod {} {} ".format(newtokenfileName, prodtokenfileName), logFile)
            copyfile(newtokenfileName, prodtokenfileName)
            printAndLog("Broadcast is done", logFile)            
        except Exception:
            try:
                f.close()
            except:
                pass
            printAndLog("Exception {}".format(sys.exc_info()[0]))
                
        

    
        
        
        
        