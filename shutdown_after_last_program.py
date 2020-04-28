#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os,sys,time,datetime,json,io,subprocess
from urllib.request import urlopen
from crontab import CronTab

response = urlopen('http://localhost:20772/api/reserves.json')
res = json.load(io.TextIOWrapper(response, response.getheader('content-type').split('charset=')[1]))

#UNIX Time (Now)
now_unix = time.time()

#UNIX Time (Tommorow 7am)
tmrw = datetime.datetime.now() + datetime.timedelta(days=1)
tmrw7am = datetime.datetime.strptime(str(tmrw.date())+' 7:00:00', '%Y-%m-%d %H:%M:%S')
tmrw7am_unix = tmrw7am.timestamp()

reserves_today = [ent['end']/1000 for ent in res if (ent['end']/1000 > now_unix) and ent['end']/1000 < tmrw7am_unix]

if len(reserves_today) > 0:
    shutdown_time = datetime.datetime.fromtimestamp(reserves_today[-1]) + datetime.timedelta(minutes=5)
    shutdown_hour = str(shutdown_time)[-8:-6]
    shutdown_minute = str(shutdown_time)[-5:-3]
    cron = CronTab(user='root')
    for _job in cron:
        if _job.comment == 'shutdown_after_last_program':
            _job.setall(shutdown_minute+' '+shutdown_hour+' * * *')
            cron.write()
