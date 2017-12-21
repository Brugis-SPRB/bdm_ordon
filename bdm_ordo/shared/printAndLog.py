from datetime import datetime

def printAndLog(myLine, myFile):
    print (myLine)
    if myLine is None:
        myFile.write("{}\n".format(datetime.now()) )
    else:
        myFile.write("{} : {}\n".format(datetime.now(),myLine) )

def printNow(myFile):
    printAndLog(None, myFile)