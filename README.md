# pooptube

Pooptube is a standalone music player that runs on a raspberry pi. It uses your own Pandora account to stream music from the "unofficial Pandora API" via the Pianobar app. See: https://github.com/PromyLOPh/pianobar

Pi Prerequisites
============
1. install raspbian OS
2. boot to the GUI
3. run the Raspberry Pi Configuration tool:
* System
  * change your password
  * change the hostname
  * change boot option to CLI (recommended)
  * disable Auto Login (recommended)
* Interfaces
  * enable SSH
* Localisation
  * set locale [example: "en (English)", "US (United States)", "UTF-8"]
  * set timezone [example: "US" "Pacific"]
  * set keyboard
  * set WiFi country [example: "US United States"]
4. connect to local wifi
5. run <code>apt-get update</code>
6. run <code>apt-get install -y ansible git</code>
7. git clone this repo

Getting Started
===============
Once you have cloned this repo to your Pi's filesystem, cd into the top-level directory. The first thing you need to do is remove my secrets.yml file and create one with your own Pandora account credentials, encrypted with your own ansible-vault password:
<pre><code>pi@pi001:~/pooptube $ rm secrets.yml 

pi@pi001:~/pooptube $ vim secrets.yml
pi@pi001:~/pooptube $ cat secrets.yml 
---
pandora_email: zer0_cool@hack_the_planet.com
pandora_pass: password1

pi@pi001:~/pooptube $ ansible-vault encrypt secrets.yml 
Vault password: 
Encryption successful

pi@pi001:~/pooptube $ cat secrets.yml 
$ANSIBLE_VAULT;1.1;AES256
63376637663032373037646561643032623536393635366536306539356266343131383834373937
73037646561643032623536393635366536306539331383834373937562663431313838343739372
39656537636366337663766303233343337326664343636623730633830353032653464646464373
63373734396432356532366332623564365353433646361383363323234623965363832623930361
3161643235363036610a353863376239333263613434646562363538373563613831623665326539
646537343039373562356163386631235363562386166616662620a6665653736396464313239653
61376638396533613834616362313036365666664393033646337613436313463333863376637663
63376637663032373037646561643032623536393635366536306539356266343131383834373937</code></pre>

Now, run the ansible-playbook command to install our app:
<code>ansible-playbook install_pooptube.yml --ask-vault-pass --become </code>
This will prompt you for the password you just used to encrypt your secrets.yml file.

The playbook will install pianobar along with some configuration files (at <code>/root/.config/pianobar/</code>) and helper scripts (at <code>/root/pianobar_scripts/</code>), as well as configure root cron to keep audio playing.

Logs will stream to <code>/var/log/pianobar.log</code>

Schedule
========
Because pooptube is intended to be run as a standalone app with little user interaction, the choice of Pandora station is controlled by a schedule. This schedule is specified in the YAML file, files/schedule.yml:
<pre><code>---
schedule:
        - stationName: ZZ Top Radio
          startTime: "8:00"

        - stationName: The Glitch Mob Radio
          startTime: "12:00 PM"

        - stationName: B.B. King Radio
          startTime: "4 PM"
</code></pre>

You may specify a startTime in several formats, including "3:00 PM", "15:00", and "3 PM". The file will be installed to /root/.config/pianobar/schedule.yml. Station names must match existing stations in your Pandora account.

Secrets
=======
This project uses ansible-vault to encrypt secrets. Here is a sample file:
<pre><code>---
pandora_email: zer0_cool@hack_the_planet.com
pandora_pass: password1

gcloud_service_account_key_file: gcloud-dns-bot.json
gcloud_project_name: hack_the_planet
gcloud_zone_name: hack_the_planet
gcloud_domain_name: hack_the_planet.com.

gcloud_service_account_key: |
  {
    "type": "service_account",
    "project_id": "hack_the_planet",
    "private_key_id": "abc123abc123abc123",
    "private_key": "-----BEGIN PRIVATE KEY-----\nabc123\n-----END PRIVATE KEY-----\n",
    "client_email": "dns-bot@hack_the_planet.iam.gserviceaccount.com",
    "client_id": "1234567890",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dns-bot%hack_the_planet.iam.gserviceaccount.com"
  }</pre></code>

The gcloud settings are optional, what's important are the pandora email and password.

A good ansible-vault tutorial is here: https://gist.github.com/tristanfisher/e5a306144a637dc739e7

Automatic gcloud DNS Registration (optional)
=================================
For ease of SSH'ing into the hosts on my local network, I have rigged up a small python script to register the hostname of each pi as a CNAME record in my private gcloud domain. Relevant config should be stored in ansible-vault (see above).
