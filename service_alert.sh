#!/bin/bash

###edit the following
service=SecurityCenter
email="email"
###stop editing

host="Security Center"
if (( $(ps -ef | grep -v grep | grep $service | wc -l) > 0 ))
then
echo "$service is running"
else
/etc/init.d/$service start
if (( $(ps -ef | grep -v grep | grep $service | wc -l) > 0 ))
then
subject="$service at $host has been started"
echo "$service on $host wasn't running and has been started" | mail -s "$subject " $email
else
subject="$service at $host is not running"
echo "$service on $host is stopped and cannot be started!!!" | mail -s "$subject " $email
fi
fi
