#!/usr/bin/env python3

import subprocess
import os

pianobar_fifo = '/tmp/pianobar'
if not os.path.exists(pianobar_fifo):
    os.mkfifo(pianobar_fifo)

output = open('/var/log/pianobar.log', 'a')
subprocess.Popen("pianobar", stdout=output, stderr=output)

