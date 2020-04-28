#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys,time,datetime,json,io,subprocess
from urllib.request import urlopen

response = urlopen('http://localhost:20772/api/reserves.json')
res = json.load(io.TextIOWrapper(response, response.getheader('content-type').split('charset=')[1]))

#UNIX Time (Now)
now_unix = time.time()

#UNIX Time (Tommorow 7am)
tmrw = datetime.datetime.now() + datetime.timedelta(days=1)
tmrw7am = datetime.datetime.strptime(str(tmrw.date())+' 7:00:00', '%Y-%m-%d %H:%M:%S')
tmrw7am_unix = tmrw7am.timestamp()

reserves_today = [ent['start']/1000 for ent in res if (ent['start']/1000 > now_unix) and ent['start']/1000 < tmrw7am_unix]

if len(reserves_today) > 0:
    wake_up_time = datetime.datetime.fromtimestamp(reserves_today[0]) - datetime.timedelta(minutes=5)
    print(str(wake_up_time)[-8:-3])
    wake_up_cmd = '/bin/bash /home/anisaba/scripts/shutdown_and_wakeup.sh '+str(wake_up_time)[-8:-3]
else:
    print('7:00')
    wake_up_cmd = '/bin/bash /home/anisaba/scripts/shutdown_and_wakeup.sh 07:00'
    
print (wake_up_cmd)
subprocess.getoutput(wake_up_cmd)

