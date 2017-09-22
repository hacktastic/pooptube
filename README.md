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
  }
  
  
netdata_nginx_cert: |
  -----BEGIN CERTIFICATE-----
  MIIDYDCCAkigAwIBAgIJALzSQ6U17UgkMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
  BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
  aWRnaXRzIFB0eSBMdGQwHhcNMTcwOTIyMDA1MjIxWhcNMTgwOTIyMDA1MjIxWjBF
  MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
  ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
  CgKCAQEA1hn3QAAtVZHAYGGM5N0synbBF07c8sieGvU84ZLL0gvg2o6dOVccj3Bi
  BQAMk1583qKQaOJ2fJOA+TtB2NOE0or4cjUMOtf+g9z0OdpmIFr9NAn40ILKJlf2
  R70/ogYEdYT3tnVr/wp1XnKVhONqbo3epsiP7wBqah/fJWOubsWKyDnFD0m80sNz
  xAJ7EHH9qX+xjGkYBVogTF8dL8HMceeD79a5ZhiyAP8jhUXHxiTQQ1y6LA9SuyqW
  i/A0rgXzdgz95VSENREp42r86mk4VtIPLsuHSFBjIp9JvEye5RN8Yoj2zQaqTosd
  r3CHt8M4WuJ6Fo8iCK9eiUshP4LnZwIDAQABo1MwUTAdBgNVHQ4EFgQUrru6aNU0
  HVQwjZwbPUhby0KLqb0wHwYDVR0jBBgwFoAUrru6aNU0HVQwjZwbPUhby0KLqb0w
  DwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAKZrzkecnhZZfTF67
  3H8q4ZMMob+mzhFsqqaRNyZ/WeJhE0c4L5upxyCx72CRcrjzZsOIrAYxtDbhfXJ5
  /xKmGeMTuGZ+opl/T/RJVnF/TqC0efPrhW1kZtTUqMHqpQkQghfYK3ucvkTaOg6n
  1dmZWkKfcaOsLx3ukWRyQok5RYiXd4Qg7TbSbBpdCqJ2i+LvaB4k+BpNi4KQ2qvq
  DYvjc0YAA6yZJzBBv99WQc1i3S9pWpPHXvWQ121aRlNpLVYeNBwYq7jtsfzSFlRN
  9YuhOOB/GZG7zO70d1KkOG0HDzVsG0X6g+xqnDWlnr392PMqtRrLLR9SJl4TRr/f
  uNEsBg==
  -----END CERTIFICATE-----

netdata_nginx_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDWGfdAAC1VkcBg
  YYzk3SzKdsEXTtzyyJ4a9TzhksvSC+Dajp05VxyPcGIFAAyTXnzeopBo4nZ8k4D5
  O0HY04TSivhyNQw61/6D3PQ52mYgWv00CfjQgsomV/ZHvT+iBgR1hPe2dWv/CnVe
  cpWE42pujd6myI/vAGpqH98lY65uxYrIOcUPSbzSw3PEAnsQcf2pf7GMaRgFWiBM
  Xx0vwcxx54Pv1rlmGLIA/yOFRcfGJNBDXLosD1K7KpaL8DSuBfN2DP3lVIQ1ESnj
  avzqaThW0g8uy4dIUGMin0m8TJ7lE3xiiPbNBqpOix2vcIe3wzha4noWjyIIr16J
  SyE/gudnAgMBAAECggEAZICT2+s5XK2qjJO+O8DHQdM1GOfgN+eMsELmbU0neFYz
  GuVPUJdfxMWQfaBkRtlX7HqLJ3EHBbuIE3aJlmrUMrEhpxrXvtedlfCmhHHM9us/
  aKo1rkt28UDhTxO7Rydj+HaOgYvlQjd6mPdY0KSgVX0rQ0dqqVqcmWyUp0x/mWct
  xzEm9B1sNCSYCWkF9U05IZTPb6aB6f5bleN9UkX26VQtpHyyOf4TgvkQTXbCfueP
  magsPwvLeqg0FH0qSdpJBt9kSKqxG4A5zIb6zewaC7GLnroNgeKQUUZxsVvZkoHT
  1IJ65lydx8Fy2onWCG5WjHb4W1ROXK7179JLJLAloQKBgQDt44XnxuMLUMcTs0v4
  RjTy07Pi7aLlLzO4fsWjbeuUuh0Qvi21mYuOmt/+JgzzRJVWzEgp5eRaDSJ43JJV
  L9akZpxhoGIaYOZ2aaY3EarLs34u5TO/GjYpkKWltPCxJu0JmHmevpg910Qr5QDd
  rj0Ru6F71LXhTbU2OG7GjKEE/QKBgQDmZtM8IusZ4OjvV+byYKE+xU22au6pMjdE
  psNJ+kMNSNt3rphZdDVrBVr/55Fey03qBvFdYwazypfrpqKvRSlkr7Tz8Xma36Om
  fOyfD7UjT7esF+IsZ1pqIqUaj4SUUWCtyQrJ62s6IonLLfRej0vGvG7JlIZS/vgB
  YbwTaMtdMwKBgEDY2eLBs5idD3eOU7I9KSfcj9fXYaVKBbZQUH3pc+OaDFxJC1rK
  nWFlVJQKOVODKZZ8n1tUgLgPhosdzYINRVyRYCW4u6VnLsuupxGx7jYTGt2bu0xn
  z8Xq2UzfkxEnhEwuVVDxsbyB1uKETYUgfyM7W5zO8jmVnkVGguP659XdAoGAT5fW
  AUBO13HLBmPndHPNQFIItqvaJrkiPqUdccDyyPQSXRYDq2Np0L7Y4O6uWYECOYaM
  eyZqelHSiaXXLZVG53GLoXoZ+FapwioF1C0o9jnjyZ+2koBhy6iMQNCzjElQjLiW
  8YpSUJL95yLI+KGoG8+ctiaJAML0CgYpYssg9eECgYA/CIs3BUWBAXlvtMsRQPzv
  0VXBoRjqzwrxGGFgeqHpB4zzgLGluNHoX3eXChSs5aKIbsUitSgo7qmrAcnA4RcH
  IPvWpMHqGpcYvc9vXKD5KhZc2jxEa9lK7cO7vw/J10jZgLIyFundAio4GdU9XgGW
  iOt3EMq63HKQfxMMqiiGfA==
  -----END PRIVATE KEY-----

nginx_password: zer0_cool:$apr1$uxEyjZDV$ZTV9KYM4JDYekG4v3QHy70</pre></code>

The gcloud and netdata settings are optional, what's important are the pandora email and password.

A good ansible-vault tutorial is here: https://gist.github.com/tristanfisher/e5a306144a637dc739e7

Automatic gcloud DNS Registration (optional)
=================================
For ease of SSH'ing into the hosts on my local network, I have rigged up a small python script to register the hostname of each pi as a CNAME record in my private gcloud domain. Relevant config should be stored in ansible-vault (see above).

Netdata (optional)
==================
You may optionally install the netdata monitoring tool. This installer (1) downloads the automatic installer, (2) executes the installer with default settings, (3) slaps an nginx frontend to handle SSL and basic-auth. To generate the passwords file for nginx, follow this guide: 
<pre><code>$ printf "zer0_cool:$(openssl passwd -apr1)" > /etc/nginx/passwords
Password: 
Verifying - Password: 
$ cat /etc/nginx/passwords 
zer0_cool:$apr1$uxEyjZDV$ZTV9KYM4JDYekG4v3QHy70
</code></pre>

More details on netdata can be found here: 

https://github.com/firehol/netdata

https://github.com/firehol/netdata/wiki

https://github.com/firehol/netdata/wiki/Running-behind-nginx
