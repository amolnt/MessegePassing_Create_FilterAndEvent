import os
import time
import hashlib
import json
import re
import datetime
import psycopg2
from ConfigParser import SafeConfigParser

checkRecord=[]
parser=SafeConfigParser()
parser.read('../tConfig.cfg')
fileDir=parser.get('fileOperations','files')

now=datetime.datetime.now()
def generateResponse(filename,data):
    count=0
    data = json.loads(data)
    fileSep=filename.split(".")

    try:
        event=data['event']
        fflag=True
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            listfiles=os.listdir(fileDir)
            for files in listfiles:
                if str(files)==str(event['user'])+".calender.response.txt":
                    fflag=False
                    break
            if fflag==True:
                cursor.execute("insert into event(username,eventName,location,datetime,discription,invitedUser) values('"+str(event['user'])+"','"+str(event['eventName'])+"','"+str(event['location'])+"','"+str(event['date'])+"','"+str(event['discription'])+"','"+str(event['users'])+"');")
               
                fdResponse=open(fileDir+""+event['user']+".calender.response.txt","w+")
                fdResponse.write("1")
                fdResponse.close()
            else:
                fdResponse=open(fileDir+""+event['user']+".calender.response.txt","w+")
                fdResponse.write("0")
                fdResponse.close()
            db.commit()
            db.close()
            return
        except psycopg2.OperationalError as e:
            db.commit()
            db.close()
            print e
    except KeyError,e:
        pass
    except TypeError as e:
        pass


    try:
        upcoming=data['upcoming']
        string=""
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select eventid,username,eventname,location,datetime,discription,inviteduser from event where (inviteduser like '"+upcoming['user']+"' or username='"+upcoming['user']+"') and datetime>=now() order by datetime asc;")
            b=cursor.fetchall()
            fdResponse=open(fileDir+""+upcoming['user']+".calender.response.csv","w+")
            for records in b:
                string=""
                for rd in records:
                    string+=str(rd)+"~"
                string=string.rstrip('~ ')
                string+="\n"
                    
                with open(fileDir+""+upcoming['user']+".calender.response.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
            db.commit()
            db.close()
            return
        except psycopg2.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError:
        pass
    except IOError:
        pass

    try:
        past=data['past']
        string=""
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select eventid,username,eventname,location,datetime,discription,inviteduser from event where (inviteduser like '"+past['user']+"' or username='"+past['user']+"') and datetime<=now() order by datetime asc;")
            b=cursor.fetchall()
            fdResponse=open(fileDir+""+past['user']+".calender.response.csv","w+")
            for records in b:
                string=""
                for rd in records:
                    string+=str(rd)+"~"
                string=string.rstrip('~ ')
                string+="\n"

                with open(fileDir+""+past['user']+".calender.response.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
            db.commit()
            db.close()
            return
        except psycopg2.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError:
        pass
    except IOError:
        pass

    try:
        events=data['getAllEvents']
        string=""
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select eventid,username,eventname,location,datetime,discription,inviteduser from event where username like '"+events['user']+"' order by datetime desc;")
            b=cursor.fetchall()
            fdResponse=open(fileDir+""+events['user']+".calender.response.csv","w+")
            for records in b:
                string=""
                for rd in range(0,len(records)):
                    if records[rd]=="" or records[rd]=="" or records[rd]=="":
                        string+="None"+"~"
                    else:    
                        string+=str(records[rd])+"~"
                string=string.rstrip('~ ')
                string+="\n"
                with open(fileDir+""+events['user']+".calender.response.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
            db.commit()
            db.close()
            return
        except psycopg2.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError,e:
        pass
    except IOError:
        pass

    try:
       
        event=data['deleteEvent']
        fflag=True
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            listfiles=os.listdir(fileDir)
            for files in listfiles:
                if str(files)==str(event['user'])+".calender.response.txt":
                    fflag=False
                    break
            if fflag==True:
                cursor.execute("delete from event where username='"+str(event['user'])+"' and eventid='"+str(event['eventid'])+"';")
                db.commit()
                cursor.execute("select * from event where eventid='"+str(event['eventid'])+"';")
                b=cursor.fetchall()
                if len(b)==0:
                    fdResponse=open(fileDir+""+event['user']+".calender.response.txt","w+")
                    fdResponse.write("1")
                    fdResponse.close()
                else:
                    fdResponse=open(fileDir+""+event['user']+".calender.response.txt","w+")
                    fdResponse.write("0")
                    fdResponse.close()
            db.close()
            return
        except psycopg2.OperationalError,e:
            print e
            db.commit();
            db.close();
    except KeyError,e:
        pass
    except TypeError,e:
        pass
    except IOError,e:
        pass

        
    try:
        event=data['updateEvent']
        fflag=True
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            listfiles=os.listdir(fileDir)
            listfiles=os.listdir(fileDir)
            for files in listfiles:
                if str(files)==str(event['user'])+".calender.response.txt":
                    fflag=False
                    break
            if fflag==True:
                cursor.execute("update event set eventname='"+str(event['eventName'])+"',location='"+str(event['location'])+"',datetime='"+str(event['date'])+"',discription='"+str(event['discription'])+"',inviteduser='"+str(event['users'])+"' where eventid='"+str(event['eventid'])+"';")
                db.commit()
                fdResponse=open(fileDir+""+event['user']+".calender.response.txt","w+")
                fdResponse.write("1")
                fdResponse.close()
            db.close()
            return
        except psycopg2.OperationalError,e:
            print e
            db.commit();
            db.close();
    except KeyError,e:
        pass
    except TypeError,e:
        pass
    except IOError,e:
        pass

    #remove responses
    try:
        filename=filename.split(".")
        fil=filename[1]+"."+filename[2]+"."+filename[3]
    	if str(data)[0]=='{' and str(data)[1]=='}' and fil=="calender.request.json" :
            listfiles=os.listdir(fileDir)
            for files in listfiles:
                if files==str(filename[0]+".calender.response.csv"):
                    os.system("rm "+fileDir+""+filename[0]+".calender.response.csv")
                if files==str(fileSep[0])+".response.csv":
                    os.system("rm "+fileDir+""+fileSep[0]+".response.csv")
                    
        if str(data)[0]=='{' and str(data)[1]=='}' and fil=="createDeleteUpdateEvent.request.json" :
            listfiles=os.listdir(fileDir)
            for files in listfiles:
                if files==str(filename[0]+".calender.response.txt"):
                    os.system("rm "+fileDir+""+filename[0]+".calender.response.txt")
    except KeyError:
        return

def periodicallyCheck():
    parseIndex=0
    connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
    conn = psycopg2.connect(connection_str)
    c = conn.cursor()
    
    c.execute("select * from requestsWatcher")
    row=c.fetchall()
    try:
        for records in row:
            fileSep=records[0].split(".")
            name=fileSep[1]+"."+fileSep[2]+"."+fileSep[3]
            if name=="calender.request.json":
                generateResponse(records[0],records[1])
            if name=="createDeleteUpdateEvent.request.json":
                generateResponse(records[0],records[1])
        conn.commit()
        conn.close()
        fd.close()
    except IndexError:
        pass

def main():
    cnt=0
    try:
    	while True:
            periodicallyCheck()
    except KeyboardInterrupt:
        return
        
main()
