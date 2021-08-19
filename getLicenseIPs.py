### Written by Andrew Shuman
### Aug 19 2021

import requests
import json
import datetime
import subprocess
import base64
import time
import os
import smtplib
import getpass
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

### TODO Add Config file for this.

param = {

            "username" : "USERNAME",
            ### If wanting to run this with cron, you will need to enter your password here. 
            ### I reccomend using base64 as an obfuscation method, however this is insecure. 
            ### You could also do things like use the API access and secret key or use a secret server, etc.
            "password" : getpass.getpass("Please enter password\n"),

            "releaseSession" : "false"

}

### SC IP

url = 'https://SC_IP//rest/'

### Get the API Token

def getToken():
    r = requests.post(url + 'token', params=param, verify=False)
    token = str(r.json()['response']['token'])
    cookie = r.cookies
    return token, cookie

### Get the config settings from Tenable.SC

def getConfig():
    token, cookie = getToken()
    header = {"X-SecurityCenter" : str(token), "Content-Type" : "application/json"}
    r = requests.get(url + 'configSection/0', headers=header, cookies=cookie, verify=False)
    json_data = json.loads(r.content)
    response = json_data['response']
    config = response['LicenseConfig']
    maxipcount = config['maxIPCount']
    ipcount = config['ipCount']
    subtraction = int(maxipcount) - int(ipcount)
    return subtraction

### Email
if getConfig() < ###Number of systems left that you want to trigger email. If you wanted to get emailed when there is 3000 ips left on your license, just put 3000 here###:
# email options
    SERVER = "SMTP_IP:PORT"
    FROM = "SC"
    TO = ["email"]
    SUBJECT = "Alert!"
    TEXT = "Our license only has 3000 IPs left."

    message = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP(SERVER)
    server.set_debuglevel(0)
    server.sendmail(FROM, TO, message)
    server.quit()
