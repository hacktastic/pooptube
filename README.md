# pooptube

Pooptube is a standalone music player that runs on a raspberry pi. To set up from fresh pi:

1. install raspbian
1. log in with default creds
1. change pi user passwd
1. connect to local wifi
1. configure pi to boot to console
1. run <code>apt-get update</code>
1. run <code>apt-get install -y ansible</code>
1. clone this repo
1. edit <code>install_pooptube.yml</code> to include your Pandora username and password
1. run <code>ansible-playbook install_pooptube.yml</code>

This will install pianobar along with some configuration files (at <code>/root/.config/pianobar/</code>) and helper scripts (at <code>/root/pianobar_scripts/</code>).

Launch pianobar by running the wrapper script <code>/root/pianobar_scripts/pianobar_wrapper.py</code>. Logs will stream to <code>/var/log/pianobar.log</code>
