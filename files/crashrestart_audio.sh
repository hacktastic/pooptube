#!/bin/bash

dead_count=0
sleep_interval=5
threshold=4
lockfile_path="/tmp/crashrestart_audio.pid"


function write_log {
	echo -e "[$(date +%F\ %T)] $1"
}

function check_for_lockfile {
	if [ -f $lockfile_path ]; then
		write_log "Found pid file. Script is probably running."
		exit 0
	else
		write_log "No pid file found. Dropping one."
		echo "$!" > $lockfile_path
		trap "rm -rf $lockfile_path" EXIT
	fi
}

function kickstart_pianobar {
    write_log "Going to kickstart pianobar"
    ps -ef | egrep "pianobar$"
    ps -ef | egrep "pianobar$" | awk '{print $2}' | xargs kill -9
    /root/pianobar_scripts/pianobar_wrapper.py
}

function is_running {
	cat /proc/asound/card0/pcm*/sub*/status | grep -c RUNNING
}

check_for_lockfile

while [[ $dead_count -lt $threshold ]]; do
	if [[ $(is_running) -ne 1 ]]; then
		write_log "audio not playing"
		dead_count=$((dead_count+1))
		write_log "dead_count is now $dead_count"
		if [[ $dead_count -ge $threshold ]]; then
			kickstart_pianobar
			dead_count=0
		fi
	else
		write_log "audio is playing"
		dead_count=0
	fi
	sleep $sleep_interval
done

