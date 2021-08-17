### Written by Andrew Shuman
### Feb 05, 2020
### Tenable does not have alerts for licence expirtation

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

            "password" : PASS,

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

if Days() < 100:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    cmds = ['./mail.sh']
    subprocess.check_call(cmds, cwd=cur_dir)
    print('mail sent')
