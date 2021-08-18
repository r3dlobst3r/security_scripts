#!/bin/bash
UP=$(pgrep SecurityCenter | wc -l);
if [ "$UP" -ne 1 ];
then
        echo "SC is down.";
        sudo service SecurityCenter start

else
        echo "All is well.";
fi
