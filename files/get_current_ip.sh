#!/bin/bash

timestamp=$(date +%F\ %T)
ip_addr=$(/sbin/ifconfig wlan0 | grep 'inet addr' | awk -F":" '{print $2}' | awk '{print $1}')

echo "$timestamp $HOSTNAME $ip_addr"

