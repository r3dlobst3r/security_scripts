### Written by Andrew Shuman
### Feb 05, 2020
### Tenable does not have alerts for licence expirtation, this script will calculate the number of days left until expiration and use 
### mail script to email users if there are less than 100 days on license.

import requests
import json
import datetime
import subprocess
import base64
import time
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

### TODO Add Config file for this.

param = {

            "username" : "USER",

             ### If wanting to run this with cron, you will need to enter your password here:
             ### "password" : "PASSWORD"
             ### I reccomend using base64 as an obfuscation method, however this is insecure. 
             ###You could also do things like use the API access and secret key or use a secret server, etc.
            "password" : getpass.getpass("Please enter password\n"),

            "releaseSession" : "false"

}
### SC URL

url = 'https://IP//rest/'

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
    expiration = config['expiration']
    return expiration
    print(expiration)
### Calculate number of days before license expiration

def Days():
    from datetime import datetime
    expiration = getConfig()
    date = int(time.time())
    delta = ((float(expiration)-float(date))/(60*60*24))
    print(delta)
    return delta

if Days() < ###Specify number of days left on license that you want to trigger email. If you want it to email you when there are less than 100 days left, just put 100 here.###::
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
