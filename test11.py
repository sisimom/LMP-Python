import re
import json
import yaml
import paramiko
import threading
import pingparsing
import time
from pymongo import MongoClient

class my_threading(threading.Thread):
    
    def __init__(self,threadID,name,ip_address,port,u_name,password):
        threading.Thread.__init__(self)
        self.threadID   = threadID
        self.name       = name
        self.ip_address = ip_address
        self.port       = port
        self.u_name     = u_name
        self.password   = password

    def run(self):
        #print("\nStarting Thread:" + self.name)
        result = main(self.ip_address,self.port,self.u_name,self.password,x)
        #print("Ending Thread:" + self.name)
##
def show_version(ip_address,port,u_name,password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip_address,port,u_name,password)
        stdin,stdout,stderr = ssh.exec_command('show version')
        outlines=stdout.readlines()
        resp=''.join(outlines)
        return resp
    except Exception as e:
        print("Something went Wrong...")
        print(str(e))
        return 0

def grep_version(arg):
    '''This function return image version'''
    error_flag = 1
    lines = arg.split('\n')
    for line in lines:
        obj = re.search('Version:\s+([\d]+\.[\d]+\.[\d]+)',line,re.M)
        if obj:
            #print("Version is:{}".format(obj.group(1)))
            error_flag = 0
            break
    if error_flag == 1:
        print("show version is not present")
    return obj.group(1)

def updating_jdb (version,cnt):
    fname = "1234.yml"
    stream = open(fname, 'r')
    data = yaml.load(stream)
    data['device'][cnt]['Base SW Release'] = version

    with open(fname, 'w') as yaml_file:
        yaml_file.write( yaml.safe_dump(data, default_flow_style=False))

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile,indent=4)
        
##
def main(ip_address,port,u_name,password,x):
    show_out = show_version(ip_address,port,u_name,password)
    Version  = grep_version(show_out)
    print('device: {}' ' version is: {}'.format(ip_address,Version),time.ctime(time.time()))
    updating_jdb(Version,x)
    


with open("1234.yml", 'r') as stream:
    data = yaml.load(stream)


for x in range(1,len(data['device'])+1):
    ip_address = data['device'][x]['IP']
    u_name     = data['device'][x]['USERNAME']
    password   = data['device'][x]['PASSWORD']
    port       = data['device'][x]['PORT']
    version_obj = my_threading(1,x,ip_address,port,u_name,password)

    version_obj.start()
    version_obj.join()
