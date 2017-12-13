'''
Created on 8 mars 2017

@author: mvanasten
'''
import os

class dbBackupRestore(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def backup(self,
               host,
               port, 
               username,
               schema,
               logfile):
        cmd = ('pg_dump' 
        '--host {}' 
        '--port {}' 
        '--username {}' 
        '--no-password'  
        '--format custom' 
        '--blobs' 
        '--encoding UTF8' 
        '--schema {}' 
        '--file {}').format(host,
                            port,
                            username,
                            schema,
                            logfile)
        os.system(cmd)
        
    def restore(self,
                host,
                port, 
                username,
                schema,
                backupfile,
                logfile):
        cmd = ('pg_restore' 
               '--host {}' 
               '--port {}'
               '--username {}' 
               '--no-password'  
               '-d databrugis' 
               '--verbose  {}  > {}').format( host,
                                              port,
                                              username,
                                              backupfile,
                                              logfile)
                
        os.system(cmd)