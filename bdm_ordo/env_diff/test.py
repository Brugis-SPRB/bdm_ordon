'''
Created on 8 mars 2017

@author: mvanasten
'''
import glob 
import re
import os
        
def doRoll(basedir, fileprefix, tempprefix, exten, threshold):
    pattern = "{}*.{}".format(fileprefix, exten)
    print pattern
    lstfiles = glob.glob1(basedir, pattern )
    print lstfiles
    for filename in lstfiles:
        ##########################
        # Extract sequence number
        
        p = re.compile('{}([0-9]?)\.{}'.format(fileprefix,exten))
        m = p.search( filename )
        seq = m.group(1)
        if len(seq) < 1:
            seq = 1
        else:
            seq = int(seq) + 1
        ##########################
        # delete file with sequence >= threshold
        if seq >= threshold:
            os.remove(os.path.join(basedir,file))
        ##########################
        # create temporary file
        tFileName = "{}{}.{}".format(tempprefix,str(seq),exten)
        tPath = os.path.join(basedir,tFileName)
        oldPath = os.path.join(basedir,file)
        os.rename(oldPath, tPath)
    
    #######################
    # rename all files 
    pattern = "{}*.{}".format(tempprefix, exten)
    print pattern
    lstfiles = glob.glob1(basedir, pattern )
    
    for filename in lstfiles:
        p = re.compile('{}([0-9]?)\.{}'.format(tempprefix,exten))
        m = p.search( filename )
        seq = m.group(1)
        if len(seq) < 1:
            seq = 1
        else:
            seq = int(seq)

        newFileName = '{}{}.{}'.format(fileprefix,str(seq),exten)
        newPath = os.path.join(basedir,newFileName)
        oldPath = os.path.join(basedir,file)
        os.rename(oldPath, newPath)




if __name__ == '__main__':
    doRoll('c:/temp/', 'essais', 'tessais', 'txt', 8)
    pass