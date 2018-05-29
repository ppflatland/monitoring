from http.client import HTTPConnection
from urllib.parse import urlencode
import requests
from collections import defaultdict
from sqlite import SQLighter
from sendmail import mail_send
from sendmail import ping_mail_send
from sendmail import err_mail_send
from telegram_bot_sent import bot_code_sent, bot_check_ping, get_all_status, bot_err_sent
import os
import time, datetime, calendar
import sqlite3
import config
#data = urlencode({"color": "Красный", "var": 15}, encoding="cp1251")

def check_ping():
    hostname = "google.ru"
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    return pingstatus
data = urlencode({'a': 'A'})
headers = {
    'User-Agent': 'Status_server_Maxim',
    'Accept': 'text/html',
    'Accept-Language': 'ru, ru-RU',
    'Accept-Charset': 'windows-1251',
    'Referer': '/',
    'Content-Type': 'application/x-www-form-urlencoded'
}
servers={"s2":"93.84.119.237","s3":"93.84.119.238","s4":"93.84.119.239","s5":"93.84.119.240","s6":"93.84.119.241","s7":"93.84.119.242","s8":"93.84.119.243"}
d = dict()
err = dict()
last_check_ping = "Network Active"
while True:
    if check_ping() != last_check_ping:
        last_check_ping = check_ping()
        bot_check_ping(last_check_ping)
        #ping_mail_send(last_check_ping)
        print("No reply for ping command!")
    if last_check_ping=="Network Active":
        for number in servers.keys():
            try:
                server = HTTPConnection('%s.open.by' %(number))
                server.request('POST', '/', data, headers=headers)
                check_result = server.getresponse()
                code = check_result.status
                reason = check_result.status
                d[number]=code 
                err[number]=0
                server.close()
            except Exception as e:
                err[number] = str(e)
                d[number] = 200
                
        #print(d)
        for number in servers:
            db_worker = SQLighter(config.database)
            base_result = db_worker.status_code(number)
            error_result = db_worker.status_error(number)
            ts = calendar.timegm(time.gmtime())
            ts_base = int(float(base_result[0][1]))
            td = ts - ts_base
            if (error_result[0][0]) != (err.get(number)):
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                error = err.get(number)
                db_worker = SQLighter(config.database)
                db_worker.update_status_error(err.get(number),ts, number)
                print(number,servers.get(number),err.get(number),st)
                bot_err_sent(number,servers.get(number),error,st)
                #err_mail_send(number,error,st)
            elif((err.get(number) != 0) and (td > 300)):
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                error=err.get(number)
                db_worker = SQLighter(config.database)
                db_worker.update_status_error(err.get(number),ts, number)
                print(number,servers.get(number),err.get(number),st)
                bot_err_sent(number,servers.get(number),error,st)
                #err_mail_send(number,error,st)
            elif (int(base_result[0][0])) != (d.get(number)):
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                code=d.get(number)
                db_worker = SQLighter(config.database)
                db_worker.update_status_code(d.get(number),ts, number)
                print(number,d.get(number),st)
                bot_code_sent(number,servers.get(number),code,st)
                #mail_send(number,code,st)
            elif((d.get(number) != 200) and (td > 300)):
            #elif(d.get(number) != 200):
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                code=d.get(number)
                db_worker = SQLighter(config.database)
                db_worker.update_status_code(d.get(number),ts, number)
                print(number,d.get(number),st)
                bot_code_sent(number,servers.get(number),code,st)
                mail_send(number,code,st)
    db_worker = SQLighter(config.database)
    get_all_status(db_worker.all_status_code())
    db_worker.close()
    time.sleep(5)




