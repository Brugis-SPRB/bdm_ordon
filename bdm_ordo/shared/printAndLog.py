from datetime import datetime

def printAndLog(myLine, myFile):
    print myLine
    if myLine is None:
        myFile.write("{}\n".format(datetime.today()) )
    else:
        myFile.write("{} : {}\n".format(datetime.today(),myLine) )

def printNow(myFile):
    printAndLog(None, myFile)