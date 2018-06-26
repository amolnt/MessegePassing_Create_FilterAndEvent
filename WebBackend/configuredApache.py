import commands, sys
import os
import re
def Configure(cmd):
    failure, output = commands.getstatusoutput(cmd)
    print output
    if failure:
       print 'Command: %s\nfailed.' % cmd
       sys.exit(1)
    return output
def configure():
    currentDirectory=os.getcwd()
    currentDirectory=currentDirectory.split("/")
    del(currentDirectory[len(currentDirectory)-1])
    currentDirectory="/".join(currentDirectory)+""
    
    i=164
    flag=False
    count=0
    while 1:
        output=Configure("sed '"+str(i)+"!d' /etc/apache2/apache2.conf")
        if re.match(r'^</Directory>$',output):
            Configure("sudo sed -e '"+str(i)+"d' /etc/apache2/apache2.conf > .tempFile;sudo mv .tempFile /etc/apache2/apache2.conf")
            break
        elif output.find("<Directory")!=-1:
            Configure("sudo sed -e '"+str(i)+"d' /etc/apache2/apache2.conf > .tempFile;sudo mv .tempFile /etc/apache2/apache2.conf")
            flag=True
        elif flag==True:
            Configure("sudo sed -e '"+str(i)+"d' /etc/apache2/apache2.conf > .tempFile;sudo mv .tempFile /etc/apache2/apache2.conf")
        else:
            count+=1
        if count==3:
            break

    Configure("sudo sed -i '164i<Directory "+currentDirectory+">'  /etc/apache2/apache2.conf")
    Configure("sudo sed -i '165i    Options Indexes FollowSymLinks' /etc/apache2/apache2.conf")        
    Configure("sudo sed -i '166i    AllowOverride None' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '167i    Order allow,deny' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '168i    Require all granted' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '169i    Allow from all' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '170i    AddHandler mod_python .psp' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '171i    PythonHandler mod_python.psp' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '172i    PythonDebug On' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '173i    AuthType None' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '174i    DirectoryIndex "+currentDirectory+"WebBackend/login.psp' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '175i    require valid-user' /etc/apache2/apache2.conf")
    Configure("sudo sed -i '176i</Directory>' /etc/apache2/apache2.conf")
    
    Configure("sudo sed -e '12d' /etc/apache2/sites-available/000-default.conf >.tempFile;sudo mv .tempFile /etc/apache2/sites-available/000-default.conf")
    Configure("sudo sed -i '12i DocumentRoot "+currentDirectory+"' /etc/apache2/sites-available/000-default.conf")
    Configure("sudo sed -e '5d' /etc/apache2/sites-available/default-ssl.conf >.tempFile;sudo mv .tempFile /etc/apache2/sites-available/default-ssl.conf")
    Configure("sudo sed -i '5i DocumentRoot "+currentDirectory+"' /etc/apache2/sites-available/default-ssl.conf")
    Configure("sudo service apache2 restart")
    
def main():
    configure()
main()
