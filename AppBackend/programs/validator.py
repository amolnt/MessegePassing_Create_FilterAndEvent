import os
import sqlite3
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
databaseDir=parser.get('fileOperations','database')
logFile=parser.get('fileOperations','logFile')
logDir=parser.get('fileOperations','logDir')

fd=open(logFile,"a")
now=datetime.datetime.now()
def generateResponse(filename,data):
    count=0
    data = json.loads(data)
    fileSep=filename.split(".")

    try:
        sign=data['signup'][0]
        fdlog=open(logDir+"userRegister.log","a+")
        listfiles=os.listdir(fileDir)
        flag=True
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
    
            cursor.execute("select username from users where username='"+str(sign['username'])+"';")
            b=cursor.fetchall()
     
            if(len(b)==0):
                query="insert into users(fname,lname,username,email,password,birthDate,gender,mobileNo) values('"+str(sign['fname'])+"','"+str(sign['lname'])+"','"+str(sign['username'])+"','"+str(sign['email'])+"','"+str(sign['password'])+"','"+str(sign['birthdate'])+"','"+str(sign['gender'])+"','"+str(sign['mobileno'])+"');"
                cursor.execute(query)
                
                query+="insert into event (username,eventname,datetime) values('"+sign['username']+"','birthday','"+sign['birthdate']+"');"
                cursor.execute(query)

                fdResponse=open(fileDir+""+fileSep[0]+".response.txt","w+")
                fdResponse.write(str(1))
                fdResponse.close()

                fdlog.write(str(time.strftime("20%y-%m-%db %H:%M:%S"))+"\n"+str(sign['username'])+" user created successfully\n")
            else:
                for files in listfiles:
                	if str(files)==str(sign['username'])+".response.txt":
                		flag=False
                		break
                if flag==True:
                	fdResponse=open(fileDir+""+fileSep[0]+".response.txt","w+")
                	fdResponse.write(str(0))
                	fdResponse.close()
            db.commit()
            db.close()
            fdlog.close()
            return
        except sqlite3.OperationalError as e:
            db.commit()
            db.close()
            fdlog.close()
            print e
    except KeyError,e:
        pass
    except TypeError as e:
            pass
    
    #Login
    try:
        login=data['login']
        fdlog=open(logDir+"userLogin.log","a+")
        listfiles=os.listdir(fileDir)
        flag=True
        try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select username,password from users where username='"+str(login['username'])+"' and password='"+str(login['password'])+"';")
            b=cursor.fetchall()
            if len(b)==0:
                fdResponse=open(fileDir+""+fileSep[0]+".response.txt","w+")
                fdResponse.write(str(0))
                fdResponse.close() 
            else:
                fdResponse=open(fileDir+""+fileSep[0]+".response.txt","w+")
                fdResponse.write(str(1))
                fdResponse.close()
                fdlog.write(str(time.strftime("20%y-%m-%db %H:%M:%S"))+"\n"+str(login['username'])+" user login successfully\n")
            fdlog.close()
            db.commit()
            db.close()
            return
        except sqlite3.OperationalError,e:
            fdlog.close()
    except KeyError,e:
        pass
    except TypeError as e:
        pass

#SendinMsg
    try:
        sendMsg=data['sendMsg']
        listfiles=os.listdir(fileDir)
        fflag=True
        try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select username from users where username='"+str(sendMsg['user_to'])+"';")
            b=cursor.fetchall()
            if len(b)==0:
                for files in listfiles:
                    if str(files)==str(sendMsg['user_from'])+".response.txt":
                        fflag=False
                        break
                if fflag==True:
                    cursor.execute("insert into outbox(user_from,user_to,subject,message,sending_time) values('"+str(sendMsg['user_from'])+"','"+str(sendMsg['user_to'])+"','"+str(sendMsg['subject'])+"','"+str(sendMsg['message'])+"','"+str(time.strftime("20%y-%m-%d %H:%M:%S"))+"');")
                   
                    fdResponse=open(fileDir+""+fileSep[0]+".response.txt","w+")
                    fdResponse.write(str(0))
                    fdResponse.close()
            else:
                for files in listfiles:
                    if str(files)==str(sendMsg['user_from'])+".response.txt":
                        fflag=False
                        break
                if fflag==True:
                    cursor.execute("insert into messages(user_from,user_to,subject,message,sending_time) values('"+str(sendMsg['user_from'])+"','"+str(sendMsg['user_to'])+"','"+str(sendMsg['subject'])+"','"+str(sendMsg['message'])+"','"+str(time.strftime("20%y-%m-%d %H:%M:%S"))+"');")
                    count+=1
                    fdResponse=open(fileDir+""+fileSep[0]+".response.txt","w+")
                    fdResponse.write(str(1))
                    fdResponse.close()

            db.commit()
            db.close()
            return
        except sqlite3.OperationalError,e:
            db.commit()
            db.close()
    except KeyError,e:
        pass
    except TypeError as e:
        pass

    #inbox
    try:
        inbox=data['inbox']
        msg=""
        try:
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            with open(fileDir+""+inbox['user_to']+".iNotify.csv",'rb') as f:
                data = f.read()
            data=data.split("\n")
            del(data[len(data)-1])
            for dt in data:
                dt=dt.split(",")
                if int(dt[len(dt)-1])==0:
                    cursor.execute("update messages set status=1 where id="+dt[0]+";")
                db.commit()
            db.close()
            fdResponse=open(fileDir+""+fileSep[0]+".response.txt","w+")
            fdResponse.close()
            return
        except sqlite3.OperationalError,e:
            db.commit()
            db.close()
    except KeyError,e:
        pass
    except TypeError as e:
        pass
    except IOError:
        pass

#iNotify
    try:
    	iNotify=data['iNotify']
        string=""
    	try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select id,user_from,user_to,subject,message,label,sending_time,status from messages where user_to='"+str(iNotify['user_from'])+"';")
            b=cursor.fetchall()
            
            fdResponse=open(fileDir+""+iNotify['user_from']+".iNotify.csv","w+")
            for records in b:
                string=""
                for rd in records:
                    string+=str(rd)+","
                string=string.rstrip(',')
                string+="\n"
                    
                with open(fileDir+""+iNotify['user_from']+".iNotify.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
            db.commit()
            db.close()
            return
    	except sqlite3.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError:
        pass
    except IOError:
        pass

    #outbox
    try:
    	outbox=data['outbox']
        string=""
    	try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select id,user_from,user_to,subject,message,label,sending_time,status from outbox where user_from='"+str(outbox['user_from'])+"';")
            b=cursor.fetchall()
            
            fdResponse=open(fileDir+""+outbox['user_from']+".draft.csv","w+")
            for records in b:
                string=""
                for rd in records:
                    string+=str(rd)+","
                string=string.rstrip(',')
                string+="\n"
                with open(fileDir+""+outbox['user_from']+".draft.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
            db.commit()
            db.close()
            return
    	except sqlite3.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError:
        pass
    except IOError:
        pass
    

    #get all users
    try:
    	getuser=data['getusers']
        string=""
    	try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select username from users;")
            b=cursor.fetchall()
            if len(b)==0:
                fdResponse=open(fileDir+""+getuser['user']+".users.csv","w+")
                fdResponse.write("")
                fdResponse.close()	
                return
            fdResponse=open(fileDir+""+getuser['user']+".users.csv","w+")
            for records in b:
                string=""
                for rd in records:
                    string+=str(rd)+","
                string=string.rstrip(',')
                string+="\n"
                with open(fileDir+""+getuser['user']+".users.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
            db.commit()
            db.close()
            return
    	except sqlite3.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError:
        pass
    except IOError:
        pass


    #getlabels
    try:
    	getLabel=data['getlabels']
        string=""
    	try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select labelid,labelName from label where username='"+str(getLabel['user'])+"';")
            b=cursor.fetchall()
            if len(b)==0:
                fdResponse=open(fileDir+""+getLabel['user']+".labels.csv","w+")
                fdResponse.write("")
                fdResponse.close()	
                return
            fdResponse=open(fileDir+""+getLabel['user']+".labels.csv","w+")
            for records in b:
                string=""
                for rd in records:
                    string+=str(rd)+","
                string=string.rstrip(',')
                string+="\n"
                with open(fileDir+""+getLabel['user']+".labels.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
            string=""
            cursor.execute("select labelHid,labelName from labelHirarchy where username='"+str(getLabel['user'])+"';")
            b=cursor.fetchall()
            if len(b)==0:
                fdResponse=open(fileDir+""+getLabel['user']+".labels.csv","a")
                fdResponse.write("")
                fdResponse.close()	
                return
            for records in b:
                string=""
                for rd in records:
                    string+=str(rd)+","
                string=string.rstrip(',')
                string+="\n"
                with open(fileDir+""+getLabel['user']+".labels.csv", "a+") as myfile:
                    myfile.write(string)
                myfile.close()
                
            db.commit()
            db.close()
            return
    	except sqlite3.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError:
        pass
    except IOError:
        pass

    #add single label
    try:
        singLabel=data['singLabel']
        listfiles=os.listdir(fileDir)
        fflag=True
        try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            for files in listfiles:
                if str(files)==str(singLabel['user'])+".response.txt":
                    fflag=False
                    break
            if fflag==True:
                cursor.execute("insert into label(labelName,subject,username,users) values('"+str(singLabel['labelName'])+"','"+str(singLabel['subject'])+"','"+str(singLabel['user'])+"','"+str(singLabel['users'])+"');")
                fdResponse=open(fileDir+""+str(singLabel['user'])+".response.txt","w+")
                fdResponse.write(str(1))
                fdResponse.close()
            db.commit()
            db.close()
            return
        except Exception:
            db.commit()
            db.close()
        except psycopg2.IntegrityError:
            db.commit()
            db.close()
        
    except KeyError,e:
        pass
    except TypeError as e:
        pass


    #add hirarchy label
    try:
        hirLabel=data['hirLabel']
        listfiles=os.listdir(fileDir)
        fflag=True
        try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            for files in listfiles:
                if str(files)==str(hirLabel['user'])+".response.txt":
                    fflag=False
                    break
            if fflag==True:
		
                cursor.execute("insert into labelHirarchy(parent_id,labelName,subject,username,users) values('"+str(hirLabel['parent_id'])+"','"+str(hirLabel['labelName'])+"','"+str(hirLabel['subject'])+"','"+str(hirLabel['user'])+"','"+str(hirLabel['users'])+"');")
                fdResponse=open(fileDir+""+str(hirLabel['user'])+".response.txt","w+")
                fdResponse.write(str(1))
                fdResponse.close()
            db.commit()
            db.close()
            return
        except Exception,e:
            db.commit()
            db.close()
	    print e
        except psycopg2.IntegrityError:
            db.commit()
            db.close()
        
    except KeyError,e:
        pass
    except TypeError as e:
        pass

    
    #get label hirarchy
    try:
        hirLabel=data['getallLabels']
        listfiles=os.listdir(fileDir)
        fflag=True
        string="["
        try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select labelid,labelName from label where username like '"+hirLabel['user']+"';")
            b=cursor.fetchall()
            i=0
            while(i<len(b)):
                string+="('"+b[i][1]+"'"
                cursor.execute("select labelhid,labelName from labelHirarchy where parent_id like '"+b[i][0]+"' and username like '"+hirLabel['user']+"';")
                hr=cursor.fetchall()
                if len(hr)!=0:
                    string+=",["
                    j=0
                    while(j<len(hr)):
                        string+="('"+hr[j][1]+"'"
                        cursor.execute("select labelhid,labelName from labelHirarchy where parent_id like '"+hr[j][0]+"' and username like '"+hirLabel['user']+"';")
                        hr1=cursor.fetchall()
                        if len(hr1)!=0:
                            string+=",["
                            k=0
                            while(k<len(hr1)):
                                string+="('"+hr1[k][1]+"'"
                                cursor.execute("select labelhid,labelName from labelHirarchy where parent_id like '"+hr1[k][0]+"' and username like'"+hirLabel['user']+"';")
                                hr2=cursor.fetchall()
                               
                                if len(hr2)!=0:
                                    string+=",[('"+hr2[0][1]+"')]"                            
                                k+=1    
                                if k==len(hr1):
                                    string+=""
                                else:
                                    string+="),"
                            string+=")]"
                        else:
                            string+="),"
                        j+=1
                    string+=")]"
                i+=1
                if i==len(b):
                    string+=")"
                else:
                    string+="),"
            string+="]"
            fdResponse=open(fileDir+""+hirLabel['user']+".labels.csv","w+")
            with open(fileDir+""+hirLabel['user']+".labels.csv", "a+") as myfile:
                myfile.write(string)
            myfile.close()
            fdResponse.close()
            db.commit()
            db.close()
            return
        except Exception,e:
            db.commit()
            db.close()
            print e
        except psycopg2.IntegrityError:
            db.commit()
            db.close()
            print e
        
    except KeyError,e:
        pass
    except TypeError as e:
        pass

    try:
    	labelMsg=data['labelsMsg']
        string=""
    	try:
            #db = sqlite3.connect(databaseDir+"user.db")
            connection_str="dbname='amol' user='amol' host='localhost' password='@mol'"
            db = psycopg2.connect(connection_str)
            cursor = db.cursor()
            cursor.execute("select subject,users from label where labelName='"+str(labelMsg['label'])+"';")
            b=cursor.fetchall()
            if len(b)==0:
                cursor.execute("select subject,users from labelHirarchy where labelName='"+str(labelMsg['label'])+"';")
                b=cursor.fetchall()
                if len(b[0][0])==0 or len(b[0][1])==0:
                    with open(fileDir+""+labelMsg['user']+".labelMsg.csv", "w+") as myfile:
                        myfile.write("")
                    return
                else:
                    query="select id,user_from,user_to,subject,message,label,sending_time,status from messages where user_to='"+str(labelMsg['user'])+"' and subject='"+b[0][0]+"' and (user_from='"
                    users=b[0][1].split(",")
                    i=0
                    for urs in users:
                        if i==len(users)-1:
                            query+=urs+"');"
                        else:
                            query+=urs+"' or user_from='"
                        i+=1
                    cursor.execute(query)
                    b=cursor.fetchall()
                    fdResponse=open(fileDir+""+labelMsg['user']+".labelMsg.csv","w+")
                    for records in b:
                        string=""
                        for rd in records:
                            string+=str(rd)+","
                        string=string.rstrip(',')
                        string+="\n"
                    
                    with open(fileDir+""+labelMsg['user']+".labelMsg.csv", "a+") as myfile:
                        myfile.write(string)
                    myfile.close()
            else:
                if len(b[0][0])==0 or len(b[0][1])==0:
                    with open(fileDir+""+labelMsg['user']+".labelMsg.csv", "w+") as myfile:
                        myfile.write("")
                        return
                else:
                    query="select id,user_from,user_to,subject,message,label,sending_time,status from messages where user_to='"+str(labelMsg['user'])+"' and subject='"+b[0][0]+"' and (user_from='"
                    users=b[0][1].split(",")
                    i=0
                    for urs in users:
                        if i==len(users)-1:
                            query+=urs+"');"
                        else:
                            query+=urs+"' or user_from='"
                        i+=1
                    cursor.execute(query)
                    b=cursor.fetchall()
                    fdResponse=open(fileDir+""+labelMsg['user']+".labelMsg.csv","w+")
                    for records in b:
                        string=""
                        for rd in records:
                            string+=str(rd)+","
                        string=string.rstrip(',')
                        string+="\n"
                    
                    with open(fileDir+""+labelMsg['user']+".labelMsg.csv", "a+") as myfile:
                        myfile.write(string)
                    myfile.close()
            db.commit()
            db.close()
            return
    	except sqlite3.OperationalError,e:
            db.commit();
            db.close();
    except KeyError:
        pass
    except TypeError:
        pass
    except IOError:
        pass

    #remove all responses
    try:
        filename=filename.split(".")
        filename=filename[1]+"."+filename[2]
    	if str(data)[0]=='{' and str(data)[1]=='}' and filename=="request.json" :
            listfiles=os.listdir(fileDir)
            for files in listfiles:
                if files==str(fileSep[0])+".response.txt":
                    os.system("rm "+fileDir+""+fileSep[0]+".response.txt")
                if files==str(fileSep[0])+".labelMsg.csv":
                    os.system("rm "+fileDir+""+fileSep[0]+".labelMsg.csv")
                 
        if str(data)[0]=='{' and str(data)[1]=='}' and filename=="iNotify.json" :
            listfiles=os.listdir(fileDir)
            for files in listfiles:
                if files==str(fileSep[0])+".iNotify.csv":
                    os.system("rm "+fileDir+""+fileSep[0]+".iNotify.csv")
                if files==str(fileSep[0])+".draft.csv":
                    os.system("rm "+fileDir+""+fileSep[0]+".draft.csv")
                if files==str(fileSep[0])+".labels.csv":
                    os.system("rm "+fileDir+""+fileSep[0]+".labels.csv")
                if files==str(fileSep[0])+".users.csv":
                    os.system("rm "+fileDir+""+fileSep[0]+".users.csv")
                if files==str(fileSep[0])+".labels.txt":
                    os.system("rm "+fileDir+""+fileSep[0]+".labels.txt")
                
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
