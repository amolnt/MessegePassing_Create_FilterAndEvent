import os
import time
import psycopg2
from ConfigParser import SafeConfigParser

parser=SafeConfigParser()
parser.read('../tConfig.cfg')
filesDir=parser.get('fileOperations','files')
databaseDir=parser.get('fileOperations','database')
sleepDuration=parser.get('fileOperations','sleepDuration')
    
def insertDatabase(filename,data): 
    try:
        connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
        conn = psycopg2.connect(connection_str)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO requestsWatcher (filename,data) SELECT '"+filename+"','"+str(data)+"' WHERE NOT EXISTS (SELECT 1 FROM requestsWatcher WHERE filename='"+filename+"');");
        cursor.execute("SELECT filename FROM requestsWatcher where filename='"+filename+"';");
        b = cursor.fetchall()
        if len(b)!=0:
            cursor.execute("update requestsWatcher set data='"+data+"',updateFlag=1 where filename='"+filename+"';")
        conn.commit()
        conn.close()
    except Exception as e:
        print e
def periodicallyCheck():
    fileList=""
    fileNameWithExtention=""
    fileList=os.listdir(filesDir)
    dirList=[]
    parseIndex=0
    data=""
    for files in fileList:
        try:
            if str(files)==".request.json":
                os.remove(filesDir+""+".request.json")
            else:
                if os.path.isfile(filesDir+""+files):
                    fileSep=files.split(".")
                    if fileSep[2]=="json" and len(fileSep)==3:
                        fileNameWithExtention=str(fileSep[0])+"."+str(fileSep[1])+"."+str(fileSep[2])
                        dirList.append(fileNameWithExtention)
                    if fileSep[3]=="json" and len(fileSep)==4:
                        fileNameWithExtention=str(fileSep[0])+"."+str(fileSep[1])+"."+str(fileSep[2])+"."+str(fileSep[3])
                        dirList.append(fileNameWithExtention)
        except IndexError:
            pass

    try:
        for files in dirList:
            with open(filesDir+""+str(files),'rb') as f:
                data = f.read()
            insertDatabase(files,data)
    except IndexError:
            pass
        
def main():
    try:
        while True:
            periodicallyCheck()
    except KeyboardInterrupt:
        return
        
main()
