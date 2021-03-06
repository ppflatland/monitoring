# -*- coding: utf-8 -*-
import config
from config import token, chat_id_Maxim, chat_id_Test_group, chat_id_All
import requests
from collections  import defaultdict 
import time, datetime, calendar
from sqlite import SQLighter

del_mess_list = defaultdict(list)
check=0
check_mess_id=0
check_str=""

def bot_check_ping (last_check_ping):
    if last_check_ping == 'Network Error':
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u274C %s' %(token,chat_id_Maxim,last_check_ping))
    else:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u2705 %s' %(token,chat_id_Maxim,last_check_ping))

def bot_err_sent (number,ip,error,st):
    if error != 0:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u274C %s-%s error: %s time: %s' %(token,chat_id_Maxim, number,ip,error,st))
        print(response.content)
    else:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u2705 %s-%s error: %s time: %s' %(token,chat_id_Maxim, number,ip,error,st))

def bot_code_sent(number,ip,code,st):
    global del_mess_list
    if code != 200 and code != 1:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u26A0 Внимание! Обнаружены проблемы с доступом к серверу %s.open.by' %(token,chat_id_Maxim, number))
        data = response.json()
        #del_mess_list[data['result']['chat']['id']].append(data['result']['message_id'])
        del_mess_list[number].append(data['result']['message_id'])
        print(del_mess_list[number])
    elif code == 200:
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u2705 Сервер %s.open.by начал работать в штатном режиме, код ответа %s' %(token,chat_id_All, number, code))
        for i, server in enumerate(del_mess_list[number]):
            response = requests.get('https://api.telegram.org/bot%s/deleteMessage?chat_id=%s&message_id=%s' %(token,chat_id_All, server))
        print(response.content)

def get_all_status(status):
    global check, check_str, check_mess_id
    server_status = ""
    for i, server in enumerate(status): 
        if (server[1] != "200") and (server[1] != "1"):
            server_status += "Сервер %s.open.by - код ответа %s\n"%(server[0], server[1])
            check=1
        elif server[1] == "1":
            server_status += "Сервер %s.open.by - не отвечает\n"%(server[0])
            check=1
        elif len(server_status)== 0:
            check=0
    if len(server_status)!= 0 and (check_str.lower() != server_status.lower()):
        response = requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=\u26A0 Внимание!  Обнаружена проблема с доступом к серверу(ам):\n%s' %(token,chat_id_All, server_status))
        data = response.json()
        check_mess_id=data['result']['message_id']
        requests.get('https://api.telegram.org/bot%s/pinChatMessage?chat_id=%s&message_id=%s' %(token,chat_id_All, data['result']['message_id']))
        check_str=server_status
        check=1 
    elif check_mess_id != 0 and check==0:
        requests.get('https://api.telegram.org/bot%s/unpinChatMessage?chat_id=%s&message_id=%s' %(token,chat_id_All, check_mess_id))
        check=0
		
def send_message_parser(message):
    header_mess ="Change information  about servers:"
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s\n%s' %(token,chat_id_Maxim, header_mess, message))


def get_reputation_server():
    send_messange=""
    db_worker = SQLighter(config.database)
    reputation = db_worker.all_iformation_reputation_servers()
    field_names = "REPUTATION SERVERS\n"
    s2 = '{0}.open.by\nEMAIL REPUTATION: {1}\nVOLUME CHANGE: {2}\nWEB REPUTATION: {3}\nBLACKLISTED: {4}\n'.format(reputation[0][0],reputation[0][2], reputation[0][5], reputation[0][3], reputation[0][6])
    s3 = '{0}.open.by\nEMAIL REPUTATION: {1}\nVOLUME CHANGE: {2}\nWEB REPUTATION: {3}\nBLACKLISTED: {4}\n'.format(reputation[1][0],reputation[1][2], reputation[1][5], reputation[1][3], reputation[1][6])
    s4 = '{0}.open.by\nEMAIL REPUTATION: {1}\nVOLUME CHANGE: {2}\nWEB REPUTATION: {3}\nBLACKLISTED: {4}\n'.format(reputation[2][0],reputation[2][2], reputation[2][5], reputation[2][3], reputation[2][6])
    s5 = '{0}.open.by\nEMAIL REPUTATION: {1}\nVOLUME CHANGE: {2}\nWEB REPUTATION: {3}\nBLACKLISTED: {4}\n'.format(reputation[3][0],reputation[3][2], reputation[3][5], reputation[3][3], reputation[3][6])
    s6 = '{0}.open.by\nEMAIL REPUTATION: {1}\nVOLUME CHANGE: {2}\nWEB REPUTATION: {3}\nBLACKLISTED: {4}\n'.format(reputation[4][0],reputation[4][2], reputation[4][5], reputation[4][3], reputation[4][6])
    s7 = '{0}.open.by\nEMAIL REPUTATION: {1}\nVOLUME CHANGE: {2}\nWEB REPUTATION: {3}\nBLACKLISTED: {4}\n'.format(reputation[5][0],reputation[5][2], reputation[5][5], reputation[5][3], reputation[5][6])
    s8 = '{0}.open.by\nEMAIL REPUTATION: {1}\nVOLUME CHANGE: {2}\nWEB REPUTATION: {3}\nBLACKLISTED: {4}\n'.format(reputation[6][0],reputation[6][2], reputation[6][5], reputation[6][3], reputation[6][6])
    requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s %s %s %s %s %s %s %s' %(token, chat_id_Maxim, field_names,s2,s3,s4,s5,s6,s7,s8))

        




